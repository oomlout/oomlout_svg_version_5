from oobb_get_items_oobb_old import *
from oobb_get_items_oobb_bearing_plate import *

#from oobb_get_items_oobb_holder import *
import oobb_get_items_oobb_holder
import oobb_base
from oobb_arch.helpers.plate_helpers import (
    get_plate_dict as _shared_get_plate_dict,
    get_plate_hole_dict as _shared_get_plate_hole_dict,
)
from oobb_arch.helpers.shaft_helpers import (
    add_oobb_shaft as _shared_add_oobb_shaft,
    get_shaft_center as _shared_get_shaft_center,
)

import copy

# helpers
def get_plate_dict(**kwargs):
    from components.plate_dict.working import action

    return action(**kwargs)

def get_plate_hole_dict(**kwargs):
    from components.plate_hole_dict.working import action

    return action(**kwargs)

# circle
def get_circle(**kwargs):    
    from components.circles.working import action

    return action(**kwargs)

def get_circle_base(**kwargs):
    # MIGRATED → components/circle_base/
    from components.circle_base.working import action
    return action(**kwargs)

# gear
def get_gear(**kwargs):



    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    diameter = kwargs.get("diameter", 1)    
    width = diameter
    height = diameter   
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)
    shaft = kwargs.get("shaft", "m6")
        
    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)    
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    


    #if diameter is an array
    if isinstance(diameter, list):
        return get_gear_double_stack(**kwargs)

    kwargs.pop("size","")
    diameter = int(diameter)
    kwargs["diameter"] = diameter
    width = int(width)
    height = int(height)

    th.append(oobb_base.get_comment("gear main","p"))
    # add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"   
    p3["shape"] = f"gear"
    p3["diametral_pitch"] = 0.53333333
    p3["number_of_teeth"] = width * 8     
    if isinstance(width, list):
        p3["number_of_teeth"] = []
        for w in width:
            p3["number_of_teeth"].append(w * 8)
    p3["depth"] = thickness
    p3["pos"] = pos
    #p3["m"] = ""  
    oobb_base.append_full(thing,**p3)      
    
    
    # add holes
    if holes:
        th.append(oobb_base.get_comment("holes main","n"))
        p3 = copy.deepcopy(kwargs)
        #if diameter rounded is even
        if math.floor(diameter) % 2 == 0 or diameter == 1.5:
            p3["diameter"] = diameter - 0.5
            p3["width"] = width - 0.5
            p3["height"] = height - 0.5
        p3["type"] = "n"
        p3["shape"] = f"{size}_holes"
        p3["width"] = width
        p3["height"] = height
        p3["pos"] = pos
        p3["both_holes"] = both_holes
        p3["circle"] = True
        p3["middle"] = False
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)      
        #th.extend(oobb_base.oobb_easy(**p3))   
    
    # shaft
    p3 = copy.deepcopy(kwargs)
    p3["thing"] = thing

    add_oobb_shaft(**p3)
    # shaft
    """
    if shaft == "":
        shaft = "m6"
    if shaft.startswith("m6") or shaft.startswith("m3"):
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"{size}_hole"
        p3["radius_name"] = shaft.split("_")[0]      
        pos1 = copy.deepcopy(pos)        
        p3["pos"] = pos1
        #p3["m"] = "#"  
        oobb_base.append_full(thing,**p3)
    else:
        p3 = copy.deepcopy(kwargs)
        p3.pop("extra","")
        p3["type"] = "n"
        p3["shape"] = f"oobb_{shaft}"     
        p3["part"] = "shaft"   
        pos1 = copy.deepcopy(pos)        
        
        
        if shaft == "motor_servo_standard_01":
            p3["rot"] = [0,0,45]
            pos1[2] += 2
            p3["overhang"] = False
        elif shaft == "motor_tt_01":            
            pos1[2] -= 1
            
        p3["pos"] = pos1
        p3["m"] = "#"  
        oobb_base.append_full(thing, **p3)
    """
        
    # if grub screw
    if "grubscrew" in shaft:
        #get grubscrew size split based on _ and it's the one after "grubscrew"
        grubscrew_list = shaft.split("_")
        size_grubscrew = "m3"
        for i, s in enumerate(grubscrew_list):
            if s == "grubscrew":
                size_grubscrew = grubscrew_list[i+1]
                break
        #add raised hub
        #add the hole
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"{size}_hole"
        p3["radius_name"] = size_grubscrew
        depth = 100
        p3["depth"] = depth
        pos1 = copy.deepcopy(pos)
        pos1[2] += thickness/2
        p3["pos"] = pos1
        p3["rot"] = [0,90,45]
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

        p4 = copy.deepcopy(p3)
        p4.pop("extra","")
        p4.pop("depth","")
        p4["shape"] = f"{size}_nut"
        pos1 = copy.deepcopy(p3["pos"])    
        dist = 3    
        pos1[0] += dist
        pos1[1] += dist
        posa = copy.deepcopy(pos1)
        posa[2] += 3
        posb = copy.deepcopy(pos1)
        posb[2] += 6
        p4["pos"] = [pos1,posa,posb]
        #p4["m"] = "#"
        
        



        #add raised hub




    if full_object:   
        return thing
    else: # only return the elements
        return th

