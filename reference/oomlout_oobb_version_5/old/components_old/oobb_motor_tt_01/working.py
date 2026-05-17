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
    d["name"] = 'oobb_motor_tt_01'
    d["name_long"] = 'OOBB Mechanical: TT Motor'
    d["description"] = 'TT-motor cutout with 26 mm shaft hole, M6 clearance hole, and countersunk mounting screws.'
    d["category"] = 'OOBB Mechanical'
    d["shape_aliases"] = ['motor_tt_01']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'part', "description": 'Part selector (all, only_holes, shaft, ...).', "type": 'string', "default": 'all'})
    v.append({"name": 'screw_lift', "description": 'Z lift applied to mounting screw positions.', "type": 'number', "default": 3})
    v.append({"name": 'radius_extra', "description": 'Extra radius added to shaft hole.', "type": 'number', "default": 0.4})
    v.append({"name": 'thickness', "description": 'Plate thickness used in screw positioning.', "type": 'number', "default": 3})
    v.append({"name": 'clearance', "description": 'Clearance extension sides: top, bottom.', "type": 'list', "default": '["top","bottom"]'})
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
    def get_oobb_motor_tt_01(**kwargs):
        part = kwargs.get("part", "all")
        screw_lift = kwargs.get("screw_lift", 3)
        radius_extra = kwargs.get("radius_extra", 0.4)
        clearance = kwargs.get("clearance", "")
        if part == "all":
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


            objects = []
            pos = kwargs.get("pos", [0, 0, 0])
            pos_original = copy.deepcopy(pos)
            x = pos[0]
            y = pos[1]
            z = pos[2]
            thickness = kwargs.get("thickness", 3)

            # kwargs["m"] = "#"

            # shaft hole
            p2 = copy.deepcopy(kwargs)
            p2["pos"] = [x, y, z]
            p2["shape"] = "oobb_hole_new"
            p2["radius"] = 26/2
            objects.extend(ob.oobb_easy(**p2))

            # clearance hole
            p3 = copy.deepcopy(kwargs)
            p3["pos"] = [x-11, y, z]
            p3["shape"] = "oobb_hole_new"
            p3["radius_name"] = "m6" 
            #p3["m"] = "#"       
            objects.extend(ob.oobb_easy(**p3))

            # mounting holes
            poss = [-20, 8.5, screw_lift], [-20, -8.5, screw_lift] #, [12, 0, thickness]
            for pos in poss:
                p4 = copy.deepcopy(kwargs)
                pos1 = copy.deepcopy(pos_original)
                pos1[0] += pos[0]
                pos1[1] += pos[1]
                pos1[2] += pos[2]
                #pos1 = [0,0,0]
                p4["pos"] = pos1
                p4["shape"] = "oobb_screw_countersunk"
                p4["radius_name"] = "m3"
                p4["include_nut"] = False
                p4["depth"] = 25
                p4["top_clearance"] = True
                #p4["m"]= "#"
                objects.extend(ob.oobb_easy(**p4))

            # rear clearance cubes
            p5 = copy.deepcopy(kwargs)
            height = 30
            width = 12
            p5["pos"] = [x-31-height/2-9.5, y-width/2, z]
            p5["shape"] = "cube"
            p5["size"] = [height, width, 2]
            #p5["m"] = "#"
            objects.append(ob.oobb_easy(**p5))
            p5 = copy.deepcopy(kwargs)
            height = 18
            width = 8
            p5["pos"] = [x-45-height/2, y-width/2, z]
            p5["shape"] = "cube"
            p5["size"] = [height, width, 2]
            #p5["m"] = "#"
            objects.append(ob.oobb_easy(**p5))

            # hole escape hole
            p5 = copy.deepcopy(kwargs)
            p5["pos"] = [x-29.569, y, z]
            p5["shape"] = "oobb_cube_center"
            p5["size"] = [8, 6, 20]
            #p5["m"] = ""
            objects.append(ob.oobb_easy(**p5))

            #main_cube
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_cube_center"
            width = 65
            height = 22            
            depth = 19
            if clearance == "":
                clearance = 1
            p3["size"] = [width + clearance, height + clearance, depth]
            pos1 = copy.deepcopy(pos_original)        
            pos1[0] += -width/2 + 11.35
            pos1[2] += -depth
            #pos1 = [0,0,0]
            p3["pos"] = pos1


            #p3["m"] = "#"
            objects.append(ob.oobb_easy(**p3))

            return_value = objects
            # packaging as a rotation object
            return_value_2 = {}
            return_value_2["type"]  = "rotation"
            return_value_2["typetype"]  = typ
            return_value_2["pos"] = pos_original
            return_value_2["rot"] = rot_original
            return_value_2["objects"] = return_value
            return_value_2 = [return_value_2]

            return return_value_2

        elif part == "shaft":
            objects = []
            pos = kwargs.get("pos", [0, 0, 0])
            depth = kwargs.get("depth", 6)

            shaft_dia = 5.5 - 0.5
            shaft_height = (3.75+.1) - 0.5

            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_cube_center"
            dep = depth
            if "bottom" in clearance:
                dep = 100
            p3["size"] = [shaft_dia + radius_extra, shaft_height + radius_extra, dep]

            pos1 = copy.deepcopy(pos)
            pos1[2] += -dep
            p3["pos"] = pos1
            #p3["m"] = "#"
            objects.append(ob.oobb_easy(**p3))

            #add screw hole 2d5
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_screw_self_tapping"
            p3["radius_name"] = "m2"
            p3["clearance"] = ["top"]
            p3["depth"] = 12
            pos1 = copy.deepcopy(pos)
            pos1[2] += 2
            p3["pos"] = pos1
            #p3["m"] = "#"  
            objects.append(ob.oobb_easy(**p3))


            return objects


    #      mechanical_motor_with_encoder
