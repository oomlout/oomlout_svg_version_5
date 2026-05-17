import copy

import oobb_base
from oobb_get_items_oobb_old import *



def get_bearing_plate(**kwargs):

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb");
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)
    just_screws = kwargs.get("just_screws", False)
    screws = []

    # extra sets
    shaft = kwargs.get("shaft", "m6")
    radius_name = kwargs.get("radius_name", "m6")
    bearing = kwargs.get("bearing", "608")
    
    micro_servo = kwargs.get("micro_servo", False)
    extra = kwargs.get("extra", "") 

    #deal with old style ones everything that isnt 6704 currently

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")
    #kwargs.pop("bearing", "")


    # plate     
    if not just_screws:
        pos_plate = [0,0,0]
        if extra == "shifted":
            pos_plate[1] = pos_plate[1] + 15/2
        kwargs["pos_plate"] = pos_plate
        get_bearing_plate_plate(thing, **kwargs)
            
    # bearing
    if not just_screws:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative" 
        p3["shape"] = f"{size}_bearing"
        p3["bearing"] = bearing
        p3["width"] = width             
        p3["height"] = height  
        p3["depth"] = thickness
        p3["pos"] = pos
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)

    # hole
    #      center
    if not just_screws:
        p3 = copy.deepcopy(kwargs)
        #p3["m"] = "#"
        get_bearing_plate_hole_center(thing,**p3)

    #      perimeter
    if not just_screws:
        p3 = copy.deepcopy(kwargs)
        #p3["m"] = "#"
        get_bearing_plate_hole_perimeter(thing,**p3)

    #      shaft
    if not just_screws:
        p3 = copy.deepcopy(kwargs)
        #p3["m"] = "#"
        get_bearing_plate_hole_shaft(thing,**p3)

    # connecting_screw
    #      perimeter    
    p3 = copy.deepcopy(kwargs)
    #p3["m"] = "#"
    screws.append(get_bearing_plate_connecting_screw_perimeter(thing,**p3))

    #      center
    p3 = copy.deepcopy(kwargs)
    #p3["m"] = "#"
    screws.append(get_bearing_plate_connecting_screw_center(thing,**p3))


    

    # slice section
    if not just_screws:
        z_level = pos[2]
        if extra == "horn_adapter_screws":   
            #z_level = -20 # NO SLIC
            z_level = pos[2]
        elif shaft == "motor_tt_01":
            z_level = pos[2] # NO SLIC
        else: 
            z_level = pos[2]
        
        # extra
        # extra_missing_middle_3_mm
        shift_slice = 0
        if "missing_middle_3_mm" in extra:
            shift_slice = 1.5

        # slices and conditional slices
        if extra == "" or "missing_middle_3_mm"  in extra or "removable" in extra or "sandwich" in extra or shaft == "coupler_flanged" or "no_center" in extra:
            if (shaft == "m6" or shaft == "motor_tt_01" or shaft == "motor_servo_standard_01" or shaft == "coupler_flanged") :
                #shift coomponents to the right and down half thickness
                components_second = copy.deepcopy(thing["components"])

                #put into a rotation object
                return_value_2 = {}
                return_value_2["type"]  = "rotation"
                return_value_2["typetype"]  = "p"
                pos1 = copy.deepcopy(pos)
                pos1[0] += width * 15 + 15
                return_value_2["pos"] = pos1
                return_value_2["rot"] = [180,0,0]
                return_value_2["objects"] = components_second
                return_value_2 = [return_value_2]


                #components_second = oobb_base.shift(components_second, shift = [50, 0 , +thickness/2])
                thing["components"] = thing["components"] + return_value_2
                


                p3 = {}
                p3["type"] = "n"
                p3["shape"] = f"oobb_slice"
                p3["mode"] = "3dpr"
                p3["pos"] = [0,0,thickness/2]
                p3["comment"] = "bearing_plate_slice"
                p3["zz"] = "bottom"
                #p3["m"] = "#"
                oobb_base.append_full(thing, **p3)

            p3 = {}
            p3["type"] = "n"
            p3["shape"] = f"oobb_slice"
            p3["mode"] = "3dpr"
            p3["pos"] = [0,0,z_level + shift_slice]
            p3["comment"] = "bearing_plate_slice"
            p3["zz"] = "top"
            #p3["m"] = "#"
            oobb_base.append_full(thing, **p3)

            if shaft == "coupler_flanged":
                shift_extra_nut = 105
                #add extra nut holder for coupler_flanged
                #create the extra piece for getting the nuts in
                p3 = copy.deepcopy(kwargs)
                p3["type"] = "p"
                p3["shape"] = f"oobb_cylinder"
                pos1 = copy.deepcopy(pos)
                pos1[0] += shift_extra_nut
                dep = 4
                pos1[2] += dep/2
                p3["pos"] = pos1
                p3["radius"] = 22/2
                p3["depth"] = dep
                #p3["m"] = "#"
                oobb_base.append_full(thing, **p3)
                #remvoe 10.5mm hole
                p3 = copy.deepcopy(kwargs)
                p3["type"] = "n"
                p3["shape"] = f"oobb_hole"
                pos1 = copy.deepcopy(pos)
                pos1[0] += shift_extra_nut
                p3["pos"] = pos1
                p3["radius"] = 6/2
                #p3["m"] = "#"
                oobb_base.append_full(thing, **p3)
                shift = 5.657
                hole_positions = []
                z_shift = 0
                hole_positions.append([[shift, shift, z_shift],360/24])
                hole_positions.append([[-shift, -shift, z_shift],360/24])
                hole_positions.append([[shift, -shift, z_shift],-360/24])
                hole_positions.append([[-shift, shift, z_shift],-360/24])
                for posa in hole_positions:
                    p3 = copy.deepcopy(kwargs)
                    p3["type"] = "n"
                    p3["shape"] = "oobb_nut"
                    pos1 = copy.deepcopy(posa[0])
                    pos1[0] += shift_extra_nut
                    p3["pos"] = pos1
                    p3["radius_name"] = "m3"
                    p3["nut"] = True
                    p3["hole"] = True
                    p3["overhang"] = True        
                    p3["rot"] = [0,0,posa[1]]
                    #p3["m"] = "#"
                    oobb_base.append_full(thing, **p3)

        elif extra == "three_quarter":
            thickness_bearing = oobb_base.gv(f'bearing_{bearing}_depth',"3dpr")
            thickness_plate = (thickness - thickness_bearing) / 2
            z_level = thickness/2 - thickness_plate
            p3 = {}
            p3["type"] = "n"
            p3["shape"] = f"oobb_slice"
            p3["mode"] = "3dpr"
            p3["pos"] = [0,0,z_level]
            p3["comment"] = "bearing_plate_slice"
            p3["zz"] = "bottom"
            #p3["m"] = "#"
            oobb_base.append_full(thing, **p3)


    if full_object:   
        return thing
    else: # only return the elements
        return thing["components"]