def add_oobb_shaft(**kwargs):
    return _shared_add_oobb_shaft(**kwargs)

def get_gear_double_stack(**kwargs):

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    diameter = kwargs.get("diameter", 1)    
    width = diameter
    height = diameter   
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)
    shaft = kwargs.get("shaft", "m6")
        
    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)    
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size","")

    pos_gear = [0,0,0]
    holes = True
    for i in range(0,len(diameter)):    
        p3 = copy.deepcopy(kwargs)
        p3["full_object"] = False
        p3["thickness"] = thickness/2
        p3["diameter"] = int(diameter[i])
        p3["pos"] = pos_gear
        #p3["holes"] = holes
        p3["both_holes"] = False
        p3["extra"] = extra[i]
        th.append(oobb_base.get_thing_from_dict(p3))
        pos_gear[2] += thickness / 2
        holes = True


    if full_object:   
        return thing
    else: # only return the elements
        return th

# holder
def get_holder(**kwargs):
    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    p3.pop("extra")
    p3["type"] = f'holder_{extra}'
    if extra != "":
        # Get the module object for the current file
        current_module = __import__("oobb_get_items_oobb_holder")
        function_name = "get_holder_" + extra
        # Call the function using the string variable
        try:
            function_to_call = getattr(current_module, function_name)
            return function_to_call(**kwargs)
        except:
            if "get_holder" in function_name:
                import oobb_get_items_oobb_holder_electronic
                p4 = copy.deepcopy(kwargs)
                p4["hole_sides"] = ["left","right","top","bottom"]
                p4["include_connecting_screws"] = False
                p4["pos_plate"] = [0,0,1.5]
                return oobb_get_items_oobb_holder_electronic.get_holder_electronic_base(**p4)
        
    else:
        Exception("No extra")

# holder
def get_other(**kwargs):
    from components.others.working import action

    return action(**kwargs)

# plate
def get_plate(**kwargs):
    from components.plates.working import action

    return action(**kwargs)

def get_plate_base(**kwargs):
    # MIGRATED → components/plate_base/
    from components.plate_base.working import action
    return action(**kwargs)

def get_plate_l(**kwargs):

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)    
    kwargs["pos"] = pos
    
    

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size","")

    #get the width plate
    p3 = copy.deepcopy(kwargs)
    pos1 = copy.deepcopy(pos)
    shift_x = 0
    shift_y = 0
    shift_z = 0
    pos1 = [pos1[0] + shift_x, pos1[1] + shift_y, pos1[2] + shift_z]
    p3["pos"] = pos1
    p3["type"] = "plate"
    p3["width"] = width
    p3["height"] = 1
    p3["full_object"] = False
    p3.pop("extra","")
    width_plate = oobb_base.get_thing_from_dict(p3)
    th.append(width_plate)

    p3 = copy.deepcopy(p3)
    pos1 = copy.deepcopy(pos)
    shift_x = -(width-1)/2 * 15
    shift_y = (height-1)/2 * 15
    shift_z = 0
    pos1 = [pos1[0] + shift_x, pos1[1] + shift_y, pos1[2] + shift_z]
    p3["pos"] = pos1
    p3["width"] = 1
    p3["height"] = height
    height_plate = oobb_base.get_thing_from_dict(p3)
    th.append(height_plate)
    
    
    if full_object:   
        return thing
    else: # only return the elements
        return th

