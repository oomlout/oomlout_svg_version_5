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
    d["name"] = 'oobb_slice'
    d["name_long"] = 'OOBB Geometry Primitives: Slice'
    d["description"] = 'Large cube slice used to clip/intersect geometry.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['slice']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'size', "description": '[x,y,z] dimensions of the slice cube in mm.', "type": 'list', "default": '[500,500,500]'})
    v.append({"name": 'zz', "description": 'Z anchor: bottom or top.', "type": 'string', "default": '"bottom"'})
    v.append({"name": 'mode', "description": 'Render modes: laser, 3dpr, true.', "type": 'list', "default": '["laser","3dpr","true"]'})
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
    p3 = copy.deepcopy(kwargs)

    modes = p3.get("mode", ["laser", "3dpr", "true"])
    pos = copy.deepcopy(p3.get("pos", [0, 0, 0]))
    size = copy.deepcopy(p3.get("size", [500, 500, 500]))
    p3["pos"] = pos
    zz = p3.get("zz", "bottom")

    return_value = []


    if pos[0] == 0 and pos[1] == 0:
        pos = [-size[0]/2,-size[1]/2,pos[2]]
        p3["pos"] = pos

    if modes == "all":
        modes = ["laser", "3dpr", "true"]

    if type(modes) == str:
        modes = [modes]

    shift = -size[2]
    p4 = copy.deepcopy(p3)
    for mode in modes:
        p3 = copy.deepcopy(p4)        
        p3["shape"] = "cube"
        p3["size"] = copy.deepcopy(size)

        #shift 250
        if zz == "bottom":
            p3["pos"][2] += 0
        elif zz == "top":
            p3["pos"][2] += shift
        kwargs.update({"inclusion": mode})
        #p3["m"] = "#"
        return_value.append(opsc.opsc_easy(**p3))
    return return_value

    # hole


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [60, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'size': [30, 30, 6], 'zz': 'bottom', 'mode': 'true'}},
     {'filename': 'test_2',
      'preview_rot': [60, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'size': [30, 30, 6], 'zz': 'top', 'mode': 'true'}}]

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


