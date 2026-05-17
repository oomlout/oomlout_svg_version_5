import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


# ---------- cross-component helper imports ----------
import importlib.util
def _load_component(folder_name):
    path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
    spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_screw_mod = _load_component("oobb_screw")
get_oobb_screw = _screw_mod.action

d = {}


def _get_parent_variables():
    screw_description = copy.deepcopy(_screw_mod.describe())
    return [
        variable for variable in screw_description.get("variables", [])
        if variable.get("name") != "style"
    ]


def describe():
    global d
    d = {}
    d["name"] = 'oobb_screw_socket_cap'
    d["name_long"] = 'OOBB Geometry Primitives: Socket Cap Screw'
    d["description"] = "Socket-cap screw cutout; wrapper over oobb_screw with style='socket_cap' pre-set."
    d["category"] = 'Fasteners'
    d["shape_aliases"] = ['screw_socket_cap']
    d["returns"] = 'List of geometry component dicts.'
    d["variables"] = _get_parent_variables()
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable
def action(**kwargs):
    """Socket cap screw â€” delegates to oobb_screw with style pre-set."""
    kwargs["style"] = "socket_cap"
    return get_oobb_screw(**kwargs)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [
        {'filename': 'test_1',
         'preview_rot': [70, 0, 20],
         'kwargs': {'pos': [0, 0, 0],
                    'type': 'positive',
                    'radius_name': 'm3',
                    'depth': 16,
                    'zz': 'none',
                    'hole': True,
                    'clearance': '',
                    'nut_include': False,
                    'overhang': False,
                    'slot': 0,
                    'mode': 'true',
                    'rot': [0, 0, 0]}},
        {'filename': 'test_2',
         'preview_rot': [70, 0, 20],
         'kwargs': {'pos': [0, 0, 0],
                    'type': 'positive',
                    'radius_name': 'm6',
                    'depth': 22,
                    'zz': 'bottom',
                    'hole': True,
                    'clearance': 'top',
                    'nut_include': True,
                    'overhang': True,
                    'slot': 0,
                    'mode': 'true',
                    'rot': [0, 0, 0]}},
        {'filename': 'test_3',
         'preview_rot': [70, 0, 20],
         'kwargs': {'pos': [0, 0, 0],
                    'type': 'positive',
                    'radius_name': 'm3',
                    'depth': 18,
                    'zz': 'top',
                    'hole': False,
                    'clearance': '',
                    'nut_include': False,
                    'overhang': False,
                    'slot': 14,
                    'mode': 'true',
                    'rot': [0, 0, 0]}}]

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