def get_bearing_plate_connecting_screw_center(thing, **kwargs):
    return_value = []
    # default sets
    thickness = kwargs.get("thickness", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    bearing = kwargs.get("bearing", "6704")
    shaft = kwargs.get("shaft", "m6")

    z = pos[2]+thickness/2

    joint_dis = 15        
    if ( bearing == "6704" or bearing == "6705" or bearing == "6810") and (shaft == "m6" or shaft == "motor_tt_01" or shaft == "motor_servo_standard_01"):
        hole_positions = []
        # 90 degrees
        #hole_positions.append([[0, joint_dis/2, pos[2]+z], [0,0,0]])
        #hole_positions.append([[0, -joint_dis/2, pos[2]+z-thickness], [0,180,0]])
        # 45 degrees
        offset = 5.303
        if bearing == "6810":
            offset = 7.5
        if offset == 5.303:
            hole_positions.append([[offset, offset, pos[2]+z], [0,0,0]])
            hole_positions.append([[-offset, -offset, pos[2]+z-thickness], [0,180,0]])
        else:
            hole_positions.append([[offset, offset, pos[2]+z], [0,0,0]])
            hole_positions.append([[-offset, -offset, pos[2]+z], [0,0,0]])
            hole_positions.append([[offset, -offset, pos[2]+z-thickness], [0,180,0]])
            hole_positions.append([[-offset, offset, pos[2]+z-thickness], [0,180,0]])
        
        for posa in hole_positions:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "n"
            p3["shape"] = "oobb_screw_countersunk"
            p3["pos"] = posa[0]
            p3["rot"] = posa[1]
            p3["depth"] = thickness
            p3["radius_name"] = "m3"
            p3["nut"] = True
            p3["overhang"] = True
            #p3["sandwich"] = True
            #p3["m"] = "#"   
            #p3["comment"]  = "bearing_plate_connecting_screw_center"
            oobb_base.append_full(thing, **p3)
    elif ((bearing == "6704" or bearing == "6705") and shaft == "coupler_flanged"):
        #coupler_flanged
        shift = 5.657
        hole_positions = []
        z_shift = thickness/2
        hole_positions.append([shift, shift, z_shift])
        hole_positions.append([-shift, -shift, z_shift])
        hole_positions.append([shift, -shift, z_shift])
        hole_positions.append([-shift, shift, z_shift])
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = "oobb_screw_countersunk"
        p3["pos"] = hole_positions
        p3["rot"] = [0,0,0]
        p3["depth"] = thickness + 10
        p3["radius_name"] = "m3"
        p3["nut"] = True
        p3["overhang"] = True        
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)
        
    
    if ( bearing == "6704" or bearing == "6705") and shaft == "m6":
        hole_positions = []
        # 90 degrees
        #hole_positions.append([[0, joint_dis/2, pos[2]+z], [0,0,0]])
        #hole_positions.append([[0, -joint_dis/2, pos[2]+z-thickness], [0,180,0]])
        # 45 degrees
        offset = 5.303
        hole_positions.append([[offset, offset, pos[2]+z], [0,0,0]])
        hole_positions.append([[-offset, -offset, pos[2]+z-thickness], [0,180,0]])
        
        for posa in hole_positions:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "n"
            p3["shape"] = "oobb_screw_countersunk"
            p3["pos"] = posa[0]
            p3["rot"] = posa[1]
            p3["depth"] = thickness
            p3["radius_name"] = "m3"
            p3["nut"] = True
            p3["overhang"] = True
            #p3["sandwich"] = True
            #p3["m"] = "#"   
            #p3["comment"]  = "bearing_plate_connecting_screw_center"
            oobb_base.append_full(thing, **p3)
    return return_value

