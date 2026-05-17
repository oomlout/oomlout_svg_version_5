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
    d["name"] = 'oobb_tube_new'
    d["name_long"] = 'OOBB Geometry Primitives: Tube (New)'
    d["description"] = 'Tube cutout with updated rendering pipeline; identical interface to oobb_tube.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['tube_new']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'r', "description": 'Outer radius in mm.', "type": 'number', "default": '""'})
    v.append({"name": 'radius_name', "description": 'Named radius for mode-aware lookup.', "type": 'string', "default": '""'})
    v.append({"name": 'wall_thickness', "description": 'Wall thickness for inner cylinder.', "type": 'number', "default": 0.5})
    v.append({"name": 'depth', "description": 'Tube height in mm.', "type": 'number', "default": 250})
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

    m_original = kwargs.get("m", "")
    kwargs.pop("m", None)

    r = kwargs.get("r", kwargs.get("r", ""))
    if r == "":
        r = kwargs.get("radius", "")
        #update r
        kwargs["r"] = r
        # pop radius
        kwargs.pop("radius", "")


    if kwargs["type"] == "p" or kwargs["type"] == "positive":
        kwargs["type"] = "negative"
    else:
        kwargs["type"] = "positive"
    kwargs["wall_thickness"] = kwargs.get("wall_thickness", 0.5)
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]

    z = kwargs.get("z", 0)
    if z == 0:
        pos = kwargs.get("pos", [0, 0, 0])
        pos = copy.deepcopy(pos)
    return_value = []
    try:
        depth = kwargs["depth"]
    except:
        depth = 250
        try:
            kwargs["pos"][2] = pos[2] - depth / 2
        except:
            kwargs["z"] = z - depth / 2

    try:
        radius_name = kwargs["radius_name"]
        for mode in modes:
            kwargs["shape"] = "cylinder"
            try:
                kwargs.update({"r": ob.gv("hole_radius_"+radius_name, mode)})
            except:
                r = ob.gv(radius_name, mode)
                kwargs.update({"r": r})                
            kwargs.update({"h": depth})
            kwargs.update({"inclusion": mode})
            #tube innard
            p2 = copy.deepcopy(kwargs)
            p2["r"] = p2["r"] - p2["wall_thickness"] 
            if p2["type"] == "p" or p2["type"] == "positive":
                p2["type"] = "negative"
            else:
                p2["type"] = "positive"
            return_value.append(opsc.opsc_easy(**p2))

            #tube outard
            p2 = copy.deepcopy(kwargs)
            p2['r'] = r
            if p2["type"] == "p" or p2["type"] == "positive":
                p2["type"] = "positive"
            else:
                p2["type"] = "negative"
            #p2["r"] = p2["r"] - p2["wall_thickness"] 
            return_value.append(opsc.opsc_easy(**p2))

    except:
        for mode in modes:
            r = kwargs.get("r", kwargs.get("radius", 0))
            kwargs["shape"] = "cylinder"
            kwargs.update({"r": r})
            kwargs.update({"h": depth})
            kwargs.update({"inclusion": mode})

            #tube innard
            p2 = copy.deepcopy(kwargs)
            p2["r"] = p2["r"] - p2["wall_thickness"] 
            if p2["type"] == "p" or p2["type"] == "positive":
                p2["type"] = "positive"
            else:
                p2["type"] = "negative"
            return_value.append(opsc.opsc_easy(**p2))

            #tube outard
            p2 = copy.deepcopy(kwargs)
            p2['r'] = r
            if p2["type"] == "p" or p2["type"] == "positive":
                p2["type"] = "negative"
            else:
                p2["type"] = "positive"
            #p2["r"] = p2["r"] - p2["wall_thickness"] 
            return_value.append(opsc.opsc_easy(**p2))

    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2["m"] = m_original
    return_value_2 = [return_value_2]


    return return_value_2


    # wire


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
                 'r': 10,
                 'wall_thickness': 2,
                 'depth': 12,
                 'mode': 'true',
                 'rot': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [60, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'r1': 12,
                 'r2': 8,
                 'wall_thickness': 1.5,
                 'depth': 18,
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


