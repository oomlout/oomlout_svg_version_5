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

_rot_mod = _load_component("oobb_rot")
get_rot = _rot_mod.action

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_cylinder_hollow'
    d["name_long"] = 'OOBB Geometry Primitives: Hollow Cylinder'
    d["description"] = 'Hollow cylinder (positive outer minus negative inner) wrapped in a rotation object.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['cylinder_hollow']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'r', "description": 'Outer radius in mm.', "type": 'number', "default": '(required)'})
    v.append({"name": 'wall_thickness', "description": 'Wall thickness for inner cylinder.', "type": 'number', "default": 2})
    v.append({"name": 'depth', "description": 'Cylinder height in mm.', "type": 'number', "default": '(required)'})
    v.append({"name": 'rot', "description": 'Rotation [rx,ry,rz] in degrees.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'rot_x', "description": 'X rotation in degrees.', "type": 'number', "default": 0})
    v.append({"name": 'rot_y', "description": 'Y rotation in degrees.', "type": 'number', "default": 0})
    v.append({"name": 'rot_z', "description": 'Z rotation in degrees.', "type": 'number', "default": 0})
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
    import opsc
    """Geometry component."""
    # setting up for rotation object
    typ = kwargs.get("type", "p")
    kwargs["type"] = "positive" #needs to be positive for the difference to work
    rot_original = get_rot(**kwargs)   
    kwargs.pop("rot", None)
    kwargs.pop("rot_x", None)
    kwargs.pop("rot_y", None)
    kwargs.pop("rot_z", None)

    # storing pos and popping it out to add it in rotation element     
    pos_original = copy.deepcopy(copy.deepcopy(kwargs.get("pos", [0, 0, 0])))
    pos_original_original = copy.deepcopy(pos_original)
    kwargs.pop("pos", None)
    pos = [0,0,0]
    kwargs["pos"] = pos

    return_value = []

    wall_thickness = kwargs.get("wall_thickness", 2)

    depth = kwargs.get("depth", None)
    if depth != None:
        kwargs["h"] = depth

    if "radius" in kwargs:
        kwargs["r"] = kwargs["radius"]
        kwargs.pop("radius", None)

    #positive_cylinder
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "cylinder"
    p3["type"] = "positive"
    return_value.append(opsc.opsc_easy(**p3))

    #negative_cylinder
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "cylinder"
    p3["type"] = "negative"
    if "r1" in p3:
        p3["r1"] = p3["r1"] - wall_thickness
        p3["r2"] = p3["r2"] - wall_thickness
    else:
        p3["r"] = p3["r"] - wall_thickness
    return_value.append(opsc.opsc_easy(**p3))

    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]

    return return_value_2


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [55, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'r': 10,
                 'wall_thickness': 2,
                 'depth': 12,
                 'rot': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [55, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'r': 12,
                 'wall_thickness': 1.2,
                 'depth': 18,
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