def get_bearing_plate_connecting_screw_perimeter(thing, **kwargs):
    return_value = []
    screws = []
    # default sets
    thickness = kwargs.get("thickness", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    bearing = kwargs.get("bearing", "6704")
    extra = kwargs.get("extra", "")

    z = thickness/2
    hole_positions = []
    
    if bearing == "606":
        joint_dis = 15*2        
        hole_positions.append([[joint_dis/2, joint_dis/4, z], [0,0,360/12]])
        hole_positions.append([[-joint_dis/2, -joint_dis/4, z], [0,0,360/12]])
        hole_positions.append([[joint_dis/4, -joint_dis/2, z-thickness], [0,180,0]])
        hole_positions.append([[-joint_dis/4, joint_dis/2, z-thickness], [0,180,0]])
    if bearing == "6704":         
        joint_dis = 18*2        
        hole_positions.append([[joint_dis/2, 0, z], [0,180,360/12]])
        hole_positions.append([[-joint_dis/2, 0, z], [0,180,360/12]])
        hole_positions.append([[0, joint_dis/2, z-thickness], [0,0,0]])
        hole_positions.append([[0, -joint_dis/2, z-thickness], [0,0,0]])
    if bearing == "6705": 
        joint_dis_y = 18*2
        joint_dis_x = 16
        hole_positions.append([[joint_dis_x/2, -joint_dis_y/2, z], [0,0,0]])
        hole_positions.append([[-joint_dis_x/2, joint_dis_y/2, z], [0,0,0]])
        hole_positions.append([[-joint_dis_x/2, -joint_dis_y/2, z-thickness], [0,180,0]])
        hole_positions.append([[joint_dis_x/2, joint_dis_y/2, z-thickness], [0,180,0]])
    if bearing == "6810":
        joint_dis_y = 60
        joint_dis_x = 60
        joint_shift = 7.5
        hole_positions.append([[joint_dis_x/2, -joint_dis_y/2 + joint_shift, z], [0,0,0]])
        hole_positions.append([[-joint_dis_x/2, joint_dis_y/2 - joint_shift, z], [0,0,0]])
        if extra == "three_quarter": # all screws on direction
            hole_positions.append([[-joint_dis_x/2 + joint_shift, -joint_dis_y/2, z], [0,0,0]])
            hole_positions.append([[joint_dis_x/2 - joint_shift, joint_dis_y/2, z], [0,0,0]])
        else:
            hole_positions.append([[-joint_dis_x/2 + joint_shift, -joint_dis_y/2, z-thickness], [0,180,0]])
            hole_positions.append([[joint_dis_x/2 - joint_shift, joint_dis_y/2, z-thickness], [0,180,0]])


    for posa in hole_positions:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = "oobb_screw_countersunk"
        pos1 = copy.deepcopy(pos)
        pos1[0] += posa[0][0]
        pos1[1] += posa[0][1]
        pos1[2] += posa[0][2]
        p3["pos"] = pos1
        p3["rot"] = posa[1]
        p3["depth"] = thickness
        p3["radius_name"] = "m3"
        p3["nut"] = True
        p3["overhang"] = True
        #p3["sandwich"] = True
        #p3["m"] = "#"            
        oobb_base.append_full(thing, **p3)

    return return_value

def get_bearing_plate_hole_center(thing, **kwargs):    
    return_value = []
    # default sets
    shaft = kwargs.get("shaft", "m6")
    extra = kwargs.get("extra", "")
    thickness = kwargs.get("thickness", 3)

    bearing = kwargs.get("bearing", "6704")
        
    bearing_id = oobb_base.gv(f'bearing_{bearing}_id',"true")
    ## the holes in the middle
    if bearing == "6705" or bearing == "6704":  
        #m3 holes and nuts     
        p3 = copy.deepcopy(kwargs)
        posss = []
        poss = []
        poss.append([7.5, 0, 0])
        poss.append([-7.5,0, 0])
        posss.append(poss)
        poss = []
        poss.append([0, 7.5, 0])
        poss.append([0,-7.5, 0])
        posss.append(poss)
        rot = [0,0,360/12]
        for poss in posss:
            p3["type"] = "n"
            shap = "oobb_hole"
            if bearing == "6705":
                shap = ["oobb_hole", "oobb_nut"]
                #p3["overhang"] = True
                p3["zz"] = "middle"
                p3["rot"] = rot
                rot = [0,0,0]
            if shaft == "motor_servo_standard_01" or shaft == "motor_tt_01":
                #move to bottom
                for pos in poss:
                    pos[2] = -thickness/2
                    p3["zz"] = "bottom"                
                    p3["hole"] = True
                    if bearing == "6705":
                        #p3["depth"] = 4
                        pos[2] = 0
                        p3["zz"] = "middle"
                        pass
                    if bearing == "6704": ##clearance for pocket nut on 6705 bearing
                        shap = ["oobb_hole", "oobb_threaded_insert"]                    
                        for pos in poss:
                            pos[2] = thickness/2
            p3["shape"] = shap
            p3["pos"] = poss
            p3["radius_name"] = "m3"
            p3["hole"] = True
            #p3["m"] = "#"
            
            p3.pop("extra", "")
            oobb_base.append_full(thing, **p3)
    if bearing == "6810":
        p3 = copy.deepcopy(kwargs)
        p3.pop("extra", "")
        p3["type"] = "n"
        p3["shape"] = "oobb_holes"
        p3["hole"]  = "all"
        p3["circle"] = True
        p3["diameter"] = 5
        p3["diameter_clearance"] = 10
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)
        
        p3 = copy.deepcopy(kwargs)
        p3.pop("extra", "")
        p3["type"] = "n"
        p3["shape"] = "oobe_holes"
        p3["hole"]  = "all"
        p3["circle"] = True
        p3["diameter"] = 9
        p3["diameter_clearance"] = 11
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)
        
        


    return return_value


