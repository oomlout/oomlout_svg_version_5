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
    d["name"] = 'oobb_electronic_battery_box_aa_battery_4_cell'
    d["name_long"] = 'OOBB Electronics: 4×AA Battery Box'
    d["description"] = '4×AA battery box cutout set with body, countersunk screws, and wire-clearance cubes.'
    d["category"] = 'OOBB Electronics'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'part', "description": 'Part selector (all, only_holes, shaft, ...).', "type": 'string', "default": 'all'})
    v.append({"name": 'depth_screw', "description": 'Depth of countersunk screw cutouts.', "type": 'number', "default": 6})
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
    def get_oobb_electronic_battery_box_aa_battery_4_cell(**kwargs):    
        typ = kwargs.get("type", "positive")
        kwargs["type"] = "positive" #setting it to positive because it's a rotation object
        depth_screw = kwargs.get("depth_screw", 6)
        extra = kwargs.get("extra", "")
        rot_original = get_rot(**kwargs)       
        rot = [0,0,0]
        kwargs["rot"] = rot
        thickness = kwargs.get("thickness", 100)
        pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
        pos_original = copy.deepcopy(pos)
        pos = [0,0,0]
        kwargs["pos"]  = pos    
        part = kwargs.get("part", "all")

        return_value = []


        if part == "all":
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_cube_center"
            p3["size"] = [62, 58, 15]
            pos1 = copy.deepcopy(pos)        
            p3["pos"] = pos1
            p3["zz"] = "bottom"
            return_value.append((oobb.oe(**p3)))

            #add screws
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_screw_countersunk"
            p3["radius_name"] = "m3"
            p3["depth"] = depth_screw
            pos1 = copy.deepcopy(pos)
            pos1[2] += 2
            posa = copy.deepcopy(pos1)
            posa[0] += 22.5
            posb = copy.deepcopy(pos1)
            posb[0] += -22.5
            posc = copy.deepcopy(pos1)
            posc[0] += 7.5
            posd = copy.deepcopy(pos1)
            posd[0] += -7.5
            p3["pos"] = [posa, posb, posc, posd]
            p3["zz"] = "top"
            #p3["m"] = "#"
            return_value.append((oobb.oe(**p3)))

            #add through clearance cube
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_cube_center"
            p3["size"] = [10, 10, thickness]
            pos1 = copy.deepcopy(pos)
            pos1[0] += 16        
            pos1[1] += 24

            p3["pos"] = pos1
            p3["zz"] = "top"
            #p3["m"] = "#"
            return_value.append((oobb.oe(**p3)))

            #add thin clearance cube
            p4 = copy.deepcopy(p3)
            p4["size"] = [30, 10, 3]
            pos1 = copy.deepcopy(p3["pos"])
            pos1[0] += -10
            pos1[1] += 0
            pos1[2] += 0
            p4["pos"] = pos1
            #p4["m"] = "#"
            return_value.append((oobb.oe(**p4)))


            #add wire cutout
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_wire_higher_voltage"
            pos1 = copy.deepcopy(pos)
            pos1[0] += -6
            pos1[1] += 15
            pos1[2] += 0
            p3["pos"] = pos1
            rot = [0,0,180]
            p3["rot"] = rot
            p3["zz"] = "top"
            #p3["m"] = "#"
            return_value.append((oobb.oe(**p3)))


        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot_original
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]

        return return_value_2

    #      button