def get_plate_label(**kwargs):
    # MIGRATED → components/plate_label/
    from components.plate_label.working import action
    return action(**kwargs)


def get_plate_ninety_degree(**kwargs):
    # MIGRATED → components/plate_ninety_degree/
    from components.plate_ninety_degree.working import action
    return action(**kwargs)

def get_plate_t(**kwargs):

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)    
    kwargs["pos"] = pos
    
    

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size","")

    #get the width plate
    p3 = copy.deepcopy(kwargs)
    pos1 = copy.deepcopy(pos)
    shift_x = 0
    shift_y = 0
    shift_z = 0
    pos1 = [pos1[0] + shift_x, pos1[1] + shift_y, pos1[2] + shift_z]
    p3["pos"] = pos1
    p3["type"] = "plate"
    p3["width"] = width
    p3["height"] = 1
    p3["full_object"] = False
    p3.pop("extra","")
    width_plate = oobb_base.get_thing_from_dict(p3)
    th.append(width_plate)

    #get the
    p3 = copy.deepcopy(p3)
    pos1 = copy.deepcopy(pos)
    shift_x = 0 # -(width-1)/2 * 15
    shift_y = (height-1)/2 * 15
    shift_z = 0
    pos1 = [pos1[0] + shift_x, pos1[1] + shift_y, pos1[2] + shift_z]
    p3["pos"] = pos1
    p3["width"] = 1
    p3["height"] = height
    height_plate = oobb_base.get_thing_from_dict(p3)
    th.append(height_plate)
    
    
    if full_object:   
        return thing
    else: # only return the elements
        return th

def get_plate_u(**kwargs):

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)    
    kwargs["pos"] = pos
    
    

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size","")

    #get the l plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "plate"
    p3["width"] = width
    p3["height"] = height
    p3["full_object"] = False
    p3["extra"] = "l"
    width_plate = oobb_base.get_thing_from_dict(p3)
    th.append(width_plate)

    #get the extra arm
    p3 = copy.deepcopy(p3)
    pos1 = copy.deepcopy(pos)
    shift_x = (width-1)/2 * 15
    shift_y = 0
    shift_z = 0
    pos1 = [pos1[0] + shift_x, pos1[1] + shift_y, pos1[2] + shift_z]
    p3["pos"] = pos1
    p3["width"] = 1
    p3["height"] = height
    height_plate = oobb_base.get_thing_from_dict(p3)
    th.append(height_plate)
    
    if full_object:   
        return thing
    else: # only return the elements
        return th

def get_plate_u_double(**kwargs):

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)    
    kwargs["pos"] = pos
    
    

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size","")

    #get the l plate
    p3 = copy.deepcopy(kwargs)
    p3.pop("extra","")
    p3["type"] = "plate"
    p3["width"] = 1
    p3["height"] = height
    p3["full_object"] = False
    pos1 = copy.deepcopy(pos)
    pos1[0] += -(width-1)/2 * 15
    pos2 = copy.deepcopy(pos)
    pos2[0] += (width-1)/2 * 15
    poss = []
    poss.append(pos1)
    poss.append(pos2)
    p3["pos"] = poss
    width_plate = oobb_base.get_thing_from_dict(p3)
    th.append(width_plate)

    #get the bottom arm
    p3 = copy.deepcopy(p3)
    pos1 = copy.deepcopy(pos)
    shift_x = 0
    shift_y = (height)/2 * 15 - 15
    shift_z = 0
    pos1 = copy.deepcopy(pos)
    pos1[0] += shift_x
    pos1[1] += shift_y
    pos1[2] += shift_z
    p3["pos"] = pos1
    p3["width"] = width
    p3["height"] = 2
    height_plate = oobb_base.get_thing_from_dict(p3)
    th.append(height_plate)

    if full_object:   
        return thing
    else: # only return the elements
        return th


