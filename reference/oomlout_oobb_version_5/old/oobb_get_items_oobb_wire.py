import copy
import oobb_base
import oobb_get_items_oobb
from oobb_arch.helpers.component_helpers import (
    get_plate_nut_dict as _shared_get_plate_nut_dict,
)



# basic
def get_wire_basic(**kwargs):
    return get_oobb_wire_base(**kwargs)

def get_wire_basic_basic_basic(**kwargs):
    return get_oobb_wire_base(**kwargs)

def get_wire_basic_basic_basic_basic(**kwargs):
    return get_oobb_wire_base(**kwargs)

def get_wire_higher_voltage(**kwargs):
    return get_oobb_wire_base(**kwargs)

def get_wire_higher_voltage_basic_basic_motor_stepper(**kwargs):
    return get_oobb_wire_base(**kwargs)

def get_wire_higher_voltage_motor_stepper(**kwargs):
    return get_oobb_wire_base(**kwargs)

def get_wire_i2c(**kwargs):
    return get_oobb_wire_base(**kwargs)

def get_wire_motor(**kwargs):
    return get_oobb_wire_base(**kwargs)

def get_wire_motor_basic(**kwargs):
    return get_oobb_wire_base(**kwargs)


def get_wire_basic_basic_motor(**kwargs):
    return get_oobb_wire_base(**kwargs)



def get_wire_motor_stepper(**kwargs):
    return get_oobb_wire_base(**kwargs)

def get_wire_spacer(**kwargs):
    return get_oobb_wire_base(**kwargs)
    
def get_wire_spacer_long(**kwargs):
    return get_oobb_wire_base(**kwargs)
    
def get_wire_spacer_u(**kwargs):
    return get_oobb_wire_base(**kwargs)


# generic
def get_oobb_wire_base(**kwargs):
    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    extra_mm = False
    if "extra_mm" in extra:
        extra_mm = True
        extra = extra.replace("_extra__mm","")
    full_object = kwargs.get("full_object", True)
        
    # extra sets
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size","")
    kwargs.pop("type","")

    pos_plate = [0,0,-thickness]
    pos_plate[0] = pos[0] + pos_plate[0]
    pos_plate[1] = pos[1] + pos_plate[1]
    pos_plate[2] = pos[2] + pos_plate[2]
    kwargs["pos_plate"] = pos_plate

    # plate
    p3 = copy.deepcopy(kwargs)
    if extra_mm:
        p3["width"] = width + 1/15
        p3["height"] = height + 1/15
    p3 = oobb_get_items_oobb.get_plate_dict(**p3) 
    if thickness == 9:
        p3["pos"][2] += 3
    oobb_base.append_full(thing, **p3)

    # hole    
    p3 = copy.deepcopy(kwargs)
    p3["hole_sides"] = ["left","right","top"]
    if width == 2:
        p3["hole_sides"] = ["left","right"]
    p3 = oobb_get_items_oobb.get_plate_hole_dict(**p3)
    #p3["m"] = "#"
    oobb_base.append_full(thing, **p3)

    # captive nuts
    if thickness > 3:
        p3 = copy.deepcopy(kwargs)
        p3 = get_plate_nut_dict(**p3)
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)
    
    depth_universal = 2.6
    # cutout
    z_shift = -depth_universal    
    if type(extra) is not list:
        extras = [extra]
    else:
        extras = extra
    for extra in extras:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"oobb_wire_{extra}"
        p3["rot"] = [0,0,180]
        x_shift = -(3-width) * 15
        if x_shift != 0:
            x_shift += 7.5
        p3["pos"][0] += x_shift
        p3["pos"][2] += z_shift
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)
        z_shift += -depth_universal 


    if full_object:   
        return thing
    else: # only return the elements
        return th

# helpers
def get_plate_nut_dict(**kwargs):
    return _shared_get_plate_nut_dict(**kwargs)

