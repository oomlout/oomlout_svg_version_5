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
    d["name"] = 'oobb_rounded_rectangle_hollow'
    d["name_long"] = 'OOBB Geometry Primitives: Hollow Rounded Rectangle'
    d["description"] = 'Hollow rounded rectangle (positive outer minus negative inner wall) wrapped in a rotation object.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['rounded_rectangle_hollow']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'size', "description": 'Outer [x,y,z] dimensions in mm.', "type": 'list', "default": '(required)'})
    v.append({"name": 'radius', "description": 'Corner radius of outer shape.', "type": 'number', "default": '(required)'})
    v.append({"name": 'wall_thickness', "description": 'Wall thickness from outer to inner.', "type": 'number', "default": 2})
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
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
    extra = kwargs.get("extra", "")
    wall_thickness = kwargs.get("wall_thickness", 2)
    if extra == "interior":
        return_value = []
        #negative_cylinder
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "rounded_rectangle"
        if "size" in p3:
            size1 = copy.deepcopy(p3["size"])
            size1[0] = size1[0] - wall_thickness * 2
            size1[1] = size1[1] - wall_thickness * 2
            p3["size"] = size1
        else:
            p3["width"] += - wall_thickness * 2
            p3["height"] += - wall_thickness * 2
        if "radius" in p3:
            rad = p3.get("radius")
            rad = rad - wall_thickness
            p3["radius"] = rad
        elif "r1" in p3:
            rad1 = p3.get("r1")
            rad1 += - wall_thickness
            p3["r1"] = rad1
            rad2 = p3.get("r2")
            rad2 += - wall_thickness
            p3["r2"] = rad2
            p3.pop("r", None)
        else:
            rad = 5
        return_value.append(opsc.opsc_easy(**p3))
        return return_value
    else:

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



        #positive_rounded_rectangle
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "rounded_rectangle"
        p3["type"] = "positive"
        return_value.append(opsc.opsc_easy(**p3))

        #negative_cylinder
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "rounded_rectangle"
        p3["type"] = "negative"
        if "size" in p3:
            size1 = copy.deepcopy(p3["size"])
            size1[0] = size1[0] - wall_thickness * 2
            size1[1] = size1[1] - wall_thickness * 2
            p3["size"] = size1
        else:
            p3["width"] += - wall_thickness * 2
            p3["height"] += - wall_thickness * 2
        if "radius" in p3:
            rad = p3.get("radius")
            rad = rad - wall_thickness
            p3["radius"] = rad
        elif "r1" in p3:
            rad1 = p3.get("r1")
            rad1 += - wall_thickness
            p3["r1"] = rad1
            rad2 = p3.get("r2")
            rad2 += - wall_thickness
            p3["r2"] = rad2
            p3.pop("r", None)
        else:
            rad = 5

        #pos = copy.deepcopy(p3.get("pos", [0, 0, 0]))
        #pos[2] += 50
        #p3["pos"] = pos


        #p3["m"] = "#"
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
                 'size': [30, 20, 8],
                 'radius': 5,
                 'wall_thickness': 2,
                 'extra': '',
                 'rot': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [55, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'size': [36, 24, 8],
                 'radius': 6,
                 'wall_thickness': 1.2,
                 'extra': '',
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