# pulley_gt2
def get_pulley_gt2(**kwargs):

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    diameter = kwargs.get("diameter", 1)
    bearing = kwargs.get("bearing", "")

    width = diameter
    height = diameter   
    thickness = kwargs.get("thickness", 3)
    thickness_extra = kwargs.get("thickness_extra", 0.5)
    thickness = thickness + thickness_extra
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    shaft = kwargs.get("shaft", "m6")
    shield = False    
    if "shield" in extra:
        shield = True    

    if "double" in extra:
        return get_pulley_gt2_shield_double(**kwargs)
    
    
    teeth = int(extra.replace("_teeth","").replace("_shield","").replace("_double",""))
    full_object = kwargs.get("full_object", True)
    thickness_shield = 1
    thickness_belt = 6
    thickness = thickness + thickness_shield * 2

    #figuring out diameter
    diameter_pulley = (teeth * 2)/3.14
    diameter = math.ceil((diameter_pulley-10) / 15)
    kwargs["diameter"] = diameter

    screws_connecting = False
    if shield and teeth >= 40:
        screws_connecting = True
    if bearing != "":
        screws_connecting = True


    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)    
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size","")

    th.append(oobb_base.get_comment("gear main","p"))
    # add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"   
    p3["shape"] = f"pulley_gt2"
    p3["number_of_teeth"] = teeth
    p3["depth"] = thickness
    pos1 = copy.deepcopy(pos)
    pos1[2] += -thickness/2
    p3["pos"] = pos1
    #p3["m"] = ""  
    oobb_base.append_full(thing,**p3)      
    
    #add shields
    if shield:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"   
        p3["shape"] = f"oobb_cylinder"
        
        p3["radius"] = diameter_pulley/2+1 #guess needs figuring out
        p3["depth"] = thickness_shield
        pos1 = copy.deepcopy(pos)
        pos1[2] += -thickness/2 + thickness_shield/2
        pos2 = copy.deepcopy(pos)
        pos2[2] += thickness/2 - thickness_shield/2
        poss = []

        poss.append(pos1)
        poss.append(pos2)
        p3["pos"] = poss
        #p3["m"] = "#"  
        oobb_base.append_full(thing,**p3)

    if screws_connecting:     
        shifts = []
        shifts.append(5.303)
        if bearing == "6705":
            shifts.append(13)
        screws = []
        for shift in shifts:                    
            screws.append([-shift,-shift,True])
            screws.append([shift,shift,True])
            screws.append([-shift,shift,False])
            screws.append([shift,-shift,False])
            
        for screw in screws:       
            p3 = copy.deepcopy(kwargs)
            #if diameter rounded is even
            p3["type"] = "n"
            p3["shape"] = f"{size}_screw_countersunk"
            p3["radius_name"] = "m3"
            p3["nut_include"] = True
            p3["depth"] = thickness
            pos1 = copy.deepcopy(pos)
            pos1[0] += screw[0]
            pos1[1] += screw[1]
            pos1[2] += thickness/2
            p3["pos"] = pos1            
            if screw[2]:                
                p3["rot"] = [0,180,0]
                pos1[2] += -thickness
            #p3["m"] = "#"
            oobb_base.append_full(thing,**p3)      
        
        

    # add holes
    if holes:
        th.append(oobb_base.get_comment("holes main","n"))
        p3 = copy.deepcopy(kwargs)
        #if diameter rounded is even
        if math.floor(diameter) % 2 == 0:
            p3["diameter"] = diameter - 0.5
            p3["width"] = width - 0.5
            p3["height"] = height - 0.5
        p3["type"] = "n"
        p3["shape"] = f"{size}_holes"        
        p3["width"] = width
        p3["height"] = height
        p3["pos"] = pos
        p3["both_holes"] = both_holes
        p3["circle"] = True
        p3["middle"] = False
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)      
        #th.extend(oobb_base.oobb_easy(**p3)) 
        if diameter == 2:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "n"
            p3["shape"] = f"oobb_hole"
            p3["radius_name"] = "m3"
            #p3["depth"] = thickness
            poss = []
            pos1 = copy.deepcopy(pos)
            pos1[0] += 7.5
            pos1[1] += 0            
            poss.append(pos1)
            pos1 = copy.deepcopy(pos)
            pos1[0] += -7.5
            pos1[1] += 0
            poss.append(pos1)
            pos1 = copy.deepcopy(pos)
            pos1[0] += 0
            pos1[1] += 7.5
            poss.append(pos1)
            pos1 = copy.deepcopy(pos)
            pos1[0] += 0
            pos1[1] += -7.5
            poss.append(pos1)
            p3["pos"] = poss
            #p3["m"] = "#"
            oobb_base.append_full(thing,**p3)



        
    # shaft
    if shaft == "":
        shaft = "m6"
    if shaft.startswith("m6") or shaft.startswith("m3"):
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"{size}_hole"
        p3["radius_name"] = shaft        
        pos1 = copy.deepcopy(pos)        
        p3["pos"] = pos1
        #p3["m"] = "#"  
        oobb_base.append_full(thing,**p3)        
    else:
        p3 = copy.deepcopy(kwargs)
        p3.pop("extra","")
        p3["type"] = "n"
        p3["shape"] = f"oobb_{shaft}"     
        p3["part"] = "shaft"   
        pos1 = copy.deepcopy(pos)        
        
        
        if shaft == "motor_servo_standard_01":
            p3["rot"] = [0,0,45]
            pos1[2] += 2
            p3["overhang"] = False
        p3["pos"] = pos1
        p3["m"] = "#"  
        oobb_base.append_full(thing,**p3)

    
    #bearing 
    if bearing != "":
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_bearing"
        p3["bearing"] = bearing
        poss = []
        pos1 = copy.deepcopy(pos)
        bearing_height_1 = -thickness/2 + thickness_shield + thickness_extra / 2 + thickness_belt / 2
        pos1[2] += bearing_height_1
        pos2 = copy.deepcopy(pos)
        pos2[2] += thickness/2 - thickness_shield - thickness_extra / 2 - thickness_belt / 2
        pos3 = copy.deepcopy(pos)
        pos3[2] += 0
        #poss.append(pos1)
        #poss.append(pos2)
        poss.append(pos3)
        p3["pos"] = poss
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

    # add_slice
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_slice"
    pos1 = copy.deepcopy(pos)
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)
    
    if full_object:   
        return thing
    else: # only return the elements
        return th


