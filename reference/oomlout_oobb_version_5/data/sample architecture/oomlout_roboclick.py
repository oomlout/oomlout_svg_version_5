from __future__ import annotations

import argparse
import copy
import datetime
import json
import os
import random
import re
import sys
import time
from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

import yaml

if sys.platform == "win32":
    import msvcrt
else:
    import select


__all__ = [
    "main",
    "cli",
    "run_single",
    "run_folder",
    "run_action",
    "discover_actions",
    "build_action_lookup",
    "get_all_actions_documentation",
    "export_actions_documentation_json",
    "export_actions_documentation_html",
    "check_key_pressed",
    "scroll_lock_toggled",
    "delay",
    "robo_delay",
]


###############################################################################
# Shared automation primitives (moved from automation_primitives.py)
###############################################################################


def check_key_pressed() -> str | None:
    try:
        if sys.platform == "win32":
            if msvcrt.kbhit():
                return msvcrt.getch().decode("utf-8", errors="ignore").lower()
        else:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                return sys.stdin.read(1).lower()
    except Exception:
        return None
    return None


def scroll_lock_toggled() -> bool:
    if sys.platform != "win32":
        return False
    try:
        import ctypes

        # 0x91 = VK_SCROLL
        return (ctypes.windll.user32.GetKeyState(0x91) & 1) == 1
    except Exception:
        return False


