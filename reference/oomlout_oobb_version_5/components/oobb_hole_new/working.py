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
    d["name"] = 'oobb_hole_new'
    d["name_long"] = 'OOBB Geometry Primitives: Hole'
    d["description"] = 'Cylindrical hole with rotation-object support, mode filtering, and named/explicit radius.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['hole_new']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'depth', "description": 'Hole depth in mm.', "type": 'number', "default": 100})
    v.append({"name": 'radius_name', "description": 'Named radius for mode-aware lookup.', "type": 'string', "default": '""'})
    v.append({"name": 'radius', "description": 'Explicit radius in mm.', "type": 'number', "default": 0})
    v.append({"name": 'zz', "description": 'Z anchor: bottom, top, middle.', "type": 'string', "default": '"middle"'})
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
    default_zz = "bottom"
    if depth == 100:
        default_zz = "middle"
    zz = kwargs.get("zz", default_zz)
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

    # storing pos and popping it out to add it in rotation element     
    pos_original = copy.deepcopy(copy.deepcopy(kwargs.get("pos", [0, 0, 0])))
    pos_original_original = copy.deepcopy(pos_original)
    kwargs.pop("pos", None)
    pos = [0,0,0]


    # modes
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]

    # zz
    pos1 = copy.deepcopy(pos)
    if zz == "bottom":
        pos1[2] += 0
    elif zz == "top":
        pos1[2] += -depth
    elif zz == "middle":
        pos1[2] += -depth/2
    kwargs["pos"] = pos1

    return_value = []
    for mode in modes:
        p3 = copy.deepcopy(kwargs)
        p3["inclusion"] = mode
        p3["shape"] = "cylinder"
        # radius
        if radius_name != "":
            r = ob.gv("hole_radius_"+radius_name, mode)
        else:
            r = radius
        p3["r"] = r
        p3["h"] = depth
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


    # motor

    #      motor_servo_standard_01


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [60, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'depth': 12,
                 'radius_name': 'm3',
                 'zz': 'middle',
                 'mode': 'true',
                 'rot': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [60, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'depth': 16,
                 'radius': 4,
                 'zz': 'middle',
                 'mode': 'true',
                 'rot': [90, 0, 0]}}]

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