def get_pulley_gt2_shield_double(**kwargs):

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    diameter = kwargs.get("diameter", 1)
    bearing = kwargs.get("bearing", "")

    width = diameter
    height = diameter   
    thickness = kwargs.get("thickness", 3)

    thickness_extra = kwargs.get("thickness_extra", 0.5)
    thickness_extra = thickness_extra * 2
    thickness = thickness + thickness_extra
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    shaft = kwargs.get("shaft", "m6")
    shield = False    
    if "shield" in extra:
        shield = True        
    teeth = int(extra.replace("_teeth","").replace("_shield","").replace("_double",""))
    full_object = kwargs.get("full_object", True)
    thickness_shield = 1
    thickness_belt = 6
    thickness = thickness * 2 + thickness_shield * 3

    #figuring out diameter
    diameter_pulley = (teeth * 2)/3.14
    diameter = math.ceil((diameter_pulley-10) / 15)
    kwargs["diameter"] = diameter

    screws_connecting = False
    if shield and diameter > 2:
        screws_connecting = True
    if bearing != "":
        screws_connecting = True


    # extra sets
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", True)    
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size","")

    th.append(oobb_base.get_comment("gear main","p"))
    # add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"   
    p3["shape"] = f"pulley_gt2"
    p3["number_of_teeth"] = teeth
    p3["depth"] = thickness
    pos1 = copy.deepcopy(pos)
    pos1[2] += -thickness/2
    p3["pos"] = pos1
    #p3["m"] = ""  
    oobb_base.append_full(thing,**p3)      
    
    #add shields
    if shield:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"   
        p3["shape"] = f"oobb_cylinder"
        
        p3["radius"] = diameter_pulley/2+1 #guess needs figuring out
        p3["depth"] = thickness_shield
        pos1 = copy.deepcopy(pos)
        pos1[2] += -thickness/2 + thickness_shield/2
        pos2 = copy.deepcopy(pos)
        pos2[2] += 0
        pos3 = copy.deepcopy(pos)
        pos3[2] += thickness/2 - thickness_shield/2
        poss = []

        poss.append(pos1)
        poss.append(pos2)
        poss.append(pos3)
        p3["pos"] = poss
        #p3["m"] = "#"  
        oobb_base.append_full(thing,**p3)

    if screws_connecting:     
        shifts = []
        shifts.append(5.303)
        if bearing == "6705":
            shifts.append(13)
        screws = []
        for shift in shifts:                    
            screws.append([-shift,-shift,True])
            screws.append([shift,shift,True])
            screws.append([-shift,shift,False])
            screws.append([shift,-shift,False])
            
        for screw in screws:       
            p3 = copy.deepcopy(kwargs)
            #if diameter rounded is even
            p3["type"] = "n"
            p3["shape"] = f"{size}_screw_countersunk"
            p3["radius_name"] = "m3"
            p3["nut_include"] = True
            p3["depth"] = thickness
            pos1 = copy.deepcopy(pos)
            pos1[0] += screw[0]
            pos1[1] += screw[1]
            pos1[2] += thickness/2
            p3["pos"] = pos1            
            if screw[2]:                
                p3["rot"] = [0,180,0]
                pos1[2] += -thickness
            #p3["m"] = "#"
            oobb_base.append_full(thing,**p3)      
        
        

    # add holes
    if holes:
        th.append(oobb_base.get_comment("holes main","n"))
        p3 = copy.deepcopy(kwargs)
        #if diameter rounded is even
        if math.floor(diameter) % 2 == 0:
            p3["diameter"] = diameter - 0.5
            p3["width"] = width - 0.5
            p3["height"] = height - 0.5
        p3["type"] = "n"
        p3["shape"] = f"{size}_holes"        
        p3["width"] = width
        p3["height"] = height
        p3["pos"] = pos
        p3["both_holes"] = both_holes
        p3["circle"] = True
        p3["middle"] = False
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)      
        #th.extend(oobb_base.oobb_easy(**p3))   
        
    # shaft
    if shaft == "":
        shaft = "m6"
    if shaft.startswith("m6") or shaft.startswith("m3"):
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"{size}_hole"
        p3["radius_name"] = shaft        
        pos1 = copy.deepcopy(pos)        
        p3["pos"] = pos1
        #p3["m"] = "#"  
        oobb_base.append_full(thing,**p3)        
    else:
        p3 = copy.deepcopy(kwargs)
        p3.pop("extra","")
        p3["type"] = "n"
        p3["shape"] = f"oobb_{shaft}"     
        p3["part"] = "shaft"   
        pos1 = copy.deepcopy(pos)        
        
        
        if shaft == "motor_servo_standard_01":
            p3["rot"] = [0,0,45]
            pos1[2] += 2
            p3["overhang"] = False
        p3["pos"] = pos1
        p3["m"] = "#"  
        oobb_base.append_full(thing,**p3)

    
    #bearing 
    if bearing != "":
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_bearing"
        p3["bearing"] = bearing
        poss = []
        pos1 = copy.deepcopy(pos)
        bearing_height_1 = -thickness/2 + thickness_shield + thickness_extra / 2 + thickness_belt / 2
        pos1[2] += bearing_height_1
        pos2 = copy.deepcopy(pos)
        pos2[2] += thickness/2 - thickness_shield - thickness_extra / 2 - thickness_belt / 2
        pos3 = copy.deepcopy(pos)
        pos3[2] += 0
        #poss.append(pos1)
        #poss.append(pos2)
        poss.append(pos3)
        p3["pos"] = poss
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

    # add_slice
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_slice"
    pos1 = copy.deepcopy(pos)
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)
    
    if full_object:   
        return thing
    else: # only return the elements
        return th


def get_shaft_center(thing, **kwargs):
    return _shared_get_shaft_center(thing, **kwargs)

# test    
def get_test(**kwargs):
    from components.tests.working import action

    return action(**kwargs)

# wheel
def get_wheel(**kwargs):
    from components.wheels.working import action

    return action(**kwargs)
    

# wire
def get_wire(**kwargs):
    from components.wires.working import action

    return action(**kwargs)