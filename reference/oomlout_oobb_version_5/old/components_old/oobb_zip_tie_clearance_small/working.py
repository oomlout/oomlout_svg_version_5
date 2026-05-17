import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import copy
import oobb
import opsc

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
    d["name"] = 'oobb_zip_tie_clearance_small'
    d["name_long"] = 'OOBB Wire Cutouts: Small Zip-Tie Clearance'
    d["description"] = 'Small zip-tie clearance cutout: two M3 holes spaced 6 mm apart and a rectangular slot.'
    d["category"] = 'OOBB Wire Cutouts'
    d["shape_aliases"] = ['zip_tie_clearance_small']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'wall_thickness', "description": 'Wall thickness context (read but not yet used).', "type": 'number', "default": 2})
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
    def get_oobb_zip_tie_clearance_small(**kwargs):
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

        wall_thickness = kwargs.get("wall_thickness", 2)



        #add holes zip tie
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_hole"    

        poss = []
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos11 = copy.deepcopy(pos1)
        pos11[1] += 3
        pos12 = copy.deepcopy(pos1)
        pos12[1] += -3
        poss.append(pos11)
        poss.append(pos12)
        p3["pos"] = poss
        p3["radius_name"] = "m3"    
        #p3["m"] = "#"
        return_value.append(oobb.oobb_easy(**p3))

        #add zip tie clearance square
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_cube"
        width = 3
        height = 8
        depth = 1.5
        p3["size"] = [width,height,depth]
        pos1 = copy.deepcopy(pos1)
        pos1[2] += 0
        p3["pos"] = pos1
        #p3["m"] = "#"
        return_value.append(oobb.oobb_easy(**p3))


        # packaging as a rotation object
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot_original
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]

        return return_value_2