def get_bearing_plate_hole_perimeter(thing, **kwargs):    
    extra = kwargs.get("extra", "")
    if extra == "shifted":
        return get_bearing_plate_hole_perimeter_shifted(thing, **kwargs)
    else:
        return get_bearing_plate_hole_perimeter_base(thing, **kwargs)

def get_bearing_plate_hole_perimeter_base(thing, **kwargs):    
    return_value = []
    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    shaft = kwargs.get("shaft", "m6")
    extra = kwargs.get("extra", "")

    bearing = kwargs.get("bearing", "6704")
        
    radius_name = "m6"
    
    holes = "perimeter_miss_middle"
    
    # add the corner holes for a 6810 bearing
    if bearing == "6810":
        holes = ["top", "bottom"] # add the side holes for non square 6810 holders
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_holes"
        p3["width"] = 5
        p3["height"] = 5
        p3["holes"] = "corners"
        p3["radius_name"] = radius_name
        oobb_base.append_full(thing, **p3)
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_holes"
        p3["width"] = 5
        p3["height"] = 5
        p3["holes"] = "single"
        p3["loc"] = [[1, 1.5],[1.5,5],[4.5,1],[5,4.5]]
        #p3["m"] = "#"
        p3["radius_name"] = "m3"
        oobb_base.append_full(thing, **p3)
    elif bearing == "606":  
        oobb_holes = []      
        oobe_holes = []
        middle_width = (width + 1) / 2
        middle_height = (height + 1) / 2
        for h in range(1,height+1):            
            for w in range(1,width+1):                
                distance_from_middle_width = abs(w - middle_width)
                distance_from_middle_height = abs(h - middle_height)
                distance_threshold = 0.5
                if distance_from_middle_width > distance_threshold or distance_from_middle_height > distance_threshold:
                    oobb_holes.append([w, h])
                ww = w + 0.5
                hh = h
                distance_from_middle_width = abs(ww - middle_width)
                distance_from_middle_height = abs(hh - middle_height)
                distance_threshold = 0.5
                if distance_from_middle_width > distance_threshold or distance_from_middle_height > distance_threshold:
                    if w < width:
                        oobe_holes.append([ww, hh])
                ww = w
                hh = h + 0.5
                distance_from_middle_width = abs(ww - middle_width)
                distance_from_middle_height = abs(hh - middle_height)
                distance_threshold = 0.5
                if distance_from_middle_width > distance_threshold or distance_from_middle_height > distance_threshold:
                    if h < height:
                        oobe_holes.append([ww, hh])



                
                
                
                
                    
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_holes"
        p3["pos"] = pos
        p3["width"] = width
        p3["height"] = height
        p3["holes"] = "single"
        p3["loc"] = oobb_holes
        p3["radius_name"] = "m6"
        oobb_base.append_full(thing, **p3)

        p4 = copy.deepcopy(p3)
        p4["radius_name"] = "m3"
        p4["loc"] = oobe_holes
        oobb_base.append_full(thing, **p4)
    
    else:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_holes"
        p3["pos"] = pos
        p3["width"] = width
        p3["height"] = height
        p3["holes"] = holes
        p3["radius_name"] = radius_name
        oobb_base.append_full(thing, **p3)

    return return_value

