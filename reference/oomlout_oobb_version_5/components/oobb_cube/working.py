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

_cube_center_mod = _load_component("oobb_cube_center")
get_oobb_cube_center = _cube_center_mod.action

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_cube'
    d["name_long"] = 'OOBB Geometry Primitives: Cube'
    d["description"] = 'Cube geometry primitive; delegates to oobb_cube_center.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['oobb_cube']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'size', "description": '[x,y,z] dimensions in mm.', "type": 'list', "default": '(required)'})
    v.append({"name": 'zz', "description": 'Z anchor point: bottom, top, center/middle.', "type": 'string', "default": '"bottom"'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable
def action(**kwargs):
    """Cube geometry â€” delegates to oobb_cube_center."""
    return get_oobb_cube_center(**kwargs)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [35, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'size': [24, 24, 12], 'zz': 'bottom'}},
     {'filename': 'test_2',
      'preview_rot': [35, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'size': [36, 18, 8], 'zz': 'middle'}}]

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