def delay(**kwargs: Any) -> str:
    delay_seconds = kwargs.get("delay", 1)
    rand_seconds = kwargs.get("rand", 0)
    message = kwargs.get("message", "")
    mode_skip_key = kwargs.get("mode_skip_key", True)
    mode_scroll_lock_skip = kwargs.get("mode_scroll_lock_skip", True)

    try:
        delay_seconds = float(delay_seconds)
    except Exception:
        delay_seconds = 1.0
    try:
        rand_seconds = int(rand_seconds)
    except Exception:
        rand_seconds = 0

    if message:
        print(message)
    if rand_seconds > 0:
        delay_seconds += random.randint(0, rand_seconds)

    if delay_seconds <= 1.0:
        time.sleep(delay_seconds)
        return ""

    if delay_seconds > 5.0:
        print(f"<<<<<>>>>> waiting for {delay_seconds:.0f} seconds (press 's' to skip)")
        splits = 10
        chunk = max(1, int(delay_seconds // splits))
        for _ in range(splits):
            print(".", end="", flush=True)
            for _ in range(chunk):
                if mode_skip_key and check_key_pressed() == "s":
                    print("\nDelay skipped by 's'")
                    time.sleep(1)
                    return ""
                if mode_scroll_lock_skip and scroll_lock_toggled():
                    print("\nScroll Lock toggled; skipping delay")
                    time.sleep(1)
                    return ""
                time.sleep(1)
        print("")
        return ""

    print(f"waiting for {delay_seconds:.0f} seconds (press 's' to skip)", end="", flush=True)
    remaining = max(1, int(round(delay_seconds)))
    for _ in range(remaining):
        print(".", end="", flush=True)
        if mode_skip_key and check_key_pressed() == "s":
            print("\nDelay skipped by 's'")
            time.sleep(1)
            return ""
        time.sleep(1)
    print("")
    return ""


def robo_delay(**kwargs: Any) -> str:
    return delay(**kwargs)


###############################################################################
# Action loading and discovery (moved from action_loader.py)
###############################################################################


@dataclass(frozen=True)
class DiscoveredAction:
    name: str
    path: Path
    metadata: dict[str, Any]
    action_fn: Callable[..., Any]
    test_fn: Callable[..., Any]
    aliases: tuple[str, ...] = ()


def resolve_actions_root(actions_root: str | Path | None = None) -> Path:
    if actions_root is not None:
        return Path(actions_root).resolve()
    return (Path(__file__).resolve().parent / "actions").resolve()


def _make_dispatch_shim(source_action_name: str) -> Callable[..., Any]:
    def _dispatch_action(command_name: str, **kwargs: Any) -> Any:
        discovered = kwargs.get("_discovered_actions")
        if discovered is None:
            discovered = build_action_lookup(actions_root=kwargs.get("actions_root"))

        action_info = discovered.get(command_name)
        if action_info is None:
            print(
                f"Warning: Unknown command during local dispatch '{command_name}' "
                f"(source action: {source_action_name})"
            )
            return ""

        run_kwargs = copy.deepcopy(kwargs)
        action_cfg = run_kwargs.get("action", {}) or {}
        if not isinstance(action_cfg, dict):
            action_cfg = {}
        action_cfg = copy.deepcopy(action_cfg)
        action_cfg.setdefault("command", command_name)
        run_kwargs["action"] = action_cfg
        run_kwargs["_discovered_actions"] = discovered
        return action_info.action_fn(**run_kwargs)

    return _dispatch_action


def _load_module_from_file(
    file_path: Path,
    action_name: str,
    inject_dispatch_shim: bool = False,
) -> ModuleType:
    module_name = f"roboclick_action_{action_name}_{abs(hash(str(file_path)))}"
    spec = spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {file_path}")
    module = module_from_spec(spec)

    if inject_dispatch_shim:
        setattr(module, "_dispatch_action", _make_dispatch_shim(action_name))

    spec.loader.exec_module(module)

    if inject_dispatch_shim and not callable(getattr(module, "_dispatch_action", None)):
        setattr(module, "_dispatch_action", _make_dispatch_shim(action_name))
    return module


def discover_actions(actions_root: str | Path | None = None) -> dict[str, DiscoveredAction]:
    root = resolve_actions_root(actions_root)
    actions: dict[str, DiscoveredAction] = {}
    if not root.exists():
        return actions

    entries = sorted(root.iterdir(), key=lambda p: p.name)
    for entry in entries:
        if not entry.is_dir():
            continue
        working_file = entry / "working.py"
        if not working_file.is_file():
            continue

        try:
            module = _load_module_from_file(
                working_file,
                entry.name,
                inject_dispatch_shim=True,
            )
        except Exception as exc:
            print(f"Warning: failed to import action module {working_file}: {exc}")
            continue

        define_fn = getattr(module, "define", None)
        action_fn = getattr(module, "action", None)
        test_fn = getattr(module, "test", None)
        if not callable(define_fn) or not callable(action_fn):
            print(
                f"Warning: skipping action '{entry.name}' because working.py must expose define() and action()"
            )
            continue

        if not callable(test_fn):
            fallback_test_files = (
                entry / "test.py",
                entry / "oomlout_test.py",
            )
            for test_file in fallback_test_files:
                if not test_file.is_file():
                    continue
                try:
                    test_module = _load_module_from_file(
                        test_file,
                        f"{entry.name}_{test_file.stem}",
                        inject_dispatch_shim=False,
                    )
                    test_fn = getattr(test_module, "test", None)
                except Exception as exc:
                    print(f"Warning: failed to import test module {test_file}: {exc}")
                    continue
                if callable(test_fn):
                    break
        if not callable(test_fn):
            print(
                "Warning: skipping action "
                f"'{entry.name}' because no callable test() found in "
                "working.py, test.py, or oomlout_test.py"
            )
            continue

        metadata_raw = define_fn()
        metadata = metadata_raw if isinstance(metadata_raw, dict) else {}
        metadata.setdefault("name", entry.name)
        metadata.setdefault("description", "")
        metadata.setdefault("variables", [])
        metadata.setdefault("category", "Other")

        declared_name = metadata.get("name", entry.name)
        if declared_name != entry.name:
            print(
                f"Warning: action '{entry.name}' define().name='{declared_name}'. Using folder name '{entry.name}'."
            )
            metadata["name"] = entry.name

        actions[entry.name] = DiscoveredAction(
            name=entry.name,
            path=working_file,
            metadata=metadata,
            action_fn=action_fn,
            test_fn=test_fn,
            aliases=tuple(_extract_aliases(metadata)),
        )
    return actions


def _extract_aliases(metadata: dict[str, Any]) -> list[str]:
    raw_aliases: list[str] = []

    for key in ("name_short",):
        value = metadata.get(key)
        if isinstance(value, str):
            raw_aliases.append(value)
        elif isinstance(value, list):
            raw_aliases.extend([item for item in value if isinstance(item, str)])

    cleaned: list[str] = []
    seen: set[str] = set()
    for alias in raw_aliases:
        normal = alias.strip()
        if not normal:
            continue
        if normal in seen:
            continue
        seen.add(normal)
        cleaned.append(normal)
    return cleaned


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _extract_variable_names(raw_variables: Any) -> list[str]:
    if not isinstance(raw_variables, list):
        return []

    names: list[str] = []
    seen: set[str] = set()
    for item in raw_variables:
        name_value = ""
        if isinstance(item, dict):
            name_value = _coerce_text(item.get("name", ""))
        elif isinstance(item, str):
            name_value = _coerce_text(item)
        if not name_value:
            continue
        if name_value in seen:
            continue
        seen.add(name_value)
        names.append(name_value)
    return names


def _build_summary(
    description: str,
    variable_names: list[str],
    returns_text: str,
) -> str:
    description_clean = " ".join(description.split())
    if description_clean:
        first_sentence = re.split(r"(?<=[.!?])\s+", description_clean, maxsplit=1)[0]
        return first_sentence

    if variable_names:
        sample = ", ".join(variable_names[:3])
        if len(variable_names) > 3:
            sample += ", ..."
        return f"Inputs: {sample}."

    if returns_text:
        returns_clean = " ".join(returns_text.split())
        first_sentence = re.split(r"(?<=[.!?])\s+", returns_clean, maxsplit=1)[0]
        return f"Returns: {first_sentence}"

    return "No summary available."


def build_action_lookup(actions_root: str | Path | None = None) -> dict[str, DiscoveredAction]:
    canonical_actions = discover_actions(actions_root=actions_root)
    lookup: dict[str, DiscoveredAction] = {}

    for action_name, discovered_action in canonical_actions.items():
        lookup[action_name] = discovered_action

    for action_name, discovered_action in canonical_actions.items():
        for alias in discovered_action.aliases:
            if alias == action_name:
                continue
            if alias in lookup and lookup[alias].name != action_name:
                print(
                    f"Warning: alias '{alias}' for action '{action_name}' conflicts with action '{lookup[alias].name}'."
                )
                continue
            lookup[alias] = discovered_action
    return lookup


def get_all_actions_documentation(actions_root: str | Path | None = None) -> list[dict[str, Any]]:
    docs: list[dict[str, Any]] = []
    discovered = discover_actions(actions_root=actions_root)
    for action_name in sorted(discovered.keys()):
        action_info = discovered[action_name]
        metadata = action_info.metadata
        aliases = list(action_info.aliases)
        description = _coerce_text(metadata.get("description", ""))
        returns_text = _coerce_text(metadata.get("returns", ""))
        variable_names = _extract_variable_names(metadata.get("variables", []))
        name_long = _coerce_text(metadata.get("name_long", "")) or action_name

        # Ensure variables are always a list of dicts with name and description
        raw_vars = metadata.get("variables", [])
        variables = []
        for v in raw_vars:
            if isinstance(v, dict):
                name = _coerce_text(v.get("name", ""))
                desc = _coerce_text(v.get("description", ""))
                variables.append({"name": name, "description": desc, "type": v.get("type", ""), "default": v.get("default", "")})
            elif isinstance(v, str):
                variables.append({"name": _coerce_text(v), "description": "", "type": "", "default": ""})
            else:
                variables.append({"name": str(v), "description": "", "type": "", "default": ""})

        docs.append(
            {
                "command": action_name,
                "name_long": name_long,
                "name_short_options": aliases,
                "description": description,
                "summary": _build_summary(
                    description=description,
                    variable_names=variable_names,
                    returns_text=returns_text,
                ),
                "variables": variables,
                "variable_names": variable_names,
                "category": metadata.get("category", "Other"),
                "returns": returns_text,
                "aliases": aliases,
            }
        )
    return docs


###############################################################################
# Runner logic (moved from runner.py)
###############################################################################


def _load_yaml_file(path: str | os.PathLike[str]) -> dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
            return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        print(f"Warning: YAML file not found: {path}")
    except yaml.YAMLError as exc:
        print(f"Warning: failed to parse YAML file {path}: {exc}")
    return {}


def _manual_yaml_path(file_action: str) -> str:
    file_action_path = Path(file_action)
    if file_action_path.suffix:
        return str(file_action_path.with_name(f"{file_action_path.stem}_manual{file_action_path.suffix}"))
    return f"{file_action}_manual.yaml"


def _load_workings(kwargs: dict[str, Any]) -> dict[str, Any]:
    workings = kwargs.get("workings")
    if isinstance(workings, dict) and workings:
        return copy.deepcopy(workings)
    file_action = kwargs.get("file_action", "working.yaml")
    return _load_yaml_file(file_action)


def _merge_manual_into_workings(file_action: str, workings: dict[str, Any]) -> dict[str, Any]:
    manual_file = _manual_yaml_path(file_action)
    if not os.path.exists(manual_file):
        return workings
    manual_data = _load_yaml_file(manual_file)
    if manual_data:
        print(f"loading manual configuration from {manual_file}")
        workings.update(manual_data)
    return workings


def _persist_result_dict(file_action: str, result: dict[str, Any]) -> None:
    manual_file = _manual_yaml_path(file_action)
    details: dict[str, Any] = {}
    if os.path.exists(manual_file):
        loaded = _load_yaml_file(manual_file)
        if isinstance(loaded, dict):
            details = loaded

    print("Updating workings with result dict")
    for key, value in result.items():
        details[key] = value
        print(f"    Updated workings key: {key} with value: {value}")

    with open(manual_file, "w", encoding="utf-8") as file:
        yaml.safe_dump(details, file, sort_keys=False)
    print(f"Updated workings saved to {manual_file}")


def _normalize_mode_list(mode: Any) -> list[str]:
    if isinstance(mode, list):
        raw_modes = mode
    elif mode in (None, ""):
        raw_modes = ["all"]
    else:
        raw_modes = [mode]

    normalized: list[str] = []
    for item in raw_modes:
        mode_name = str(item)
        if mode_name in ("all", ""):
            normalized.extend(["oomlout_ai_roboclick", "oomlout_corel_roboclick"])
        elif mode_name == "ai":
            normalized.append("oomlout_ai_roboclick")
        elif mode_name == "corel":
            normalized.append("oomlout_corel_roboclick")
        else:
            normalized.append(mode_name)
    return normalized


def _expand_numbered_variants(mode_list: list[str]) -> list[str]:
    expanded: list[str] = []
    for mode_name in mode_list:
        expanded.append(mode_name)
        tail = mode_name.rsplit("_", 1)[-1]
        if tail.isdigit():
            continue
        expanded.extend([f"{mode_name}_{i}" for i in range(1, 101)])
    return expanded


def _extract_mode_index(mode_name: str, prefix: str) -> int | None:
    pattern = rf"^{re.escape(prefix)}_?(\d+)$"
    match = re.match(pattern, mode_name)
    if not match:
        return None
    index = int(match.group(1))
    if 1 <= index <= 100:
        return index
    return None


def _discover_oomp_modes(workings: dict[str, Any]) -> list[str]:
    discovered: list[str] = []
    mode_prefixes = ["oomlout_ai_roboclick", "oomlout_corel_roboclick"]
    for prefix in mode_prefixes:
        indexed_modes: list[tuple[int, str]] = []
        for mode_name, mode_cfg in workings.items():
            if not isinstance(mode_cfg, dict):
                continue
            if not isinstance(mode_cfg.get("actions"), list):
                continue
            mode_index = _extract_mode_index(str(mode_name), prefix)
            if mode_index is None:
                continue
            indexed_modes.append((mode_index, str(mode_name)))
        indexed_modes.sort(key=lambda item: item[0])
        discovered.extend([name for _, name in indexed_modes])
    return discovered



def run_folder_recursive(**kwargs: Any) -> None:
    directory = kwargs.get("directory", "")    

    #get folders in directory but do not recurse into them yet
    entries = sorted(os.listdir(directory))
    for entry in entries:
        run_dir = os.path.join(directory, entry)
        if not os.path.isdir(run_dir):
            continue
        print(f"Processing folder: {run_dir}")
        run_kwargs = copy.deepcopy(kwargs)
        #pop directory from kwargs and set folder for run_folder
        run_kwargs.pop("directory", None)
        run_kwargs["folder"] = run_dir        
        run_folder(**run_kwargs)

def run_folder(**kwargs: Any) -> None:
    folder = kwargs.get("folder", "")
    if not folder:
        print("Error: folder is required for run_folder")
        return

    folder_abs = os.path.abspath(folder)
    if not os.path.isdir(folder_abs):
        print(f"Error: folder does not exist: {folder_abs}")
        return

    file_action_arg = kwargs.get("file_action", "")
    candidate_files: list[str] = []
    if file_action_arg:
        candidate_files.append(file_action_arg)
    candidate_files.extend(["working.oomp", "working.yaml"])

    file_action = ""
    for candidate in candidate_files:
        candidate_path = candidate if os.path.isabs(candidate) else os.path.join(folder_abs, candidate)
        if os.path.exists(candidate_path):
            file_action = candidate_path
            break
    if not file_action:
        print(f"Error: no working file found in {folder_abs}. Expected working.oomp or working.yaml")
        return

    workings = _load_yaml_file(file_action)
    if not workings:
        print(f"Warning: no workings loaded from {file_action}")
        return

    mode_arg = kwargs.get("mode", "all")
    if mode_arg not in ("all", "", None):
        mode_list = _normalize_mode_list(mode_arg)
        modes = _expand_numbered_variants(mode_list)
    else:
        modes = _discover_oomp_modes(workings)

    if not modes:
        print(
            "Warning: no runnable modes found. "
            "Expected keys like oomlout_ai_roboclick_1..100 or oomlout_corel_roboclick_1..100"
        )
        return

    run_kwargs = copy.deepcopy(kwargs)
    run_kwargs["directory"] = folder_abs
    run_kwargs["directory_absolute"] = folder_abs
    run_kwargs["file_action"] = file_action
    run_kwargs["workings"] = workings

    print(f"Running {len(modes)} mode(s) from {file_action}")
    for mode_name in modes:
        run_kwargs["mode"] = mode_name
        run_single(**run_kwargs)


def _directory_matches_filters(directory_name: str, kwargs: dict[str, Any]) -> bool:
    filt = kwargs.get("filter", "")
    filt_all = kwargs.get("filter_all")
    filt_or = kwargs.get("filter_or")
    if filt_all:
        return all(token in directory_name for token in filt_all)
    if filt_or:
        return any(token in directory_name for token in filt_or)
    return (filt in directory_name) or (filt == "")


def run_action(**kwargs: Any) -> Any:
    action_cfg = kwargs.get("action", {}) or {}
    command = action_cfg.get("command")
    if not command:
        print("Warning: action missing 'command' key")
        return ""

    discovered = kwargs.get("_discovered_actions")
    if discovered is None:
        discovered = build_action_lookup(actions_root=kwargs.get("actions_root"))

    action_module = discovered.get(command)
    if action_module is None:
        print(f"Warning: Unknown command '{command}'")
        robo_delay(delay=10)
        return ""
    return action_module.action_fn(**kwargs)


def run_single(**kwargs: Any) -> Any:
    file_action = kwargs.get("file_action", "working.yaml")
    mode = kwargs.get("mode", "")

    workings = _load_workings(kwargs)
    workings = _merge_manual_into_workings(file_action, workings)

    base = workings.get(mode, {})
    if not isinstance(base, dict):
        return ""

    actions = base.get("actions", [])
    if not isinstance(actions, list) or not actions:
        return ""

    file_test = base.get("file_test", "")
    file_test_mode = base.get("file_test_mode", "exists")
    if file_test:
        file_test_absolute = os.path.join(kwargs.get("directory_absolute", ""), file_test)
        print(f"file test mode {file_test_mode} on {file_test_absolute}")
        if file_test_mode == "exists" and os.path.exists(file_test_absolute):
            print(f"File test {file_test_absolute} exists, skipping actions.")
            return ""
        if file_test_mode != "exists" and not os.path.exists(file_test_absolute):
            print(f"File test {file_test_absolute} does not exist, skipping actions.")
            return ""

    discovered = kwargs.get("_discovered_actions")
    if discovered is None:
        discovered = build_action_lookup(actions_root=kwargs.get("actions_root"))
    print(f"Running with actions: {len(actions)}")

    run_kwargs = copy.deepcopy(kwargs)
    run_kwargs["actions"] = actions
    run_kwargs["_discovered_actions"] = discovered

    result: Any = ""
    for action_cfg in actions:
        run_kwargs["action"] = action_cfg
        result = run_action(**run_kwargs)
        if result in ("exit", "exit_no_tab"):
            print("Exiting due to exit command.")
            break
        if isinstance(result, dict):
            _persist_result_dict(file_action=file_action, result=result)
    return result

def run_single_action(**kwargs: Any) -> Any:
    action = kwargs.get("action", {}) or {}
    if not isinstance(action, dict):
        print("Error: action must be a dict")
        return ""
    result = run_action(**kwargs)
    if isinstance(result, dict):
        file_action = kwargs.get("file_action", "working.yaml")
        _persist_result_dict(file_action=file_action, result=result)
    return result

def main(**kwargs: Any) -> None:
    mode_list = _normalize_mode_list(kwargs.get("mode", "all"))
    folder = kwargs.get("folder", "")
    directory = kwargs.get("directory", "")
    file_action_default = kwargs.get("file_action", "working.yaml")
    if kwargs.get("filter", "") and (kwargs.get("filter_all") or kwargs.get("filter_or")):
        print("Error: Too many filters specified. Use only one of filter/filter_all/filter_or.")
        return

    if folder:
        run_folder(**kwargs)
        return

    if directory:
        for entry in sorted(os.listdir(directory)):
            if not _directory_matches_filters(entry, kwargs):
                continue
            run_dir = os.path.join(directory, entry)
            if not os.path.isdir(run_dir):
                continue

            file_action = os.path.join(run_dir, "working.yaml")
            run_kwargs = copy.deepcopy(kwargs)
            run_kwargs["directory"] = run_dir
            run_kwargs["directory_absolute"] = os.path.abspath(run_dir)
            run_kwargs["file_action"] = file_action
            run_kwargs["workings"] = _load_yaml_file(file_action)

            modes_list = _expand_numbered_variants(mode_list)
            for mode_name in modes_list:
                run_kwargs["mode"] = mode_name
                run_single(**run_kwargs)
        return

    run_kwargs = copy.deepcopy(kwargs)
    run_kwargs["file_action"] = file_action_default
    if "workings" not in run_kwargs:
        run_kwargs["workings"] = _load_yaml_file(file_action_default)
    for mode_name in mode_list:
        run_kwargs["mode"] = mode_name
        run_single(**run_kwargs)


###############################################################################
# Documentation export
###############################################################################


def export_actions_documentation_json(output_file: str, actions_root: str | None = None) -> None:
    docs = get_all_actions_documentation(actions_root=actions_root)
    payload = {
        "actions": docs,
        "generated_date": str(datetime.date.today()),
        "total_actions": len(docs),
    }
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)
    print(f"Action documentation written to {output_file}")


def export_actions_documentation_html(
    template_file: str,
    output_file: str,
    actions_root: str | None = None,
) -> None:
    docs = get_all_actions_documentation(actions_root=actions_root)
    payload = {
        "actions": docs,
        "generated_date": str(datetime.date.today()),
        "total_actions": len(docs),
    }
    with open(template_file, "r", encoding="utf-8") as file:
        template_content = file.read()

    if "<!-- DOCUMENTATION_DATA_PLACEHOLDER -->" in template_content:
        js = (
            "const DOCUMENTATION_DATA = "
            + json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
            + ";\nif (typeof window.DOCUMENTATION_DATA_READY === 'function') "
            + "window.DOCUMENTATION_DATA_READY();\n"
        )
        html = template_content.replace("<!-- DOCUMENTATION_DATA_PLACEHOLDER -->", js)
    elif "{{documentation_JSON}}" in template_content:
        html = template_content.replace("{{documentation_JSON}}", json.dumps(docs, indent=2))
    else:
        js = (
            "<script>\nconst DOCUMENTATION_DATA = "
            + json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
            + ";\n</script>\n"
        )
        html = template_content.replace("<script>", js + "<script>", 1)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html)
    print(f"Action documentation HTML written to {output_file}")


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RoboClick modular action runner")
    parser.add_argument("--mode", default="all")
    parser.add_argument("--file-action", default="working.yaml")
    parser.add_argument("--folder", default="")
    parser.add_argument("--directory", default="")
    parser.add_argument("--actions-root", default=None)
    parser.add_argument("--docs-json", default="")
    parser.add_argument("--docs-html-template", default="")
    parser.add_argument("--docs-html-output", default="")
    parser.add_argument("--docs-only", action="store_true")
    return parser