def get_bearing_plate_hole_perimeter_shifted(thing, **kwargs):    
    return_value = []
    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos_plate = kwargs.get("pos_plate", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    shaft = kwargs.get("shaft", "m6")
    extra = kwargs.get("extra", "")

    bearing = kwargs.get("bearing", "6704")
        
    radius_name = "m6"
    
    holes = "perimeter_miss_middle"
    
    # add the corner holes for a 6810 bearing
    if bearing == "6810":
        holes = ["top", "bottom"] # add the side holes for non square 6810 holders
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_holes"
        p3["width"] = 5
        p3["height"] = 5
        p3["holes"] = "corners"
        p3["radius_name"] = radius_name
        oobb_base.append_full(thing, **p3)
    elif bearing == "606":  
        oobb_holes = []      
        oobe_holes = []
        oobb_holes.append([1, 1])
        oobb_holes.append([2, 1])        
        oobb_holes.append([3, 1])        
        oobb_holes.append([1, 2])
        oobb_holes.append([3, 2])
        oobb_holes.append([1, 3])
        oobb_holes.append([2, 3])
        oobb_holes.append([3, 3])
        oobb_holes.append([1, 4])
        oobb_holes.append([2, 4])
        oobb_holes.append([3, 4])



        oobe_holes.append([1.5, 1])
        
        oobe_holes.append([3, 1.5])
        oobe_holes.append([2.5, 3])

        oobe_holes.append([1, 2.5])


        oobe_holes.append([1, 3.5])
        oobe_holes.append([2, 3.5])
        oobe_holes.append([3, 3.5])
        oobe_holes.append([1.5, 4])
        oobe_holes.append([2.5, 4])




                
                
                
                
                    
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_holes"
        p3["pos"] = pos_plate
        p3["width"] = width
        p3["height"] = height
        p3["holes"] = "single"
        p3["loc"] = oobb_holes
        p3["radius_name"] = "m6"
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)

        p4 = copy.deepcopy(p3)
        p4["radius_name"] = "m3"
        p4["loc"] = oobe_holes
        p3["m"] = "#"
        oobb_base.append_full(thing, **p4)
    
    else:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_holes"
        p3["pos"] = pos
        p3["width"] = width
        p3["height"] = height
        p3["holes"] = holes
        p3["radius_name"] = radius_name
        oobb_base.append_full(thing, **p3)

    return return_value

