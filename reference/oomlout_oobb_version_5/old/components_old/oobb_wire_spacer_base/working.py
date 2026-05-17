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
    d["name"] = 'oobb_wire_spacer_base'
    d["name_long"] = 'OOBB Wire Cutouts: Wire Spacer Base'
    d["description"] = 'Base rounded-rectangle spacer plate geometry used by all wire spacer variants.'
    d["category"] = 'OOBB Wire Cutouts'
    d["shape_aliases"] = ['wire_spacer_base']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'length_spacer', "description": 'Length of the rounded-rectangle spacer plate.', "type": 'number', "default": 23})
    v.append({"name": 'pos_spacer', "description": 'Positional offset applied to the spacer plate.', "type": 'list', "default": '[-1.5,0,0]'})
    v.append({"name": 'thickness', "description": 'Plate thickness (z size) and z-offset adjustment.', "type": 'number', "default": 1})
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
    def get_oobb_wire_spacer_base(**kwargs):
        # setting up for rotation object
        typ = kwargs.get("type", "negative")
        kwargs["type"] = "positive" #needs to be positive for the difference to work
        rot_original = get_rot(**kwargs)  
        kwargs.pop("rot","") 

        length_spacer = kwargs.get("length_spacer", 23)
        pos_spacer = kwargs.get("pos_spacer", [-1.5,0,0])

        # storing pos and popping it out to add it in rotation element     
        pos_original = copy.deepcopy(copy.deepcopy(kwargs.get("pos", [0, 0, 0])))
        kwargs.pop("pos", None)
        pos = [0,0,0]
        kwargs["pos"] = pos
        return_value = []

        p3 = copy.deepcopy(kwargs)
        pos_plate = p3.get("pos", [0, 0, 0])
        thickness = p3.get("thickness", 1)

        pos1 = copy.deepcopy(pos_plate)
        pos1[0] = pos1[0] + pos_spacer[0]
        pos1[2] = pos1[2] - thickness + 3
        p3 = copy.deepcopy(kwargs)    
        p3["shape"] = f"rounded_rectangle"      
        p3["size"] = [length_spacer,22,thickness]
        p3["pos"] = pos1
        return_value.append( oobb.oe(**p3))

        # packaging as a rotation object
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot_original
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]


        return return_value_2