def cli() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()
    if args.docs_json:
        export_actions_documentation_json(args.docs_json, actions_root=args.actions_root)
    if args.docs_html_template and args.docs_html_output:
        export_actions_documentation_html(
            template_file=args.docs_html_template,
            output_file=args.docs_html_output,
            actions_root=args.actions_root,
        )
    if not args.docs_only:
        main(
            mode=args.mode,
            file_action=args.file_action,
            folder=args.folder,
            directory=args.directory,
            actions_root=args.actions_root,
        )


##### utility stuff
def get_url(part):
    file_url = "url.yaml"
    directory = get_directory(part)
    file_url = f"{directory}\\url.yaml"
    import yaml
    url = ""
    if os.path.isfile(file_url):
        #url may have multiple lines use the last one
        with open(file_url, 'r', encoding='utf-8') as f:
            try:
                data_list = yaml.safe_load(f)
                url = data_list[len(data_list)-1]
            except Exception as e:
                print(f"Error reading url from {file_url}: {e}")
    return url
                
            

def get_directory(part):
    
    #type, size, color, description_main, description_extra
    tags = ["classification","type", "size", "color", "description_main", "description_extra", "manufacturer", "part_number"]

    directory = ""

    for tag in tags:
        if tag in part:
            if part[tag] != "":
                if directory != "":
                    directory += "_"
                extra = part[tag]
                if extra == None:
                    extra = ""
                directory += str(extra)
    #make lowercase and replace spaces with underscores and slashes with underscores
    directory = directory.replace(" ", "_")
    directory = directory.replace("/", "_")
    directory = directory.replace("\\", "_")
    directory = directory.replace("__", "_")
    directory = directory.replace(")", "_")
    directory = directory.replace("(", "_")
    directory = directory.lower()

    directory = f"parts\\{directory}"

    return directory