def get_bearing_plate_hole_shaft(thing, **kwargs):
    return_value = []
    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    shaft = kwargs.get("shaft", "m6")
    extra = kwargs.get("extra", "")
    bearing = kwargs.get("bearing", "608")

    radius_name = "m6"

    # middle hole type
    if shaft == "m6":        
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_holes"
        p3["pos"] = pos
        p3["width"] = width
        p3["height"] = height
        p3["holes"] = "just_middle"
        p3["radius_name"] = radius_name
        oobb_base.append_full(thing, **p3)
    elif shaft == "coupler_flanged": 
        p3 = copy.deepcopy(kwargs)       
        p3["type"] = "n"
        p3["shape"] = f"oobb_hole"
        p3["pos"] = pos
        p3["radius"] = 10.5/2
        oobb_base.append_full(thing, **p3)
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_hole"
        p3["pos"] = pos
        p3["radius_name"] = "m3"
        p3["depth"] = 25
        p3["rot"] = [0,90,90]
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)

        


    elif shaft == "motor_building_block_large_01":
        posa = copy.deepcopy(pos)
        posa[2] = posa[2] - thickness/2
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_motor_building_block_large_01"
        p3["pos"] = posa

        oobb_base.append_full(thing, **p3)
    elif shaft == "motor_gearmotor_01" or shaft == "motor_tt_01":
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_motor_tt_01"
        poss = []
        pos1 = copy.deepcopy(pos)
        lift = 3
        pos1[2] = pos1[2] - thickness/2 + 6 + lift
        pos2 = copy.deepcopy(pos)
        p3["pos"] = pos1
        p3["clearance"] = "bottom"
        p3["part"] = "shaft"
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)
        #add an extra bearing clearance below
        # bearing
        poss = []
        if "removable" in extra:
            pos1 = copy.deepcopy(pos)
            pos1[2] = pos1[2] - 3
            pos2 = copy.deepcopy(pos)
            pos2[2] = pos2[2] - 6
            poss = [pos1, pos2]
        elif "sandwich" in extra:
            pos1 = copy.deepcopy(pos)
            pos1[2] = pos1[2] - 6
            poss = [pos1]
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n" 
        p3["shape"] = f"{size}_bearing"
        p3["bearing"] = bearing
        p3["width"] = width             
        p3["height"] = height  
        p3["depth"] = thickness
        p3["pos"] = poss
        #p3["m"] =   "#"
        
        oobb_base.append_full(thing, **p3)
    elif shaft == "motor_n20":
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_motor_n20"
        p3["pos"] = pos
        p3["part"] = "shaft"
        oobb_base.append_full(thing, **p3)
    elif shaft == "motor_servo_micro_01":
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_motor_servo_micro_01"
        p3["pos"] = pos
        p3["part"] = "shaft"
        oobb_base.append_full(thing, **p3)
    elif shaft == "motor_servo_standard_01" and extra == "horn_adapter_printed":
        posa = copy.deepcopy(pos)
        posa[2] = posa[2] - thickness/2
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_motor_servo_standard_01"
        p3["pos"] = posa
        p3["part"] = "shaft"
        p3["rot"] = [0, 0, 45]
        oobb_base.append_full(thing, **p3)
    elif shaft == "motor_servo_standard_01" and extra == "horn_adapter_screws":        
        posa = copy.deepcopy(pos)
        posa[2] = posa[2]
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_motor_servo_standard_01"
        p3["pos"] = posa
        p3["part"] = "shaft"        
        p3["rot"] = [0, 0, 45]
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)
        #add an extra bearing clearance below
        # bearing
        pos1 = copy.deepcopy(pos)
        pos1[2] = pos1[2] - 3
        pos2 = copy.deepcopy(pos)
        pos2[2] = pos2[2] - 6
        poss = [pos1, pos2]
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n" 
        p3["shape"] = f"{size}_bearing"
        p3["bearing"] = bearing
        p3["width"] = width             
        p3["height"] = height  
        p3["depth"] = thickness
        p3["pos"] = poss
        oobb_base.append_full(thing, **p3)



