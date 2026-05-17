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
    d["name"] = 'oobb_slot'
    d["name_long"] = 'OOBB Geometry Primitives: Slot'
    d["description"] = 'Slot (two-ended rounded cutout) with rotation-object support, mode filtering, and named/explicit radius.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['slot']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'depth', "description": 'Slot depth in mm.', "type": 'number', "default": 250})
    v.append({"name": 'radius', "description": 'Slot end-cap radius in mm.', "type": 'number', "default": '""'})
    v.append({"name": 'radius_name', "description": 'Named radius for mode-aware lookup.', "type": 'string', "default": '""'})
    v.append({"name": 'zz', "description": 'Z anchor: middle, bottom, top.', "type": 'string', "default": '"middle"'})
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
    depth = kwargs.get("depth", "")
    pos = kwargs.get("pos", [0, 0, 0])
    pos = copy.deepcopy(pos)
    zz = kwargs.get("zz", "middle")
    radius = kwargs.get("radius", "")
    radius_name = kwargs.get("radius_name", "")
    radius_1 = kwargs.get("radius_1", "")
    radius_2 = kwargs.get("radius_2", "")


    #      mode sorting
    if modes == "all":
        modes = ["laser", "3dpr", "true"]    
    if type(modes) != list:
        modes = [modes]

    #      depth sorting
    if depth == "":
            depth = 250
            pos[2] = pos[2] - depth / 2

    #      zz sorting
    if zz == "middle":
        pos[2] = pos[2] - depth / 2
        kwargs["pos"] = pos
    elif zz == "bottom":
        pos[2] = pos[2] - depth
        kwargs["pos"] = pos
    elif zz == "top":
        pass



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


    return_value = []
    p3 = copy.deepcopy(kwargs)
    for mode in modes:
        if radius_name != "":
            radius = ob.gv("hole_radius_"+radius_name, mode)
        p3["shape"] = "slot"
        if radius_1 == "":        
            p3["r"] = radius
        else:
            p3["r1"] = radius_1
            p3["r2"] = radius_2
        p3["h"] = depth
        p3.update({"inclusion": mode})
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

    #tube


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
                 'radius': 3,
                 'zz': 'middle',
                 'mode': 'true',
                 'rot': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [60, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'depth': 12,
                 'radius': 3,
                 'zz': 'middle',
                 'mode': 'true',
                 'rot': [0, 0, 90]}}]

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


