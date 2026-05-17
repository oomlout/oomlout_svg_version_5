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
    d["name"] = 'oobb_nut'
    d["name_long"] = 'OOBB Geometry Primitives: Nut'
    d["description"] = 'Hexagonal nut pocket with optional through-hole, overhang, and clearance, across all render modes.'
    d["category"] = 'Fasteners'
    d["shape_aliases"] = ['nut']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'radius_name', "description": 'Named radius key, e.g. m3, m6.', "type": 'string', "default": '"m3"'})
    v.append({"name": 'zz', "description": 'Z anchor: bottom, top, middle.', "type": 'string', "default": '"bottom"'})
    v.append({"name": 'depth', "description": 'Nut pocket depth in mm.', "type": 'number', "default": '""'})
    v.append({"name": 'overhang', "description": 'Add overhang support geometry.', "type": 'bool', "default": False})
    v.append({"name": 'clearance', "description": 'Clearance extension sides.', "type": 'string', "default": '""'})
    v.append({"name": 'hole', "description": 'Include a through-hole below the nut.', "type": 'bool', "default": False})
    v.append({"name": 'extra_clearance', "description": 'Extra mm added to side clearance height.', "type": 'number', "default": 0})
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
    l_string = ""
    pos = kwargs.get("pos", [0, 0, 0])
    kwargs["pos"] = pos
    pos = copy.deepcopy(pos)
    extra = kwargs.get("extra", "")
    depth = kwargs.get("depth", "")
    overhang = kwargs.get("overhang", False)
    zz = kwargs.get("zz", "bottom")
    clearance = kwargs.get("clearance", "")
    hole = kwargs.get("hole", False) #whether or not to include a hole
    extra_clearance = kwargs.get("extra_clearance", 0)
    clearance_tightness = kwargs.get("clearance_tightness", 0) #tight or loose

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
    pos = [0,0,0]
    kwargs["pos"]  = pos


    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]
    return_value = []

    for mode in modes:        
        p2 = copy.deepcopy(kwargs)
        p2["shape"] = "polyg"
        p2["sides"] = 6
        p2["inclusion"] = mode
        radius_name = p2["radius_name"]
        extra_str = ""
        #extra loose or tight
        #if extra != "":
        #    extra_str = f"_{extra}"

        r = oobb.gv(f"nut_radius_{l_string}{radius_name}{extra_str}", mode)
        r = r + clearance_tightness
        p2.update({"r": r})

        #getting depth of nut
        if depth == "":
            depth = oobb.gv(f"nut_depth_{l_string}{radius_name}", mode)

        #setting anchor point zz
        if zz == "top":
            p2["pos"][2] += -depth            
        elif zz == "middle":
            p2["pos"][2] += -depth/2            
        else:
            p2["pos"][2] += 0

        #clearance
        if "top" in clearance:
            depth += 50
        if "bottom" in clearance:
            depth += 50
            p2["pos"][2] -= 100
        #side clearance
        if True:
            p4 = copy.deepcopy(p2)
            p4["shape"] = "cube"
            hei = r*2 + extra_clearance * 0.866
            wid = 20
            dep = depth
            if extra_clearance > 0:
                dep += extra_clearance          
            p4.pop("r", "")
            p4.pop("radius", "")
            p4.pop("radius_name", "")
            p4["size"] = [wid, hei, dep]
            pos1 = copy.deepcopy(p2["pos"])
            pos1[0] += -wid/2
            pos1[1] += -hei/2
            if "left" in clearance:                
                pos1[0] += wid/2
                p4["pos"] = pos1
                return_value.append(oobb.oobb_easy(**p4))
            if "right" in clearance:                
                pos1[0] += -wid/2
                p4["pos"] = pos1
                return_value.append(oobb.oobb_easy(**p4))




        p2["height"] = depth
        return_value.append(opsc.opsc_easy(**p2))




        # overhang
        if overhang:
            p3 = copy.deepcopy(kwargs)
            if zz == "top":
                p3["pos"][2] += -depth            
            elif zz == "middle":
                p3["pos"][2] += -depth/2            
            else:
                p3["pos"][2] += 0
            p3["shape"] = "oobb_overhang" 
            #p3["radius_name"] = "m3_nut"
            p3["inclusion"] = "3dpr"
            pos1 = copy.deepcopy(p3["pos"])                   
            pos1[2] += 0
            p3["pos"] = pos1
            #p3["m"] = "#"
            p3["zz"] = "top"
            return_value.append(oobb.oe(**p3))
            p4 = copy.deepcopy(p3)
            pos1 = copy.deepcopy(p3["pos"])
            pos1[2] += depth
            p4["pos"] = pos1
            #p4["m"] = "#"
            p4["zz"] = "bottom"
            return_value.append(oobb.oe(**p4))
        # hole
        if hole:
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_hole"
            p3.pop("depth", "")
            return_value.extend(oobb.oobb_easy(**p3))

            # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]


    return return_value_2

    # plate


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
                 'radius_name': 'm3',
                 'zz': 'middle',
                 'depth': 3,
                 'overhang': False,
                 'clearance': '',
                 'hole': False,
                 'mode': 'true',
                 'rot': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [55, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'radius_name': 'm3',
                 'zz': 'middle',
                 'depth': 3,
                 'overhang': False,
                 'clearance': '',
                 'hole': True,
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


