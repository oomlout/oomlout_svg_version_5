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
    d["name"] = 'oobb_motor_stepper_nema_17'
    d["name_long"] = 'OOBB Mechanical: NEMA-17 Stepper Motor'
    d["description"] = 'NEMA-17 stepper motor cutout with shaft hole, four M3 mounting holes, optional screws/spacers, and clearance cubes.'
    d["category"] = 'OOBB Mechanical'
    d["shape_aliases"] = ['motor_stepper_nema_17']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'part', "description": 'Part selector: all, only_holes, spacer, shaft.', "type": 'string', "default": '"all"'})
    v.append({"name": 'include_screws', "description": 'Include screw cutouts.', "type": 'bool', "default": True})
    v.append({"name": 'overhang', "description": 'Add overhang support geometry.', "type": 'bool', "default": True})
    v.append({"name": 'clearance', "description": 'Clearance extension sides: top, bottom.', "type": 'list', "default": '["top","bottom"]'})
    v.append({"name": 'thickness', "description": 'Plate thickness for screw positioning.', "type": 'number', "default": 0})
    v.append({"name": 'spacer_depth', "description": 'Depth of spacer cylinders.', "type": 'number', "default": 0})
    v.append({"name": 'screw_rot_y', "description": 'Rotate screw head 180° on Y.', "type": 'bool', "default": False})
    v.append({"name": 'screw_depth', "description": 'Depth of mounting screw holes.', "type": 'number', "default": 8})
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
    def get_oobb_motor_stepper_nema_17(**kwargs):
        include_screws = kwargs.get("include_screws", True)   
        overhang = kwargs.get("overhang", True)
        clearance = kwargs.get("clearance", ["top", "bottom"])
        screws = kwargs.get("screws", True)
        typ = kwargs.get("type", "p")
        kwargs["type"] = "p" #setting it to positive because it's a rotation object
        depth = kwargs.get("thickness", 0)
        spacer_depth = kwargs.get("spacer_depth", 0)
        screw_rot_y = kwargs.get("screw_rot_y", False) # whether the head is on the top or the bottom
        screw_depth = kwargs.get("screw_depth", 8) 
        screw_depth_shaft = kwargs.get("screw_depth_shaft", 6)
        extra = kwargs.get("extra", "horn_adapter_screws")
        rot = get_rot(**kwargs)   
        rot_y = rot[1]
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
            pos = kwargs.get("pos", [0, 0, 0])

            # screws
            if screws:
                offset = 15.5
                p3 = copy.deepcopy(kwargs)        
                p3["shape"] = "oobb_screw_countersunk"        
                p3["radius_name"] = "m3"
                p3["depth"] = 25
                poss = []
                pos1 = copy.deepcopy(pos)
                pos1[2] += depth
                posa = copy.deepcopy(pos1)
                posa[0] += offset
                posa[1] += offset
                posb = copy.deepcopy(pos1)
                posb[0] += -offset
                posb[1] += offset
                posc = copy.deepcopy(pos1)
                posc[0] += offset
                posc[1] += -offset
                posd = copy.deepcopy(pos1)
                posd[0] += -offset
                posd[1] += -offset
                poss = [posa, posb, posc, posd]
                p3["pos"] = poss
                #p3["m"] = "#"
                return_value.extend(oobb.oobb_easy(**p3))

            # middle hole
            p3 = copy.deepcopy(kwargs)
            pos1 = copy.deepcopy(pos)
            p3["shape"] = "oobb_cylinder"
            p3["radius"] = 29/2
            #p3["m"] = "#"
            return_value.extend(oobb.oobb_easy(**p3))

        elif part == "spacer":
            pos = kwargs.get("pos", [0, 0, 0])

            # spacers
            offset = 15.5
            p3 = copy.deepcopy(kwargs)        
            p3["shape"] = "oobb_cylinder"        
            p3["radius"] = 9/2
            p3["depth"] = spacer_depth
            poss = []
            pos1 = copy.deepcopy(pos)
            pos1[2] += depth
            posa = copy.deepcopy(pos1)
            posa[0] += offset
            posa[1] += offset
            posb = copy.deepcopy(pos1)
            posb[0] += -offset
            posb[1] += offset
            posc = copy.deepcopy(pos1)
            posc[0] += offset
            posc[1] += -offset
            posd = copy.deepcopy(pos1)
            posd[0] += -offset
            posd[1] += -offset
            poss = [posa, posb, posc, posd]
            p3["pos"] = poss
            #p3["m"] = "#"
            return_value.extend(oobb.oobb_easy(**p3))      


        elif part == "shaft":


            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_hole"
            p3["radius_name"] = "m5"
            p3["depth"] = 25
            #p3["m"] = "#"              
            return_value.extend(oobb.oobb_easy(**p3))



        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]

        return return_value_2

    #      mottor_tt
