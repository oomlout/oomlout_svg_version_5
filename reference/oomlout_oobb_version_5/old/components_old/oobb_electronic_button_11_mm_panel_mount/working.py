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

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_electronic_button_11_mm_panel_mount'
    d["name_long"] = 'OOBB Electronics: 11mm Panel Mount Button'
    d["description"] = '11 mm panel-mount push-button cutout with optional clearance extension.'
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
    def get_oobb_electronic_button_11_mm_panel_mount(**kwargs):
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
            p2["r"] = [12/2, 7/2]
            p2["h"] = [18, 12]
            return_value.extend((get_cylinders(**p2)))
            return_value = oobb.shift(return_value, [0, 0, -18-extra_clearance])

        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot_original
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]

        return return_value_2


    #      potentiometer
