from __future__ import annotations

import argparse
import ast
import re
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
ACTIONS_DIR = ROOT / "actions"

CORE_PREFIX = ("describe", "define", "_check_key_pressed", "_scroll_lock_toggled")
CORE_SUFFIX = ("action", "old", "test")
CORE_ALL = set(CORE_PREFIX + CORE_SUFFIX)


DEFINE_TEMPLATE = """def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable
"""

CHECK_KEY_STUB = """def _check_key_pressed():
    return None
"""

SCROLL_LOCK_STUB = """def _scroll_lock_toggled():
    return False
"""

ACTION_WRAPPER = """def action(**kwargs):
    return old(**kwargs)
"""

OLD_FALLBACK = """def old(**kwargs):
    return ""
"""

TEST_CANONICAL = """def test(**kwargs):
    try:
        import oomlout_test
    except Exception:
        return callable(old)

    test_fn = getattr(oomlout_test, "test", None)
    if not callable(test_fn):
        return callable(old)

    try:
        return bool(test_fn(**kwargs))
    except Exception:
        return callable(old)
"""

AS_BOOL_HELPER = """def _as_bool(value, default):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    return bool(value)
"""


def _iter_working_files() -> list[Path]:
    files: list[Path] = []
    if not ACTIONS_DIR.is_dir():
        return files
    for item in sorted(ACTIONS_DIR.iterdir(), key=lambda p: p.name):
        path = item / "working.py"
        if item.is_dir() and path.is_file():
            files.append(path)
    return files


def _function_source(lines: list[str], node: ast.FunctionDef) -> str:
    start = node.lineno - 1
    end = node.end_lineno
    return "\n".join(lines[start:end]).rstrip() + "\n"


def _node_source(lines: list[str], node: ast.AST) -> str:
    start = node.lineno - 1
    end = node.end_lineno
    return "\n".join(lines[start:end]).rstrip() + "\n"


def _normalize_blocks(parts: list[str]) -> str:
    kept = [part.strip("\n") for part in parts if part and part.strip()]
    return "\n\n".join(kept).rstrip() + "\n"


def _get_top_nodes_to_preserve(tree: ast.Module) -> list[ast.AST]:
    kept: list[ast.AST] = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Try)):
            kept.append(node)
    return kept