def get_bearing_plate_plate(thing, **kwargs):

    return_value = []
    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    pos_plate = kwargs.get("pos_plate", [0, 0, 0])
    shaft = kwargs.get("shaft", "m6")
    bearing = kwargs.get("bearing", "608")
    bearing_od = ob.gv(f"bearing_{bearing}_od", "3dpr") - 2
    extra = kwargs.get("extra", "")

    if "minimal" not in extra:
        if shaft == "m6":        
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "p";           
            p3["shape"] = f"{size}_plate";    
            p3["width"] = width;   
            p3["height"] = height;   
            p3["extra_mm"] = True
            p3["depth"] = thickness;  
            pos1 = copy.deepcopy(pos_plate)
            pos1[2] = pos1[2] - thickness/2 
            p3["pos"] = pos1
            #holes is false
            p3["holes"] = False
            #p3["m"] = "#" 
            p3["comment"] = "bearing_plate_plate"
            oobb_base.append_full(thing, **p3)
        
        if shaft != "m6" or extra == "no_center": 
            #add a 24mm cylinder thickness thick
            p3 = copy.deepcopy(kwargs)
            p3.pop("size","")
            p3["type"] = "positive";           
            if extra == "no_center":
                p3["type"] = "negative";                   
            p3["shape"] = "oobb_cylinder"
            p3["depth"] = thickness
            p3["radius"] = bearing_od
            p3["height"] = thickness
            p3["pos"] = pos_plate
            p3["mode"] = "all"
            p3["comment"] = "bearing_plate_plate"
            thing = oobb_base.append_full(thing, **p3)

    else: ### minimal plate
        #just 7605 at the moment
        pass
        radius_bearing = 32/2
        radius_exrta = 3/2
        p3 = copy.deepcopy(kwargs)
        p3.pop("size","")
        p3["type"] = "positive"
        p3["shape"] = "oobb_cylinder"
        p3["depth"] = thickness
        p3["radius"] = radius_bearing + radius_exrta
        p3["height"] = thickness
        p3["zz"] = "middle"
        oobb_base.append_full(thing, **p3)
        #add plate for connecting botlts
        p3 = copy.deepcopy(kwargs)
        p3.pop("size","")
        p3["type"] = "positive"
        p3["shape"] = "rounded_rectangle"
        size = [26,44,thickness]
        p3["size"] = size
        pos1 = copy.deepcopy(pos_plate)
        pos1[2] = pos1[2] - thickness/2
        p3["pos"] = pos1
        oobb_base.append_full(thing, **p3)
    

    if thing == "":
        return return_value
    else:
        return thing
    