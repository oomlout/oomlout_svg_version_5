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
    d["name"] = 'oobb_electronic_potentiometer_stick_single_axis_16_mm'
    d["name_long"] = 'OOBB Electronics: 16mm Single-Axis Joystick'
    d["description"] = '16 mm single-axis joystick/potentiometer cutout with body, foot cubes, and stick hole.'
    d["category"] = 'OOBB Electronics'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'part', "description": 'Part selector (all, only_holes, shaft, ...).', "type": 'string', "default": 'all'})
    v.append({"name": 'clearance', "description": 'Clearance extension sides: top, bottom.', "type": 'list', "default": '["top","bottom"]'})
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
    v.append({"name": 'width_stick', "description": 'Radius of the stick shaft hole.', "type": 'number', "default": 2})
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
    def get_oobb_electronic_potentiometer_stick_single_axis_16_mm(**kwargs):
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
        width_stick = kwargs.get("width_stick", 2)

        return_value = []


        if part == "all":
            clearance = kwargs.get("clearance", False)
            extra_clearance = 0
            if clearance:
                extra_clearance = 20
            return_value = []

            # main cube
            p3 = copy.deepcopy(kwargs)
            pos1 = copy.deepcopy(pos)        
            p3["shape"] = "oobb_cube_center"      
            cube_depth = 12  
            p3["size"] = [16,16,cube_depth]
            p3["zz"] = "bottom"
            p3["pos"] = pos1
            #p3["m"] = "#"        
            return_value.extend(oobb.oobb_easy(**p3))

            # feet cubes
            p3 = copy.deepcopy(kwargs)        
            pos1 = copy.deepcopy(pos)        
            poss = []
            shift_y = 15/2
            shift_x = 13.5/2
            poss.append([pos1[0]+shift_x, pos1[1]+shift_y, pos1[2]])
            poss.append([pos1[0]-shift_x, pos1[1]+shift_y, pos1[2]])
            poss.append([pos1[0]+shift_x, pos1[1]-shift_y, pos1[2]])
            poss.append([pos1[0]-shift_x, pos1[1]-shift_y, pos1[2]])
            p3["shape"] = "oobb_cube_center"        
            p3["size"] = [3,1.5,4]
            p3["zz"] = "top"
            p3["pos"] = poss
            #p3["m"] = "#"        
            return_value.extend(oobb.oobb_easy(**p3))

            # extra side plastics
            # feet cubes
            p3 = copy.deepcopy(kwargs)        
            pos1 = copy.deepcopy(pos)        
            poss = []
            shift_x = 11/2
            poss.append([pos1[0]+shift_x, pos1[1], pos1[2]])
            poss.append([pos1[0]-shift_x, pos1[1], pos1[2]])
            p3["shape"] = "oobb_cube_center"        
            p3["size"] = [2,19,3.5]
            p3["zz"] = "bottom"
            p3["pos"] = poss
            #p3["m"] = "#"        
            return_value.extend(oobb.oobb_easy(**p3))


            # pot cube
            p3 = copy.deepcopy(kwargs)
            pos1 = copy.deepcopy(pos)        
            pos1[0] += 16/2 + 4/2
            pos1[2] += -4
            p3["shape"] = "oobb_cube_center"        
            p3["size"] = [4,12,16]
            p3["zz"] = "bottom"
            p3["pos"] = pos1        
            #p3["m"] = "#"        
            return_value.extend(oobb.oobb_easy(**p3))

            # other side clearance cube
            p3 = copy.deepcopy(p3)
            p3["size"] = [1.5,12,16]
            pos1 = copy.deepcopy(pos)
            pos1[0] -= 16/2 + 1.5/2        
            pos1[2] += -4
            p3["pos"] = pos1

            return_value.extend(oobb.oobb_easy(**p3))

            # stick
            p3 = copy.deepcopy(kwargs)
            pos1 = copy.deepcopy(pos)                
            pos1[2] += cube_depth
            p3["shape"] = "oobb_cube_center"        
            p3["size"] = [width_stick,1,9]
            p3["zz"] = "bottom"
            p3["pos"] = pos1        
            #p3["m"] = "#"        
            return_value.extend(oobb.oobb_easy(**p3))



        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot_original
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]

        return return_value_2



    # helpers
