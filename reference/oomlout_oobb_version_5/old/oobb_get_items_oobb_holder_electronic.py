import copy
import oobb_base
import oobb_get_items_oobb
from oobb_arch.helpers.component_helpers import (
    get_plate_cutout_dict as _shared_get_plate_cutout_dict,
    get_plate_screw_dict as _shared_get_plate_screw_dict,
)


# battery_box
def get_holder_electronic_battery_box_aa_battery_4_cell(**kwargs):
    thickness = kwargs.get("thickness", 3)
    pos_item = [6,0,0]
    kwargs["pos_item"] = pos_item  
    kwargs["pos_plate"] = [0,7.5,0]  
    
    p3 = copy.deepcopy(kwargs)
    p3["hole_sides"] = ["right", "top"]
    p3["include_connecting_screws"] = False
    p3["include_cutout"] = False
    p3["include_nut"] = True
    return_value = get_holder_electronic_base(**p3)

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = "oobb_cylinder"
    p3["radius"] = 16/2
    p3["depth"] = 15    
    p3["zz"] = "bottom"
    p3.pop("size","")
    #p3["m"] = "#"
    #oobb_base.append_full(return_value, **p3)


    return return_value


#button
def get_holder_electronic_button_11_mm_panel_mount(**kwargs):
    thickness = kwargs.get("thickness", 3)
    pos_item = [0,0,-1.5]
    if thickness == 3:
        pos_item[2] += 18 - 3
    kwargs["pos_item"] = pos_item    
    return_value = get_holder_electronic_base(**kwargs)
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = "oobb_cylinder"
    p3["radius"] = 16/2
    p3["depth"] = 15    
    p3["zz"] = "bottom"
    p3.pop("size","")
    #p3["m"] = "#"
    oobb_base.append_full(return_value, **p3)


    return return_value

def get_holder_electronic_button_11_mm_panel_mount_x4(**kwargs):
    pos_item = []    
    spacing = 6
    pos_item.append([-spacing, spacing, -1.5])
    pos_item.append([spacing, spacing, -1.5])
    pos_item.append([-spacing, -spacing, -1.5])
    pos_item.append([spacing, -spacing, -1.5])
    kwargs["pos_item"] = pos_item    
    return get_holder_electronic_base(**kwargs)


# potentiometer
def get_holder_electronic_potentiometer_17_mm(**kwargs):
    pos_item = [0,0,-1.5]
    kwargs["pos_item"] = pos_item
    rot_item = [0,0,90]
    kwargs["rot_item"] = rot_item
    return get_holder_electronic_base(**kwargs)

def get_holder_electronic_potentiometer_stick_single_axis_16_mm(**kwargs):
    pos_item = [0,0,-1.5]
    kwargs["pos_item"] = pos_item
    rot_item = [0,0,0]
    kwargs["rot_item"] = rot_item
    return get_holder_electronic_base(**kwargs)

    