def add_action(**kwargs):
    part = kwargs.get("part", {})
    actions = kwargs.get("actions", {})
    action_name = kwargs.get("action_name", "")
    action_type = kwargs.get("action_type", "ai")
    file_test = kwargs.get("file_test", "tag")

    #get largest existing index for this action_type
    count = 1
    if True:
        while True:
            test_action_name = f"oomlout_{action_type}_roboclick_{count}"
            test_action = part.get(test_action_name, {})
            if test_action != {}:
                count += 1
            else:                
                break

        action_id = f"oomlout_{action_type}_roboclick_{count}"

    #filetest_name and add create file at end if tag
    if True:
        if file_test =="tag":
            file_test = f"aaaa_{action_name}_tag_done.txt"
            action = {}
            action["command"] = "create_text_file"
            action["file_name"] = file_test
            action["content"] = f"Tag for {action_name} completed."
            actions.append(action)

    base = {}
    base["actions"] = actions
    base["file_test"] = file_test
    part[action_id] = base

################################ utility routines
def ai_query_from_prompts(part,part2,prompts,mode_ai_wait, count, file_destination_yaml="", action_name=""):
    count += 1            
    action_type = "ai" # "corel"
    action_default_name = f"create_prompt_verbose"
    if action_name == "":         
        action_name = f"{action_default_name}" 

    #default to a tag but if an image is created use that instead
    file_test = "tag" #(creates a tag at the end)

    actions = []
    
    ### action 1
    # new chat
    action = {}
    #- command: 'new_chat'
    action["command"] = "new_chat"  
    action["description"] = f"{action_name}"
    actions.append(action)
    
    ### action 2
    
    
    
    for prompt in prompts:                
        file_name_image = prompt.get("file_name_image", "")
        prompt.pop("file_name_image", None)
    
        action = {}
        action.update(copy.deepcopy(prompt))
        action["command"] = "ai_query"
        action["mode_ai_wait"] = mode_ai_wait
        actions.append(action)
    
        if file_name_image != "":
            action = {}
            #- command: 'save_image'
            action["command"] = "save_image_generated"  
            action["file_name"] = file_name_image
            action["mode_ai_wait"] = mode_ai_wait
            actions.append(action)
            #if image is created use that rather than tag
            file_test = file_name_image

    if file_destination_yaml != "":
        action = {}
        action["text"] = "if the above output is yaml please put it in the reply, if it is not please summarize the above information in a yaml format and only return the yaml without any other text. The yaml should be in the format of a dictionary with keys and values. The keys should be descriptive of the information they contain. The values should be the information itself. Please make sure the yaml is between two &&&tag for copy&&& strings"
        action["command"] = "ai_query"
        action["mode_ai_wait"] = mode_ai_wait
        actions.append(action)
        
        action = {}
        action["command"] = "ai_save_text"
        action["file_name_clip"] = file_destination_yaml.replace(".yaml", "_raw.yaml")
        action["file_name_full"] = file_destination_yaml.replace(".yaml", "_full.txt")
        actions.append(action)
        if action_name == "" or action_name == action_default_name:            
            file_test = file_destination_yaml

        action = {}
        action["command"] = "ai_fix_yaml_copy_paste"
        new_item_name = part2.get("new_item_name", "")
        if new_item_name != "":
            action["new_item_name"] = new_item_name
        remove_top_level = part2.get("remove_top_level", "")
        if remove_top_level != "":
            action["remove_top_level"] = remove_top_level
        search_and_replace = part2.get("search_and_replace", {})
        if search_and_replace != {}:
            action["search_and_replace"] = search_and_replace
        action["file_source"] = file_destination_yaml.replace(".yaml", "_raw.yaml")
        action["file_destination"] = file_destination_yaml
        actions.append(action)

    #close tab
    action = {}
    action["command"] = "close_tab"
    actions.append(action)

    add_action(part=part, action_type=action_type, action_name=action_name, actions=actions, file_test=file_test)  
    return count       

