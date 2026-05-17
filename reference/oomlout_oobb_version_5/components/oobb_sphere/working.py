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
    d["name"] = 'oobb_sphere'
    d["name_long"] = 'OOBB Geometry Primitives: Sphere'
    d["description"] = 'Sphere (optionally ellipsoidal via radius_1/radius_2 scale) with z-anchor support.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['sphere']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'radius', "description": 'Sphere radius in mm.', "type": 'number', "default": 10})
    v.append({"name": 'radius_1', "description": 'Base radius for ellipsoid scaling.', "type": 'number', "default": '(optional)'})
    v.append({"name": 'radius_2', "description": 'Z-scale radius for ellipsoid.', "type": 'number', "default": '(optional)'})
    v.append({"name": 'zz', "description": 'Z anchor: bottom, top, middle.', "type": 'string', "default": '"bottom"'})
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
    radius_1 = kwargs.get("radius_1", None)
    if radius_1 != None:
        radius = radius_1
    else:
        radius = kwargs.get("radius", 10)    
    radius_2 = kwargs.get("radius_2", None)
    if radius_2 == None:
        radius_2 = radius    
    pos = kwargs.get("pos", [0, 0, 0])
    zz = kwargs.get("zz", "bottom")
    depth = radius_1 * 2
    #zz 
    if zz == "bottom":
        pos[2] += 0
    elif zz == "top":
        pos[2] += -depth
    elif zz == "middle":
        pos[2] += -depth/2

    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "sphere"
    p3["r"] = radius
    sc = (radius_2 / radius_1) * 2
    return_value = ([opsc.opsc_easy(**p3)])
    return_value[0]["scale"] = [1,1,sc]
    return return_value


    # cylinder


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [35, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'radius': 10, 'zz': 'middle'}},
     {'filename': 'test_2',
      'preview_rot': [35, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'radius_1': 8, 'radius_2': 12, 'zz': 'middle'}}]

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


