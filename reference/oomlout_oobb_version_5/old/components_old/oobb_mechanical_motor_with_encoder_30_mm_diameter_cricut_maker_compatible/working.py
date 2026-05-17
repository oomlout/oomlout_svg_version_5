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
    d["name"] = 'oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible'
    d["name_long"] = 'OOBB Mechanical: 30mm Motor with Encoder (Cricut Compatible)'
    d["description"] = '30 mm diameter Cricut-compatible motor-with-encoder cutout set (shaft hole + M2.5 mounting holes).'
    d["category"] = 'OOBB Mechanical'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'part', "description": 'Part selector (all, only_holes, shaft, ...).', "type": 'string', "default": 'all'})
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
    def get_oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible(**kwargs):
        part = kwargs.get("part", "all")


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

        if part == "all":        
            pos = kwargs.get("pos", [0, 0, 0])


            # shaft hole
            p3 = copy.deepcopy(kwargs)
            pos1 = copy.deepcopy(pos)
            p3["pos"] = pos1
            p3["shape"] = "oobb_hole"
            p3["radius"] = 12/2        
            #p3["m"] = "#"
            return_value.append(ob.oobb_easy(**p3))

            # add screw holes
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_hole"
            p3["radius_name"] = "m2_5"
            poss = []
            pos1 = copy.deepcopy(pos)
            split = 15.75
            pos1[0] += split /2
            pos2 = copy.deepcopy(pos1)
            pos2[0] = -pos2[0]
            poss.append(pos1)
            poss.append(pos2)
            p3["pos"] = poss
            #p3["m"] = "#"
            return_value.append(ob.oobb_easy(**p3))







            return_value_2 = {}
            return_value_2["type"]  = "rotation"
            return_value_2["typetype"]  = typ
            return_value_2["pos"] = pos_original
            return_value_2["rot"] = rot
            return_value_2["objects"] = return_value
            return_value_2 = [return_value_2]

            return return_value_2



    # nut
