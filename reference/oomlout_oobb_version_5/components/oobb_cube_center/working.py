import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_cube_center'
    d["name_long"] = 'OOBB Geometry Primitives: Cube Center'
    d["description"] = 'Center-aligned cube that shifts pos by -size/2 on x/y before passing to OpenSCAD.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['cube_center']
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
    import oobb
    """Center-aligned cube geometry primitive."""
    p3 = copy.deepcopy(kwargs)
    zz = kwargs.get("zz", "bottom")
    
    #if size doesn't exist build it from width height and depth
    if "size" not in kwargs:
        width = kwargs.get("width", 1)
        height = kwargs.get("height", 1)
        depth = kwargs.get("depth", 1)
        p3["size"] = [width, height, depth]

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
    return oobb.oobb_easy(**p3)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [35, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'size': [24, 24, 12], 'zz': 'middle'}},
     {'filename': 'test_2',
      'preview_rot': [35, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'size': [18, 18, 24], 'zz': 'middle'}}]

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