def _load_module(path: Path):
    module_name = f"normalize_{path.parent.name}_{abs(hash(str(path)))}"
    spec = spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _safe_string(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _dedupe_strings(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        token = value.strip()
        if not token:
            continue
        if token in seen:
            continue
        seen.add(token)
        result.append(token)
    return result


def _to_string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _clean_token(value: str, fallback: str) -> str:
    token = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    return token or fallback


def _derive_callable_alias(name: str) -> str:
    remainder = name.removeprefix("roboclick_action_")
    known_prefixes = (
        "google_doc_",
        "save_image_",
        "wait_for_",
        "base_time_",
        "ai_",
        "alias_",
        "browser_",
        "convert_",
        "corel_",
        "file_",
        "image_",
        "openscad_",
        "text_",
        "wait_",
    )
    for prefix in known_prefixes:
        if remainder.startswith(prefix):
            candidate = remainder[len(prefix) :]
            if candidate:
                return _clean_token(candidate, "action")
    return _clean_token(remainder, "action")


def _action_domain_prefix(name: str) -> str:
    remainder = name.removeprefix("roboclick_action_")
    if remainder.startswith("google_doc_"):
        return "google_doc"
    if remainder.startswith("save_image_"):
        return "save_image"
    if remainder.startswith("wait_for_"):
        return "wait_for"
    if "_" in remainder:
        return remainder.split("_", 1)[0]
    return remainder


def _choose_callable_alias(name: str, raw_long_5: str, raw_aliases: list[str]) -> str:
    aliases = _dedupe_strings([_clean_token(alias, "") for alias in raw_aliases if alias.strip()])
    domain_prefix = _action_domain_prefix(name)
    raw_long_5_clean = _clean_token(raw_long_5, "") if raw_long_5 else ""

    filtered = [alias for alias in aliases if alias != "legacy_alias"]

    def select(candidates: list[str], require_underscore: bool, reject_domain_prefix: bool) -> str:
        for candidate in candidates:
            if require_underscore and "_" not in candidate:
                continue
            if reject_domain_prefix and domain_prefix and candidate.startswith(f"{domain_prefix}_"):
                continue
            return candidate
        return ""

    for require_underscore, reject_domain_prefix in (
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ):
        choice = select(filtered, require_underscore, reject_domain_prefix)
        if choice:
            return choice

    if raw_long_5_clean and raw_long_5_clean != "legacy_alias":
        return raw_long_5_clean

    return _derive_callable_alias(name)


def _is_migration_description(description: str) -> bool:
    lowered = description.strip().lower()
    return (
        "self-contained action migrated" in lowered
        or "legacy parameter" in lowered
        or "action logic is implemented directly in old()" in lowered
    )


def _build_action_description(name: str, callable_alias: str, existing_description: str) -> str:
    if existing_description and not _is_migration_description(existing_description):
        cleaned = existing_description.strip()
        plain_words = re.findall(r"[A-Za-z0-9_]+", cleaned)
        if len(plain_words) >= 4:
            if cleaned.endswith("."):
                return cleaned
            return f"{cleaned}."

    phrase = callable_alias.replace("_", " ").strip()
    if not phrase:
        phrase = name.removeprefix("roboclick_action_").replace("_", " ").strip()
    if not phrase:
        phrase = "Run action"
    return f"{phrase[0].upper()}{phrase[1:]}."


def _normalize_variables(raw: Any) -> list[dict]:
    if not isinstance(raw, list):
        return []
    variables: list[dict] = []
    for item in raw:
        if isinstance(item, dict):
            variables.append(item)
            continue
        if isinstance(item, str):
            token = item.strip()
            if token:
                variables.append(
                    {"name": token, "description": "", "type": "string", "default": ""}
                )
    return variables


def _safe_literal(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        return [_safe_literal(item) for item in value]
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            cleaned[str(key)] = _safe_literal(item)
        return cleaned
    return str(value)


def _raw_metadata_from_working(path: Path) -> dict[str, Any]:
    try:
        module = _load_module(path)
    except Exception:
        return {}
    define_fn = getattr(module, "define", None)
    if not callable(define_fn):
        return {}
    try:
        payload = define_fn()
    except Exception:
        return {}
    if isinstance(payload, dict):
        return payload
    return {}


def _fallback_name_tokens(name: str) -> list[str]:
    tokens = [token.strip().lower() for token in name.split("_") if token.strip()]
    if tokens:
        return tokens
    return ["roboclick", "action", "misc", "action"]


def _normalize_metadata(path: Path) -> dict[str, Any]:
    action_name = path.parent.name
    raw = _raw_metadata_from_working(path)

    name = _safe_string(raw.get("name"), action_name) or action_name
    name_tokens = _fallback_name_tokens(name)

    name_long_values: dict[int, str] = {}
    for index in range(1, 5):
        raw_value = _safe_string(raw.get(f"name_long_{index}"), "")
        if raw_value:
            name_long_values[index] = _clean_token(raw_value, f"part_{index}")
        else:
            fallback = name_tokens[index - 1] if index - 1 < len(name_tokens) else f"part_{index}"
            name_long_values[index] = _clean_token(fallback, f"part_{index}")

    raw_name_short: list[str] = []
    raw_name_short.extend(_to_string_list(raw.get("name_short_options")))
    raw_name_short.extend(_to_string_list(raw.get("name_short")))
    raw_name_short.extend(_to_string_list(raw.get("aliases")))
    raw_name_short = _dedupe_strings(raw_name_short)

    raw_long_5 = _safe_string(raw.get("name_long_5"), "")
    callable_alias = _choose_callable_alias(name, raw_long_5, raw_name_short)

    name_long_values[5] = callable_alias

    name_short = [callable_alias]
    name_short.extend(_clean_token(alias, "action") for alias in raw_name_short)
    name_short = _dedupe_strings(name_short)

    description = _build_action_description(
        name=name,
        callable_alias=callable_alias,
        existing_description=_safe_string(raw.get("description"), ""),
    )

    returns = _safe_string(raw.get("returns"), "")
    if not returns:
        returns = (
            'Return "" or None to continue, "exit"/"exit_no_tab" to stop, '
            "or dict to merge into *_manual.yaml."
        )

    category = _safe_string(raw.get("category"), "Other") or "Other"
    variables = _normalize_variables(raw.get("variables"))

    reserved = {
        "name",
        "name_long",
        "name_short",
        "name_short_options",
        "description",
        "returns",
        "category",
        "variables",
        "aliases",
    }
    reserved.update({f"name_long_{index}" for index in range(1, 51)})

    extras: dict[str, Any] = {}
    for key, value in raw.items():
        if key in reserved:
            continue
        extras[str(key)] = _safe_literal(value)

    return {
        "name": name,
        "name_long_values": name_long_values,
        "name_short": name_short,
        "description": description,
        "returns": returns,
        "category": category,
        "variables": variables,
        "extras": extras,
    }


def _build_describe_block(path: Path) -> str:
    metadata = _normalize_metadata(path)

    lines: list[str] = []
    lines.append("def describe():")
    lines.append("    global d")
    lines.append("    d = {}")

    for index in range(1, 6):
        value = metadata["name_long_values"][index]
        lines.append(f"    d[\"name_long_{index}\"] = {repr(value)}")

    lines.append("    d[\"name_long\"] = \"\"")
    lines.append("    for i in range(1, 50):")
    lines.append("        adding = d.get(f\"name_long_{i}\", \"\")")
    lines.append("        if adding != \"\":")
    lines.append("            if d[\"name_long\"]:")
    lines.append("                d[\"name_long\"] += \"_\"")
    lines.append("            d[\"name_long\"] += adding")
    lines.append("    if d[\"name_long\"].endswith(\"_\"):")
    lines.append("        d[\"name_long\"] = d[\"name_long\"][:-1]")

    lines.append(f"    d[\"name\"] = {repr(metadata['name'])}")
    lines.append(f"    d[\"name_long\"] = {repr(metadata['name'])}")
    lines.append(f"    d[\"name_short\"] = {repr(metadata['name_short'])}")
    lines.append(f"    d[\"name_short_options\"] = {repr(metadata['name_short'])}")
    lines.append(f"    d[\"description\"] = {repr(metadata['description'])}")
    lines.append(f"    d[\"returns\"] = {repr(metadata['returns'])}")
    lines.append(f"    d[\"category\"] = {repr(metadata['category'])}")

    lines.append("    v = []")
    lines.append("    if True:")
    if metadata["variables"]:
        for variable in metadata["variables"]:
            lines.append(f"        v.append({repr(variable)})")
    else:
        lines.append("        pass")
    lines.append("    d[\"variables\"] = v")

    for key, value in metadata["extras"].items():
        lines.append(f"    d[{repr(key)}] = {repr(value)}")

    lines.append("    return d")
    return "\n".join(lines) + "\n"


def _build_file_content(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    tree = ast.parse(source)

    function_nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    function_map = {node.name: node for node in function_nodes}
    ordered_function_names = [node.name for node in function_nodes]

    top_blocks = [_node_source(lines, node) for node in _get_top_nodes_to_preserve(tree)]

    describe_src = _build_describe_block(path)
    define_src = DEFINE_TEMPLATE

    if "_check_key_pressed" in function_map:
        check_key_src = _function_source(lines, function_map["_check_key_pressed"])
    else:
        check_key_src = CHECK_KEY_STUB

    if "_scroll_lock_toggled" in function_map:
        scroll_lock_src = _function_source(lines, function_map["_scroll_lock_toggled"])
    else:
        scroll_lock_src = SCROLL_LOCK_STUB

    helper_names = [
        name for name in ordered_function_names if name not in CORE_ALL and name != "_define_original"
    ]
    helper_sources: list[str] = []

    old_source = _function_source(lines, function_map["old"]) if "old" in function_map else OLD_FALLBACK
    helper_name_set = set(helper_names)
    if "_as_bool(" in old_source and "_as_bool" not in helper_name_set:
        helper_sources.append(AS_BOOL_HELPER)
        helper_name_set.add("_as_bool")

    for helper_name in helper_names:
        helper_sources.append(_function_source(lines, function_map[helper_name]))

    if "action" in function_map:
        action_source = _function_source(lines, function_map["action"])
    else:
        action_source = ACTION_WRAPPER

    file_parts: list[str] = []
    file_parts.extend(top_blocks)
    file_parts.append("d = {}")
    file_parts.append(describe_src)
    file_parts.append(define_src)
    file_parts.append(check_key_src)
    file_parts.append(scroll_lock_src)
    file_parts.extend(helper_sources)
    file_parts.append(action_source)
    file_parts.append(old_source)
    file_parts.append(TEST_CANONICAL)
    return _normalize_blocks(file_parts)


def _validate_file(path: Path) -> tuple[bool, str]:
    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except Exception as exc:
        return False, f"parse error: {exc}"

    function_nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    names = [node.name for node in function_nodes]
    if len(names) < 7:
        return False, f"insufficient function count: {len(names)}"
    if tuple(names[:4]) != CORE_PREFIX:
        return False, f"prefix mismatch: {tuple(names[:4])}"
    if tuple(names[-3:]) != CORE_SUFFIX:
        return False, f"suffix mismatch: {tuple(names[-3:])}"
    if "_define_original" in names:
        return False, "contains forbidden helper _define_original"

    describe_node = function_nodes[0]
    if not isinstance(describe_node, ast.FunctionDef) or describe_node.name != "describe":
        return False, "describe function missing"

    required_keys = {"name", "name_long_5", "name_short", "description", "variables"}
    assigned_keys: set[str] = set()
    for node in ast.walk(describe_node):
        if not isinstance(node, ast.Assign):
            continue
        if not node.targets:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Subscript):
            continue
        if not isinstance(target.value, ast.Name) or target.value.id != "d":
            continue
        key = None
        if isinstance(target.slice, ast.Constant) and isinstance(target.slice.value, str):
            key = target.slice.value
        if key:
            assigned_keys.add(key)
    if not required_keys.issubset(assigned_keys):
        missing = sorted(required_keys - assigned_keys)
        return False, f"describe missing keys: {missing}"

    try:
        module = _load_module(path)
        define_fn = getattr(module, "define", None)
        if not callable(define_fn):
            return False, "define not callable"
        payload = define_fn()
        if not isinstance(payload, dict) or not payload:
            return False, "define returned empty or non-dict metadata"
        name_short = payload.get("name_short", [])
        if isinstance(name_short, str):
            name_short = [name_short]
        if not isinstance(name_short, list):
            return False, "name_short is not list/string"
        name_short = [item for item in name_short if isinstance(item, str)]
        if len(name_short) != len(set(name_short)):
            return False, "name_short contains duplicates"
        name_long_5 = payload.get("name_long_5", "")
        if not isinstance(name_long_5, str) or not name_long_5:
            return False, "missing name_long_5"
        if name_long_5 not in name_short:
            return False, "name_long_5 not callable in name_short"
    except Exception as exc:
        return False, f"define runtime validation failed: {exc}"

    return True, "ok"


def run(check_only: bool = False) -> int:
    files = _iter_working_files()
    changed: list[str] = []
    invalid: list[str] = []

    for path in files:
        new_content = _build_file_content(path)
        old_content = path.read_text(encoding="utf-8")
        if new_content != old_content:
            if not check_only:
                path.write_text(new_content, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))

    for path in files:
        ok, reason = _validate_file(path)
        if not ok:
            invalid.append(f"{path.relative_to(ROOT)} -> {reason}")

    if check_only:
        print(f"Checked: {len(files)} files")
    else:
        print(f"Processed: {len(files)} files")
    print(f"Changed: {len(changed)}")
    for item in changed:
        print(f"  - {item}")
    print(f"Invalid: {len(invalid)}")
    for item in invalid:
        print(f"  - {item}")

    return 1 if invalid else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return run(check_only=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
