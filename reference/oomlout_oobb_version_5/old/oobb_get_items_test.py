import copy
import oobb_base
import math

# gear
def get_test_gear(**kwargs):
    from components.test_gear.working import action

    return action(**kwargs)

#hole
def get_test_hole(**kwargs):
    from components.test_hole.working import action

    return action(**kwargs)
    

# rotation
def get_test_rotation(**kwargs):
    from components.test_rotation.working import action

    return action(**kwargs)

# motor

#      motor_tt_01
def get_test_motor_tt_01(**kwargs):
    from components.test_motor_tt_01.working import action

    return action(**kwargs)


#      motor_tt_01_shaft
def get_test_motor_tt_01_shaft(**kwargs):
    from components.test_motor_tt_01_shaft.working import action

    return action(**kwargs)


#      motor_n20_shaft
def get_test_motor_n20_shaft(**kwargs):
    from components.test_motor_n20_shaft.working import action

    return action(**kwargs)

#      motor_servo_standard_01
def get_test_oobb_motor_servo_standard_01(**kwargs):
    from components.test_oobb_motor_servo_standard_01.working import action

    return action(**kwargs)

#nut
def get_test_oobb_nut(**kwargs):
    from components.test_oobb_nut.working import action

    return action(**kwargs)


# screw
def get_test_oobb_screw_socket_cap(**kwargs):
    from components.test_oobb_screw_socket_cap.working import action

    return action(**kwargs)

def get_test_oobb_screw_countersunk(**kwargs):
    from components.test_oobb_screw_countersunk.working import action

    return action(**kwargs)

def get_test_oobb_screw_self_tapping(**kwargs):
    from components.test_oobb_screw_self_tapping.working import action

    return action(**kwargs)

def get_test_oobb_screw(**kwargs):
    from components.test_oobb_screw.working import action

    return action(**kwargs)

def get_test_oobb_screw_socket_cap_old_1(**kwargs):
    from components.test_oobb_screw_socket_cap_old_1.working import action

    return action(**kwargs)

    # legacy implementation retained below during migration; unreachable by design
    # default sets
    width = 5
    height = 5
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", False)
    kwargs["pos"] = pos
    
    

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")    
    kwargs.pop("extra","")
    
    pos_current = [0,0,0]
    pos_shift = 30    
    comment_extra = ""
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 

    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"  
    p4["nut"] = True  
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom nut : True"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"  
    p4["nut"] = True  
    p4["pos"] = copy.deepcopy(pos_current)
    p4["clearance"] = "bottom"
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom nut : True clearance : bottom"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"  
    p4["nut"] = True  
    p4["rot_y"] = 180
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom nut : True rot_y : 180"
    oobb_base.append_full(thing, **p4) 

    
    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : bottom"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # clearance_bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : bottom nut : True"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # clearance_bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = ["top","bottom"]
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : [bottom , top] nut : True"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # clearance_bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = ["top","bottom"]
    p4["zz"] = "top"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : [bottom , top] nut : True zz : top"
    oobb_base.append_full(thing, **p4) 

    pos_current[1] += pos_shift
    # clearance_bottom zz bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : bottom nut : True zz : bottom"
    oobb_base.append_full(thing, **p4) 

    ########################### rot_y

    pos_current = [300,0,0]
    pos_shift = 30    
    comment_extra = " rot_y : 180"
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_y"] = 180
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 

    
    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True"
    oobb_base.append_full(thing, **p4) 

    
    pos_current[1] += pos_shift
    # clearance_bottom zz bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True zz : bottom"
    oobb_base.append_full(thing, **p4) 

    ########################### rot_y 90

    pos_current = [600,0,0]
    pos_shift = 30    
    comment_extra = " rot_y : 90"
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_y"] = 90
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 

    
    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom"
    oobb_base.append_full(thing, **p4) 
    
    pos_current[1] += pos_shift
    # clearance_top
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True"
    oobb_base.append_full(thing, **p4) 

    
    pos_current[1] += pos_shift
    # clearance_bottom zz bottom
    p4 = copy.deepcopy(p3)    
    p4["clearance"] = "bottom"
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True zz : bottom"
    oobb_base.append_full(thing, **p4) 

    ########################### rot_x 180

    pos_current = [900,0,0]
    pos_shift = 60    
    comment_extra = " rot_x : 180"
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_x"] = 180
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 

    ########################### rot_x -90

    pos_current = [1200,0,0]
    pos_shift = 60    
    comment_extra = " rot_x : -90"
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_x"] = -90
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 

    ########################### rot_x 90 rot_y 90

    pos_current = [1500,0,0]
    pos_shift = 60    
    comment_extra = " rot_x : 90 rot_y : 90 rot_z : 90"
    #basic     
    
    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_x"] = 90
    p3["rot_y"] = 90
    p3["rot_z"] = 90
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    
    
    pos_current[1] += pos_shift
    # nut
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)
        
    pos_current[1] += pos_shift
    # nut and overhang
    p4 = copy.deepcopy(p3)    
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)    
     
    pos_current[1] += pos_shift
    # zz top
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "top"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4) 


    pos_current[1] += pos_shift
    # zz bottom
    p4 = copy.deepcopy(p3)    
    p4["zz"] = "bottom"    
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4) 
    

    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]

# shape
def get_test_oobb_shape_slot(**kwargs):
    from components.test_oobb_shape_slot.working import action

    return action(**kwargs)


# wire
def get_test_oobb_wire(**kwargs):
    from components.test_oobb_wire.working import action

    return action(**kwargs)