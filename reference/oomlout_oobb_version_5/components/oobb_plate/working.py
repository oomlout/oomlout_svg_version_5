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
    d["name"] = 'oobb_plate'
    d["name_long"] = 'OOBB Geometry Primitives: Plate'
    d["description"] = 'OOBB grid-sized plate (cylinder for 1Ã—1, rounded rectangle otherwise) with optional hole pattern.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['plate']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'width', "description": 'Width in OOBB grid units.', "type": 'number', "default": 1})
    v.append({"name": 'height', "description": 'Height in OOBB grid units.', "type": 'number', "default": 1})
    v.append({"name": 'depth', "description": 'Plate thickness in mm.', "type": 'number', "default": 3})
    v.append({"name": 'zz', "description": 'Z anchor: bottom, top, middle.', "type": 'string', "default": '"bottom"'})
    v.append({"name": 'extra_mm', "description": 'Adds 1/15 to size for clearance fit.', "type": 'bool', "default": False})
    v.append({"name": 'holes', "description": 'Include OOBB hole pattern.', "type": 'bool', "default": False})
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
    kwargs = copy.deepcopy(kwargs)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    extra_mm = kwargs.get("extra_mm", False)
    depth_mm = kwargs.get("depth", 3)
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    zz = kwargs.get("zz", "bottom")
    holes = kwargs.get("holes", False)
    include = kwargs.get("include", "")

    return_value = []

    if zz == "top":
        pos[2] += -depth_mm
    elif zz == "middle":
        pos[2] += -depth_mm/2
    else:
        pos[2] += 0
    kwargs["pos"] = pos


    #add extra_mm
    if extra_mm:
        width = width + 1/15 
        height = height + 1/15

    width_mm = width * oobb.gv("osp") - oobb.gv("osp_minus")
    height_mm = height * oobb.gv("osp") - oobb.gv("osp_minus")



    # if 1 x 1 than just cylinder
    if width == 1 and height == 1:

        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "cylinder"
        p3["r"] = (width * oobb.gv("osp") - oobb.gv("osp_minus"))/2
        p3["h"] = depth_mm
        return_value.append(opsc.opsc_easy(**p3))

    else:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "rounded_rectangle"
        p3["width_mm"] = width_mm
        p3["height_mm"] = height_mm
        p3["size"] = [ width_mm, height_mm, depth_mm]
        omit_corner = p3.get("omit_corner", "")
        if omit_corner != "":
            p3["omit_corner"] = omit_corner
        return_value.append(opsc.opsc_easy(**p3))


    if holes or "hole" in include:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_holes"
        p3["both_holes"] = True  
        p3.pop("holes", None)
        rot = p3.get("rot", [0, 0, 0])
        if rot[2] == 90:   #if rotated 90 degrees do the hole swap
            wid = p3["width"]
            hei = p3["height"]
            p3["width"] = hei
            p3["height"] = wid
        return_value.extend(oobb.oobb_easy(**p3))

    return return_value

    #screw


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
                 'width': 3,
                 'height': 2,
                 'depth': 3,
                 'zz': 'bottom',
                 'holes': False}},
     {'filename': 'test_2',
      'preview_rot': [55, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'width': 3, 'height': 2, 'depth': 3, 'zz': 'bottom', 'holes': True}}]

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


