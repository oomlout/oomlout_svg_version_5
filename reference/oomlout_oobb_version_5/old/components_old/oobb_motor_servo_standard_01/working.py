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
_overhang_mod = _load_component("oobb_overhang")
get_oobb_overhang = _overhang_mod.action

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_motor_servo_standard_01'
    d["name_long"] = 'OOBB Mechanical: Standard Servo Motor'
    d["description"] = 'Standard servo motor cutout with shaft hole, M3 mounting holes, optional screws, body cube, and overhang support.'
    d["category"] = 'OOBB Mechanical'
    d["shape_aliases"] = ['motor_servo_standard_01']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'part', "description": 'Part selector: all, only_holes.', "type": 'string', "default": '"all"'})
    v.append({"name": 'include_screws', "description": 'Include socket-cap screw cutouts.', "type": 'bool', "default": True})
    v.append({"name": 'overhang', "description": 'Add overhang support geometry.', "type": 'bool', "default": True})
    v.append({"name": 'clearance', "description": 'Clearance extension sides: top, bottom.', "type": 'list', "default": '["top","bottom"]'})
    v.append({"name": 'screw_rot_y', "description": 'Rotate screw head 180° on Y.', "type": 'bool', "default": False})
    v.append({"name": 'screw_depth', "description": 'Depth of mounting screw holes.', "type": 'number', "default": 8})
    v.append({"name": 'screw_depth_shaft', "description": 'Depth of shaft screw hole.', "type": 'number', "default": 6})
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
    def get_oobb_motor_servo_standard_01(**kwargs):
        include_screws = kwargs.get("include_screws", True)   
        overhang = kwargs.get("overhang", True)
        clearance = kwargs.get("clearance", ["top", "bottom"])
        typ = kwargs.get("type", "p")
        kwargs["type"] = "p" #setting it to positive because it's a rotation object


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
            xx = pos[0]
            yy = pos[1]
            zz = pos[2]


            # shaft hole
            p3 = copy.deepcopy(kwargs)
            p3["pos"] = [xx, yy, zz]
            p3["shape"] = "oobb_hole"
            p3["radius_name"] = "m6"
            p3["depth"] = 25
            #p3["m"] = "#"
            return_value.append(oobb.get_comment("motor_servo_standard_01_shaft_hole",typ))
            return_value.extend(oobb.oobb_easy(**p3))

            # mounting holes and screw clearance
            x1 = 14.25
            x2 = -36.25
            y1 = 4.75
            y2 = -y1
            poss = []
            poss.append([x1, y1, 0])
            poss.append([x1, y2, 0])
            poss.append([x2, y1, 0])
            poss.append([x2, y2, 0])
            if clearance != "": #don't incleude holes for the bottom piece
                for pos in poss:
                    p3 = copy.deepcopy(kwargs)
                    p3["pos"] = [xx+pos[0], yy+pos[1], zz+pos[2]]
                    p3["shape"] = "oobb_hole"
                    p3["radius_name"] = "m3"
                    #p3["m"] = "#"
                    return_value.extend(oobb.oobb_easy(**p3))
                    if include_screws:
                        p3 = copy.deepcopy(kwargs)
                        shift_screw = -2
                        p3["pos"] = [xx+pos[0], yy+pos[1], zz+pos[2]+shift_screw] #the thickness of a socket head screw plus a bit
                        p3["shape"] = "oobb_screw_socket_cap"
                        p3["radius_name"] = "m3"
                        p3["nut"] = True
                        p3["clearance"] = clearance
                        p3["depth"] = screw_depth
                        p3["zz"] = "top"
                        p3["rot_z"] = 360/12                
                        #p3["top_clearance"] = True
                        if screw_rot_y:
                            p3["rot_y"] = 180
                            p3["zz"] = "bottom"
                            p3["pos"][2] = p3["pos"][2] 
                        #p3["m"] ="#"

                        return_value.extend(oobb.oobb_easy(**p3))


            if "only_holes" not in part:
                servo_extra = 0.5 
                # cube main
                p3 = copy.deepcopy(kwargs)            
                width = 42 + servo_extra
                height = 21 + servo_extra
                depth = 40            
                x = xx-11
                y = yy-0
                z = zz - depth        
                if "top" in clearance:
                    depth = depth + 50
                    z = z 
                p3["pos"] = [x,y,z]
                p3["shape"] = "oobb_cube_center"        
                p3["size"] = [width, height, depth]
                #p3["m"] = "#"
                return_value.append(oobb.oobb_easy(**p3))

                # cube bump on top of bracket clearance
                p3 = copy.deepcopy(kwargs)            
                width = 50 + servo_extra
                height = 3 + servo_extra
                depth = 3
                x = xx-11
                y = yy-0
                z = zz - 8.5 
                p3["pos"] = [x,y,z]
                p3["shape"] = "oobb_cube_center"        
                p3["size"] = [width, height, depth]            
                #p3["m"] = "#"
                return_value.append(oobb.oobb_easy(**p3))

                # cube bigger one clearance on the bottom            
                p3 = copy.deepcopy(kwargs)            
                width = 61 + servo_extra #extra width for clearance for a driver on the underside nut better dealt with with cylinders but this is easier for now
                height = 21 + servo_extra
                depth = 2.5
                x = xx-11
                y = yy-0
                z = zz - depth - 8.5            
                if "bottom" in clearance:
                    depth = depth + 50
                    z = z - 50
                p3["size"] = [width, height, depth]
                p3["pos"] = [x,y,z]
                p3["shape"] = "oobb_cube_center"                    
                #p3["m"] = ""
                return_value.append(oobb.oobb_easy(**p3))

            return_value_2 = {}
            return_value_2["type"]  = "rotation"
            return_value_2["typetype"]  = typ
            return_value_2["pos"] = pos_original
            return_value_2["rot"] = rot
            return_value_2["objects"] = return_value
            return_value_2 = [return_value_2]

            return return_value_2

        elif part == "shaft":

            pos = copy.deepcopy(pos)
            x = pos[0]
            y = pos[1]
            z = pos[2]

            #horn_dia_bottom = 6.1
            #horn_dia_top = horn_dia_bottom - 0.2
            horn_dia_bottom = 5.8
            horn_dia_top = horn_dia_bottom - 0.2

            horn_height = 4
            screw_radius_name = "m2d5"
            # middle hole
            p4 = copy.deepcopy(kwargs)        
            p4["shape"] = "oobb_hole"
            p4["radius_name"] = screw_radius_name
            return_value.extend(oobb.oobb_easy(**p4))


            if extra == "horn_adapter_printed":
                p3 = copy.deepcopy(kwargs)
                p3["shape"] = "oobb_cylinder"
                p3["r2"] = horn_dia_top / 2
                p3["r1"] = horn_dia_bottom / 2
                p3["depth"] = horn_height
                p3["pos"] = [x, y,-6+horn_height/2]
                #p3["m"] = "#"
                return_value.extend(oobb.oobb_easy(**p3))

                p3 = copy.deepcopy(kwargs)
                #p3["m"] = "#"
                p3["pos"] = [x, y,-6+horn_height+0.3]
                return_value.extend(get_oobb_overhang(**p3))




            elif extra == "horn_adapter_screws":    

                # add screw holes
                p4 = copy.deepcopy(kwargs)        
                pos1 = copy.deepcopy(pos)
                #move down 2
                shift_z = screw_depth_shaft
                pos1[2] = pos1[2] - 1.5 - 2 + shift_z
                pos2 = copy.deepcopy(pos1)


                shift_y = -7.375
                pos1[1] = pos1[1] + shift_y
                pos2[1] = pos2[1] - shift_y

                poss = []
                poss.append(pos1)
                poss.append(pos2)
                p4["shape"] = "oobb_screw_self_tapping"
                #p4["shape"] = "oobb_screw_self_tapping"
                p4["radius_name"] = "m2"
                p4["zz"] = "top"        
                p4["depth"] = 15
                p4["overhang"] = overhang
                p4["clearance"] = "top"
                p4["nut"] = False
                p4["loose"] = "screw"
                p4["pos"] = poss
                p4["m"] = "#"


                return_value.extend(oobb.oobb_easy(**p4))

                # middle screw clearnce
                p4  = copy.deepcopy(kwargs)
                p4["pos"] = [0, 0, 0]
                p4["shape"] = "oobb_hole"
                p4["radius_name"] = "m6"
                #p4["m"] = "#"
                return_value.extend(oobb.oobb_easy(**p4))

            return_value_2 = {}
            return_value_2["type"]  = "rotation"
            return_value_2["typetype"]  = typ
            return_value_2["pos"] = pos_original
            return_value_2["rot"] = rot
            return_value_2["objects"] = return_value
            return_value_2 = [return_value_2]

            return return_value_2


    #      motor_stepper_nema_17