def ai_action_from_folder(**kwargs):
    part = kwargs.get("part", {})
    part2 = kwargs.get("part2", {})
    folder_name = part2.get("folder_name", "")    
    count = kwargs.get("count", 1)    
    
    

    for i in range(1,101):
        file_name = f"{folder_name}\\working_{i}.yaml"
        if os.path.isfile(file_name):
            #load yaml file
            with open(file_name, 'r', encoding='utf-8') as f:
                try:
                    data = yaml.safe_load(f)
                    prompts = data.get("prompts", [])
                    if prompts:
                        count = ai_query_from_prompts(part,prompts,mode_ai_wait, count)
                except Exception as e:
                    print(f"Error reading yaml from {file_name}: {e}")
            part2.update(data)
        else:
            print(f"No file found at {file_name}, stopping folder processing.")
            robo_delay(delay=10)


        ####f string format
        #f string update part_2 variables and all actions in part2
        for key, value in part2.items():
            if isinstance(value, str):
                part2[key] = value.format(**part2)
        #for actions
        actions_working = part2.get("actions", [])
        for action in actions_working:
            for key, value in action.items():
                if isinstance(value, str):
                    try:
                        action[key] = value.format(**part2)
                    except Exception as e:
                        print(f"Error formatting action key {key} with value {value}: {e}")
                        action[key] = ""
                        pass

        actions = part2.get("actions", [])       
        action_name = part2.get("action_name", f"{folder_name}_action")
        action_type = part2.get("action_type", "ai")
        file_test = part2.get("file_test", "tag")
        mode_ai_wait = part2.get("mode_ai_wait", "slow")


        file_test = part2.get("file_test", "tag")
        add_action(part=part, action_type=action_type, action_name=action_name, actions=actions, file_test=file_test)  
        count += 1
        return count  

if __name__ == "__main__":
    cli()


