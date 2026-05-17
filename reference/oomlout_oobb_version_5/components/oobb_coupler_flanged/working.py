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
    d["name"] = 'oobb_coupler_flanged'
    d["name_long"] = 'OOBB Mechanical: Flanged Coupler'
    d["description"] = 'Flanged coupler with shaft holes and flange M3/M8 cutouts, wrapped in a rotation object.'
    d["category"] = 'OOBB Mechanical'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'part', "description": 'Which part to generate: all, only_holes, shaft.', "type": 'string', "default": '"all"'})
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
    """Flanged coupler geometry with shaft and flange parts."""
    typ = kwargs.get("type", "p")
    kwargs["type"] = "p" #setting it to positive because it's a rotation object
    

    rot = get_rot(**kwargs)   
    kwargs.pop("rot","")
    kwargs.pop("rot_x","")
    kwargs.pop("rot_y","")
    kwargs.pop("rot_z","")
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    pos_original = copy.deepcopy(pos)
    pos = [0,0,0]
    kwargs["pos"]  = pos    
    #z zero is base of shaft
    part = kwargs.get("part", "all")

    return_value = []

    if part == "all" or part == "only_holes":        
        pass
    elif part == "shaft":
        
        pos = copy.deepcopy(pos)
        
        p3 = copy.deepcopy(kwargs)        
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = "m3"
        poss = []
        shift = 5.657
        pos1 = copy.deepcopy(pos)
        pos1[0] += shift
        pos1[1] += shift
        pos2 = copy.deepcopy(pos)
        pos2[0] += -shift
        pos2[1] += -shift
        pos3 = copy.deepcopy(pos)
        pos3[0] += shift
        pos3[1] += -shift
        pos4 = copy.deepcopy(pos)
        pos4[0] += -shift
        pos4[1] += shift        
        poss.append(pos1)
        poss.append(pos2)
        poss.append(pos3)
        poss.append(pos4)
        p3["pos"] = poss
        #p3["m"] = "#"
        return_value.extend(oobb.oobb_easy(**p3))

        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = "m8"
        return_value.extend(oobb.oobb_easy(**p3))

        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot
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
      'preview_rot': [45, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'type': 'positive', 'part': 'all', 'rot': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [45, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'type': 'positive', 'part': 'shaft', 'rot': [0, 0, 0]}}]

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


