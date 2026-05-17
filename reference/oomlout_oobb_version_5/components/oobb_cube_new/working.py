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
    d["name"] = 'oobb_cube_new'
    d["name_long"] = 'OOBB Geometry Primitives: Cube New'
    d["description"] = 'Cube with full rotation-object support and mode filtering.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['cube_new']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'size', "description": '[x,y,z] dimensions in mm.', "type": 'list', "default": '(required)'})
    v.append({"name": 'zz', "description": 'Z anchor point: bottom, top, center/middle.', "type": 'string', "default": '"bottom"'})
    v.append({"name": 'mode', "description": 'Render modes: laser, 3dpr, true.', "type": 'list', "default": '["laser","3dpr","true"]'})
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
    import oobb
    import opsc
    """Geometry component."""
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    depth = kwargs.get("depth", 100)
    zz = kwargs.get("zz", "bottom")
    radius_name = kwargs.get("radius_name", "")
    radius = kwargs.get("radius", 0)

    # setting up for rotation object
    typ = kwargs.get("type", "p")
    kwargs["type"] = "positive" #needs to be positive for the difference to work
    rot_original = get_rot(**kwargs)       
    kwargs.pop("rot", None)
    kwargs.pop("rot_x", None)
    kwargs.pop("rot_y", None)
    kwargs.pop("rot_z", None)
    rot_shift_original = copy.deepcopy(kwargs.get("rot_shift", None))
    kwargs.pop("rot_shift", None)

    # storing pos and popping it out to add it in rotation element     
    pos_original = copy.deepcopy(copy.deepcopy(kwargs.get("pos", [0, 0, 0])))
    pos_original_original = copy.deepcopy(pos_original)
    kwargs.pop("pos", None)
    pos = [0,0,0]
    kwargs["pos"] = pos


    return_value = []
    p3 = copy.deepcopy(kwargs)
    zz = kwargs.get("zz", "bottom")

    p3["shape"] = "cube"
    pos1 = copy.deepcopy(p3["pos"])
    pos1[0] = pos1[0] - p3["size"][0]/2
    pos1[1] = pos1[1] - p3["size"][1]/2
    if zz == "center" or zz == "middle":
        pos1[2] = pos1[2] - p3["size"][2]/2
    elif zz == "top":
        pos1[2] = pos1[2] - p3["size"][2]
    elif zz == "bottom":
        pos1[2] = pos1[2]

    p3["pos"] = pos1
    return_value.append(opsc.opsc_easy(**p3))


    #components_second = copy.deepcopy(thing["components"])

    #put into a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    pos1 = copy.deepcopy(pos)
    #pos1[0] += 50
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    if rot_shift_original != None:
        return_value_2["rot_shift"] = rot_shift_original
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
      'preview_rot': [35, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'size': [24, 18, 12],
                 'zz': 'middle',
                 'mode': 'true',
                 'rot': [25, 20, 10]}},
     {'filename': 'test_2',
      'preview_rot': [35, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'size': [30, 20, 10],
                 'zz': 'middle',
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


