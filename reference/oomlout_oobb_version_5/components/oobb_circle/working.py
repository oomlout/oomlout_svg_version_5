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
    d["name"] = 'oobb_circle'
    d["name_long"] = 'OOBB Geometry Primitives: Circle'
    d["description"] = 'Renders a cylinder (solid or cutout) sized to an OOBB grid position.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['circle']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'width', "description": 'Width in OOBB grid units.', "type": 'number', "default": 1})
    v.append({"name": 'height', "description": 'Height in OOBB grid units.', "type": 'number', "default": 1})
    v.append({"name": 'depth', "description": 'Z depth (height) of the cylinder in mm.', "type": 'number', "default": 3})
    v.append({"name": 'extra_mm', "description": 'Adds 1/15 to width/height for clearance fit.', "type": 'bool', "default": False})
    v.append({"name": 'zz', "description": 'Z anchor point: bottom, top, middle.', "type": 'string', "default": '"bottom"'})
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
    """Circle geometry â€” cylinder cutout or solid at OOBB grid position."""
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    extra_mm = kwargs.get("extra_mm", False)
    pos = kwargs.get("pos", [0, 0, 0])
    depth = kwargs.get("depth", 3)
    zz = kwargs.get("zz", "bottom")

    
    #add extra_mm
    if extra_mm:
        width = width + 1/15 
        height = height + 1/15
    
    #zz 
    if zz == "bottom":
        pos[2] += 0
    elif zz == "top":
        pos[2] += -depth
    elif zz == "middle":
        pos[2] += -depth/2

    width_mm = width * oobb.gv("osp") - oobb.gv("osp_minus")
    height_mm = height * oobb.gv("osp") - oobb.gv("osp_minus")
    


       
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "cylinder"
    p3["r"] = (width * oobb.gv("osp") - oobb.gv("osp_minus"))/2
    p3["h"] = depth
    return [opsc.opsc_easy(**p3)]


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [60, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'width': 3, 'height': 3, 'depth': 3, 'zz': 'bottom'}},
     {'filename': 'test_2',
      'preview_rot': [60, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'width': 5,
                 'height': 5,
                 'depth': 3,
                 'extra_mm': True,
                 'zz': 'bottom'}}]

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


