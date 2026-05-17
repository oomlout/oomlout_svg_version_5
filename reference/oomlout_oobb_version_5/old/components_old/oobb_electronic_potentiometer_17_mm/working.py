import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import copy
import oobb

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
_cube_center_mod = _load_component("oobb_cube_center")
get_oobb_cube_center = _cube_center_mod.action

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_electronic_potentiometer_17_mm'
    d["name_long"] = 'OOBB Electronics: 17mm Potentiometer'
    d["description"] = '17 mm potentiometer cutout with shaft cylinders, keying cube, and wire-clearance cubes.'
    d["category"] = 'OOBB Electronics'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'part', "description": 'Part selector (all, only_holes, shaft, ...).', "type": 'string', "default": 'all'})
    v.append({"name": 'clearance', "description": 'Clearance extension sides: top, bottom.', "type": 'list', "default": '["top","bottom"]'})
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
    """Geometry component."""
    def get_oobb_electronic_potentiometer_17_mm(**kwargs):
        clearance = kwargs.get("clearance", ["top", "bottom"])
        typ = kwargs.get("type", "positive")
        kwargs["type"] = "positive" #setting it to positive because it's a rotation object

        extra = kwargs.get("extra", "")
        rot_original = get_rot(**kwargs)       
        rot = [0,0,0]
        kwargs["rot"] = rot
        pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
        pos_original = copy.deepcopy(pos)
        pos = [0,0,0]
        kwargs["pos"]  = pos    
        part = kwargs.get("part", "all")

        return_value = []


        if part == "all":
            clearance = kwargs.get("clearance", False)
            extra_clearance = 0
            if clearance:
                extra_clearance = 20
            return_value = []
            p2 = copy.deepcopy(kwargs)        
            p2["r"] = [18/2, 7.5/2, 6/2]
            p2["h"] = [9+extra_clearance, 7, 14]
            return_value.extend((get_cylinders(**p2)))
            return_value = oobb.shift(return_value, [0, 0, -9-extra_clearance])
            #return_value = oobb.shift(return_value, [0, 0, -30])

            #add a keying cube 1.2 x 2.8 x 2.5 plus 0.5 at 0,8
            p2 = copy.deepcopy(kwargs)
            extra = 0.5
            height = 2.8
            width = 1.2
            depth = 2.6
            p2["size"] = [width+extra, height+extra, depth+extra]
            #offset pos for center postion
            p2["pos"] = [p2["pos"][0]-8, p2["pos"][1], p2["pos"][2]]
            return_value.append((get_oobb_cube_center(**p2)))

            # add a cube for the wires 18 x 25.5 x 3 at 0, -3.75, 0
            p2 = copy.deepcopy(kwargs)
            extra = 0
            height = 12.5
            width = 18
            depth = 3+extra_clearance
            p2["size"] = [width+extra, height+extra, depth+extra]
            #offset pos for center postion    
            p2["pos"] = [p2["pos"][0], p2["pos"][1]-5.75, p2["pos"][2] - depth]
            return_value.append((get_oobb_cube_center(**p2)))

            # add a cube for the wire bottoms
            p2 = copy.deepcopy(kwargs)
            extra = 0
            height = 5.5
            width = 13
            #depth = 3
            p2["size"] = [width+extra, height+extra, depth+extra]
            #offset pos for center postion    
            p2["pos"] = [p2["pos"][0], p2["pos"][1]-13.75, p2["pos"][2] -depth]
            return_value.append((get_oobb_cube_center(**p2)))
        elif part == "shaft":
            return_value = []  
            p2 = copy.deepcopy(kwargs)
            p2["r"] = 5.9/2
            p2["type"] = typ
            p2["shape"] = "oobb_hole"                
            return_value.extend(oobb.oe(**p2))        
            return return_value


        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot_original
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]

        return return_value_2
