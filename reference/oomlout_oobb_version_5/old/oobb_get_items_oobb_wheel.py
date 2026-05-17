import copy
import oobb_base
import oobb_get_items_oobb_old

def get_wheel_no_tire(**kwargs):
    return get_wheel(**kwargs)

def get_wheel(**kwargs):
    bearing = kwargs.get("bearing", "")
    extra = kwargs.get("extra", "")
    connecting_screws = kwargs.get("connecting_screws", False)
    thickness = kwargs.get("thickness", 3)
    oring_type = kwargs.get("oring_type", "")
    pos = kwargs.get("pos", [0,0,0])
    pos_plate = kwargs.get("pos_plate", [0,0,0])
    pos_plate[0] += pos[0]
    pos_plate[1] += pos[1]
    pos_plate[2] += pos[2]
    #figuring out radius
    minus_bit = 1.5
    if oring_type != "": #if no oring
        od = oobb_base.gv(f"oring_{oring_type}_od", "true")
        id = oobb_base.gv(f"oring_{oring_type}_id", "true")
        idt = oobb_base.gv(f"oring_{oring_type}_id_tight", "true")            
        radius = idt + (od-id)/2 + 0.5 - minus_bit #(to account for the minusing) 
        diameter_big = radius*2/oobb_base.gv("osp")
        diameter = int(round(diameter_big, 0))
        if diameter % 2 == 0:
            diameter -= 1
    else:
        diameter = kwargs.get("diameter", 3)
        diameter_big = diameter
        radius = (diameter * 15 - 1)/2
    
    #if diameter is even take one off to make it odd
    

    kwargs.update({"diameter": diameter})
    thing = oobb_base.get_default_thing(**kwargs)    
    
    kwargs.update({"diameter": diameter_big})
    
    kwargs.pop("size","")
    
    #circle
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = "oobb_circle"
    p3["depth"] = thickness
    p3["radius"] = radius
    p3["pos"] = pos
    p3["zz"] = "middle"
    #p3["m"] = "#"
    oobb_base.append_full(thing, **p3)

    
    #holes
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = "oobb_holes"
    p3["diameter_center_clearance"] = 15
    p3["circle"] = True
    p3["both_holes"] = True
    #p3["m"] = "#"
    oobb_base.append_full(thing, **p3)

    #oring
    if extra != "no_tire":
        if oring_type != "":
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "negative"
            p3["shape"] = "oobb_oring"
            p3["oring_type"] = oring_type
            #p3["m"] = "#"
            oobb_base.append_full(thing, **p3)
        else:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "negative"
            p3["shape"] = "oobb_tire"
            radius_tube = 5
            p3["depth"] = radius_tube
            p3["id"] = radius - radius_tube/2
            #p3["m"] = "#"
            oobb_base.append_full(thing, **p3)

    
    #bearing 
    if bearing != "":
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = "oobb_bearing"
        if diameter_big == 1.75:
            p3["clearance"] = "top"
        p3["bearing"] = bearing
        p3["m"] = "#"
        oobb_base.append_full(thing, **p3)
        connecting_screws = True

    #connecting_screws
    if connecting_screws:
        import oobb_get_items_oobb_bearing_plate
        oobb_get_items_oobb_bearing_plate.get_bearing_plate_connecting_screw_perimeter(thing = thing, **kwargs)
        

    if bearing != "" and diameter_big != 1.75:
        #add second side
        #shift coomponents to the right and down half thickness
        components_second = copy.deepcopy(thing["components"])

        #put into a rotation object
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += diameter * 15 + 15
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        return_value_2 = [return_value_2]

        thing["components"] = thing["components"] + return_value_2

        #slice
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = "oobb_slice"
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)


    return thing

def get_wheel_bearing(**kwargs):
    return oobb_get_items_oobb_old.get_wheel_old_1(**kwargs)

def get_wheel_bearing_twenty_twenty_aluminium_extrusion(**kwargs):
    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    diameter = kwargs.get("diameter", 20)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)
    bearing = kwargs.get("bearing", "606")
        
    # extra sets
    kwargs["pos"] = pos
    
    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size","")
    kwargs.pop("type","")

    pos_plate = [0,0,-thickness/2]
    pos_plate[0] = pos[0] + pos_plate[0]
    pos_plate[1] = pos[1] + pos_plate[1]
    pos_plate[2] = pos[2] + pos_plate[2]
    kwargs["pos_plate"] = pos_plate

    # plate
    p3 = copy.deepcopy(kwargs)
    pos1 = copy.deepcopy(pos)
    p3["type"] = "positive"
    p3["shape"] = "oobb_cylinder"  
    depth_middle = 6
    p3["depth"] = depth_middle
    p3["radius"] = diameter/2
    pos1[2] += 0
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing, **p3)
    
    # core the middle
    p3 = copy.deepcopy(kwargs)
    pos1 = copy.deepcopy(pos)
    p3["type"] = "negative"
    p3["shape"] = "oobb_hole"  
    p3["radius"] = 5
    #p3["m"] = "#"
    oobb_base.append_full(thing, **p3)


    # cones
    p3 = copy.deepcopy(kwargs)
    pos1 = copy.deepcopy(pos)
    p3["type"] = "positive"
    p3["shape"] = "oobb_cylinder"
    r_big = (diameter)/2
    r_little = r_big - 8/2
    p3["r1"] = r_big
    p3["r2"] = r_little
    dep = (thickness - depth_middle) / 2    
    p3["depth"] = dep
    pos1[2] = pos1[2] + dep/2  + depth_middle / 2
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing, **p3)

    p4 = copy.deepcopy(p3)
    p4["r1"] = p3["r2"]
    p4["r2"] = p3["r1"]
    pos1 = copy.deepcopy(pos)
    pos1[2] = pos1[2] - dep/2  - depth_middle / 2
    p4["pos"] = pos1
    #p4["m"] = "#"
    oobb_base.append_full(thing, **p4)

    # bearings
    pos1 = copy.deepcopy(pos)
    pos1[2] += thickness/2    
    p3 = copy.deepcopy(kwargs)    
    p3["type"] = "negative"
    p3["shape"] = "oobb_bearing"
    p3["bearing"] = bearing
    p3["zz"] = "top"    
    p3["pos"] = pos1
    p3["m"] = "#"
    oobb_base.append_full(thing, **p3)

    p4 = copy.deepcopy(p3)
    pos2 = copy.deepcopy(pos)
    pos2[2] += -thickness/2
    p4["pos"] = pos2
    p4["zz"] = "bottom"    
    #p4["m"] = "#"
    oobb_base.append_full(thing, **p4)
    
    # slice at 0
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = "oobb_slice"
    oobb_base.append_full(thing, **p3)

    if full_object:   
        return thing
    else: # only return the elements
        return th

