import copy
import ntpath
import os
import re
import shutil
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

d = {}


def describe():
    global d
    d = {}
    d["name"] = "raw_scad"
    d["name_long"] = "OPSC Composite Shapes: Raw SCAD"
    d["description"] = "Imports or inlines raw OpenSCAD modules through the component system."
    d["category"] = "OPSC Composite Shapes"
    d["shape_aliases"] = ["raw_scad"]
    d["returns"] = "List of geometry component dicts."
    d["variables"] = []
    return d


def define():
    global d
    if not d:
        describe()
    defined = {}
    defined.update(d)
    return defined


def action(**kwargs):
    import opsc

    params = copy.deepcopy(kwargs)
    params.setdefault("type", "positive")
    params["shape"] = "raw_scad"
    return [opsc.opsc_easy(**params)]


def _write_raw_scad_source(source, module_name, cache_dir=None):
    import hashlib

    if cache_dir is not None:
        cache_root = _get_reference_dir(cache_dir)
    else:
        cache_root = os.path.join(_PROJECT_ROOT, "_raw_scad_cache")
    os.makedirs(cache_root, exist_ok=True)

    if cache_dir is not None:
        filename = os.path.join(cache_root, f"{module_name}.scad")
    else:
        digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]
        filename = os.path.join(cache_root, f"{module_name}_{digest}.scad")

    with open(filename, "w", encoding="utf-8") as handle:
        handle.write(source)

    return filename


def _get_reference_dir(cache_dir):
    return os.path.join(os.path.dirname(os.path.abspath(cache_dir)), "scad_reference")


def _is_absolute_scad_path(path):
    return (
        os.path.isabs(path)
        or ntpath.isabs(path)
        or re.match(r"^[A-Za-z]:[\\/]", path) is not None
    )


def _path_key(path):
    return os.path.normcase(os.path.abspath(path))


def _resolve_include_path(target, base_dir):
    if _is_absolute_scad_path(target):
        candidate = ntpath.abspath(target) if "\\" in target else os.path.abspath(target)
    else:
        candidate = os.path.abspath(os.path.join(base_dir, target.replace("/", os.sep)))

    if os.path.isfile(candidate):
        return candidate

    target_parts = [part for part in re.split(r"[\\/]+", target) if part]
    if target_parts and target_parts[0] == "git":
        project_git_candidate = os.path.join(_PROJECT_ROOT, *target_parts)
        if os.path.isfile(project_git_candidate):
            return project_git_candidate

        git_candidate = os.path.join(
            _PROJECT_ROOT,
            "components",
            "github_belfryscad_bosl2_screw",
            *target_parts,
        )
        if os.path.isfile(git_candidate):
            return git_candidate

    return None


def _is_path_inside(path, root):
    try:
        return os.path.commonpath([os.path.abspath(path), os.path.abspath(root)]) == os.path.abspath(root)
    except ValueError:
        return False


def _safe_external_relative_path(source_abs):
    drive, tail = ntpath.splitdrive(source_abs)
    drive_name = drive.rstrip(":").lower() or "local"
    raw_parts = [part for part in re.split(r"[\\/]+", tail.lstrip("\\/")) if part]
    safe_parts = [re.sub(r"[^A-Za-z0-9_.-]", "_", part) for part in raw_parts]
    return os.path.join("external", drive_name, *safe_parts)


def _reference_destination_path(source_abs, reference_dir):
    if _is_path_inside(source_abs, reference_dir):
        return source_abs

    source_parts = [part for part in re.split(r"[\\/]+", os.path.abspath(source_abs)) if part]
    if "git" in source_parts:
        git_index = source_parts.index("git")
        relative_path = os.path.join(*source_parts[git_index:])
        return os.path.join(reference_dir, relative_path)

    if _is_path_inside(source_abs, _PROJECT_ROOT):
        relative_path = os.path.relpath(source_abs, _PROJECT_ROOT)
    else:
        relative_path = _safe_external_relative_path(source_abs)

    return os.path.join(reference_dir, relative_path)


def _copy_reference_tree(source_path, reference_dir, copied=None):
    if copied is None:
        copied = {}

    source_abs = os.path.abspath(source_path)
    source_key = _path_key(source_abs)
    if source_key in copied:
        return copied[source_key]

    destination = _reference_destination_path(source_abs, reference_dir)
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    if _path_key(source_abs) != _path_key(destination):
        shutil.copyfile(source_abs, destination)
    copied[source_key] = destination

    include_re = re.compile(r"(use|include)[ \t]+<([^>]+)>[ \t]*;?")
    source_dir = os.path.dirname(source_abs)
    destination_dir = os.path.dirname(destination)

    try:
        with open(destination, "r", encoding="utf-8") as handle:
            content = handle.read()
    except UnicodeDecodeError:
        return destination

    def replace_include(match):
        directive = match.group(1)
        target = match.group(2).strip()
        included_source = _resolve_include_path(target, source_dir)
        if included_source is None:
            return f"{directive} <{target}>;"

        included_destination = _copy_reference_tree(
            included_source,
            reference_dir,
            copied=copied,
        )
        relative_target = os.path.relpath(included_destination, destination_dir).replace("\\", "/")
        return f"{directive} <{relative_target}>;"

    updated = include_re.sub(replace_include, content)
    if updated != content:
        with open(destination, "w", encoding="utf-8") as handle:
            handle.write(updated)

    return destination


def _bundle_raw_scad_references(filename, cache_dir):
    if cache_dir is None:
        return filename

    reference_dir = _get_reference_dir(cache_dir)
    os.makedirs(reference_dir, exist_ok=True)
    return _copy_reference_tree(filename, reference_dir)


def render(params):
    from solid2 import import_scad

    source = params.get("source", "")
    filename = params.get("file", "")
    module_name = params.get("module", "main")
    module_kwargs = params.get("module_kwargs", {})
    cache_dir = params.get("cache_dir", None)

    if source:
        filename = _write_raw_scad_source(source, module_name, cache_dir=cache_dir)
    if not filename:
        raise ValueError("raw_scad requires either 'source' or 'file'.")
    filename = _bundle_raw_scad_references(filename, cache_dir)

    scad_object = import_scad(filename)
    module_fn = getattr(scad_object, module_name, None)
    if module_fn is None:
        raise ValueError(f"raw_scad module '{module_name}' not found in {filename}")

    result = module_fn(**module_kwargs)
    if cache_dir is not None:
        include_path = os.path.relpath(filename, cache_dir).replace("\\", "/")
        result.include_file_path = include_path
        result.include_string = f"use <{include_path}>;\n"
    return result


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [35, 0, 25],
      'kwargs': {'type': 'positive',
                 'source': 'module main(){cube([12,12,12], center=true);}',
                 'module': 'main',
                 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [35, 0, 25],
      'kwargs': {'type': 'positive',
                 'source': 'module main(){difference(){cube([20,12,6], center=true); '
                           'translate([0,0,0]) cube([10,6,8], center=true);}}',
                 'module': 'main',
                 'pos': [0, 0, 0]}}]

    generated_files = []

    for sample in samples:
        kwargs = copy.deepcopy(sample["kwargs"])
        result = action(**kwargs)
        if isinstance(result, dict) and "components" in result:
            components = copy.deepcopy(result["components"])
        elif isinstance(result, list):
            components = result
        else:
            components = [result]

        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        png_path = os.path.join(sample_dir, "image.png")

        opsc.opsc_make_object(
            scad_path,
            components,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_preview_images(scad_path, sample_dir)
        generated_files.append(png_path)

    return generated_files