def get_holder_electronic_potentiometer_stick_single_axis_16_mm_arm(**kwargs):
    shift_hole = -4
    
    thickness = kwargs.get("thickness", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    pos_item = kwargs.get("pos_item", [-6+shift_hole, 0, -16/2 - thickness / 2])
    rot_item = kwargs.get("rot_item", [0, 90, 0])
    extra = kwargs.get("extra", "") .replace("_arm","")
    full_object = kwargs.get("full_object", True)
    width = kwargs.get("width", 3)
    
    

    thing = oobb_base.get_default_thing(**kwargs)
    
    kwargs.pop("size","")   
    #remove _x# from kwargs extra
    for i in range(10):
        extra = extra.replace(f"_x{i}","") 

    # servo shaft at 0,0,0 position
    
    x = (width-1)/2*15
    y = 0
    z = -thickness/2
    pos_plate = [x,y,z]
    pos_plate = [pos_plate[0] + pos[0], pos_plate[1] + pos[1], pos_plate[2] + pos[2]]
    kwargs["pos_plate"] =  pos_plate

    # plate
    p3 = copy.deepcopy(kwargs)
    p3 = oobb_get_items_oobb.get_plate_dict(**p3)    
    oobb_base.append_full(thing, **p3)

    # cube for lockiong in
    p3 = copy.deepcopy(kwargs)
    pos1 = copy.deepcopy(pos)
    shift_x = 11
    shift_y = 0
    shift_z = -8
    pos1 = [pos1[0] + shift_x, pos1[1] + shift_y, pos1[2] + shift_z]
    p3["type"] = "positive" 
    p3["shape"] = f"oobb_cube_center"  
    p3["size"] = [10,5,15]
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing, **p3)

    # hole    
    # shaft hole
    p3 = copy.deepcopy(kwargs)
    pos1 = copy.deepcopy(pos)
    pos1[0] += shift_hole
    p3["type"] = "negative" 
    p3["shape"] = f"oobb_hole"  
    p3["radius_name"] = "m2d5"
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing, **p3)
    
    #      oobb_holes
    locs = []
    locs.append([3,1])
    locs.append([2,1])
    p3 = copy.deepcopy(kwargs)
    pos1 = copy.deepcopy(pos_plate)
    p3["type"] = "negative" 
    p3["shape"] = f"oobb_holes"  
    p3["holes"] = "single"
    p3["loc"] = locs
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing, **p3)
    locs = []
    locs.append([2.5,1])
    p4 = copy.deepcopy(p3)
    p4["loc"] = locs
    p4["radius_name"] = "m3"
    oobb_base.append_full(thing, **p4)
    
    

    # item    
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative" 
    p3["shape"] = f"oobb_{extra}"  
    p3["pos"] = pos_item
    p3["rot"] = rot_item
    p3["width_stick"] = 10
    #p3["m"] = "#"
    oobb_base.append_full(thing, **p3)

    
    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]


def get_holder_electronic_base(**kwargs):
    thickness = kwargs.get("thickness", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    pos_item = kwargs.get("pos_item", [0, 0, 0])
    rot_item = kwargs.get("rot_item", [0, 0, 0])
    hole_sides = kwargs.get("hole_sides", ["left","right","top"])
    extra = kwargs.get("extra", "")    
    full_object = kwargs.get("full_object", True)
    part = kwargs.get("part", "all")
    pos_plate = kwargs.get("pos_plate", [0, 0, 0])
    include_connecting_screws = kwargs.get("include_connecting_screws", True)
    include_cutout = kwargs.get("include_cutout", True)
    include_hole = kwargs.get("include_hole", True)
    

    thing = oobb_base.get_default_thing(**kwargs)
    
    kwargs.pop("size","")   
    #remove _x# from kwargs extra
    for i in range(10):
        extra = extra.replace(f"_x{i}","") 

    # servo shaft at 0,0,0 position
    
    pos_plate_shift = [0,0,-thickness]
    pos_plate = [pos_plate[0] + pos_plate_shift[0], pos_plate[1] + pos_plate_shift[1], pos_plate[2] + pos_plate_shift[2]]
    kwargs["pos_plate"] =  pos_plate

    # plate
    p3 = copy.deepcopy(kwargs)
    p3 = oobb_get_items_oobb.get_plate_dict(**p3)    
    oobb_base.append_full(thing, **p3)

    # cutout
    if include_cutout:
        if thickness != 3:
            p3 = copy.deepcopy(kwargs)
            p3 = get_plate_cutout_dict(**p3)
            #p3["m"] = "#"
            oobb_base.append_full(thing, **p3)

    # hole    
    if include_hole:
        p3 = copy.deepcopy(kwargs)
        p3["hole_sides"] = hole_sides
        p3["both_holes"] = True
        p3.pop("diameter","")
        p3 = oobb_get_items_oobb.get_plate_hole_dict(**p3)
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)

    # screw
    if include_connecting_screws:
        p3 = get_plate_screw_dict(**kwargs)
        p3["type"] = "negative"
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)

    # item    
    try:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative" 
        p3["shape"] = f"oobb_{extra}"  
        p3["pos"] = pos_item
        p3["rot"] = rot_item
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)
    except Exception as e:
        print("insertion item not found in oobb_get_items_oobb_holder_electronic")
        print(e)

    
    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]




def get_plate_cutout_dict(**kwargs):
    return _shared_get_plate_cutout_dict(**kwargs)



def get_plate_screw_dict(**kwargs):
    return _shared_get_plate_screw_dict(**kwargs)