from oobb_get_items_base import *
from oobb_get_item_common import *
import oobb_base as ob
from oobb_get_items_oobb import *
from oobb_get_items_oobb_old import *

import copy

def get_bearing_circle(**kwargs):
    thing = ob.get_default_thing(**kwargs)

    diameter = kwargs.get("diameter", "")
    thickness = kwargs.get("thickness", "")
    bearing_type = kwargs.get("bearing_type", "606")
    
    
    pos = kwargs.get("pos", [0, 0, 0])

    # solid piece
    th = thing["components"]
    kwargs.update({"exclude_d3_holes": True})
    kwargs.update({"exclude_center_holes": True})
    
    #th.extend(get_circle(**kwargs)["components"])
    # adding connecting screws
    connecting_screws = []
    a = 10.607
    # hole_positions = [1-adj,mid_h],[mid_w,height+adj],[mid_w,1-adj],[width+adj,mid_h]
    #outer connecting screws
    hole_positions = [[a,a],[a,-a],[-a,-a],[-a,a]]
    rot_current = 0
    rotz_current = 360/12
    times_through = 0
    for posa in hole_positions:
        x, y = pos[0]+posa[0], pos[1]+posa[1]
        z = pos[2]+thickness/2
        connecting_screws.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", sandwich=True, radius_name="m3", depth=thickness, pos=[x, y, z], m="", rotY=rot_current, rotZ=rotz_current))
        if rot_current == 0:
            rot_current = 180
        else:
            rot_current = 0
        times_through += 1
    th.extend(connecting_screws)

    # add bearing cutout
    th.extend(ob.oobb_easy(t="n", s="oobb_bearing", bearing_type=bearing_type, pos=pos, mode="all", m=""))

    # halfing it if 3dpr
    inclusion = "3dpr"
    th.append(ob.oobb_easy(t="n", s="cube", size=[500, 500, 500], pos=[pos[0]-500/2, pos[1]-500/2, pos[2]+0], inclusion=inclusion, m=""))
    
    return thing

def get_bearing_wheel(**kwargs):
    oring_type = kwargs.get("oring_type", "327")
    #figuring out radius
    thickness = kwargs.get("thickness", 9)
    od = ob.gv(f"oring_{oring_type}_od", "true")
    id = ob.gv(f"oring_{oring_type}_id", "true")
    pos = kwargs.get("pos", [0, 0, 0])
    idt = ob.gv(f"oring_{oring_type}_id_tight", "true")
    minus_bit = 1.5
    radius = idt + (od-id)/2 + 0.5 - minus_bit #(to account for the minusing) 
    diameter_big = radius*2/ob.gv("osp")
    diameter = int(round(diameter_big, 0))
    bearing_type = kwargs.get("bearing_type", "606")
    kwargs.update({"bearing_type": bearing_type})
    #if diameter is even take one off to make it odd
    if diameter % 2 == 0:
        diameter -= 1

    kwargs.update({"diameter": diameter})
    thing = ob.get_default_thing(**kwargs)
    
    # solid piece
    th = thing["components"]
    #kwargs.update({"exclude_d3_holes": True})
    #kwargs.update({"exclude_center_holes": True})
    
    kwargs.update({"diameter": diameter_big})
    kwargs.update({"exclude_center_holes": True})
    kwargs.update({"exclude_d3_holes": True})
    th.extend(get_circle(**kwargs)["components"])

    

    # adding connecting screws
    connecting_screws = []
    if diameter > 2:
        a = 10.607
    else:
        a = 8.5
    # hole_positions = [1-adj,mid_h],[mid_w,height+adj],[mid_w,1-adj],[width+adj,mid_h]
    #outer connecting screws
    hole_positions = [[a,a],[a,-a],[-a,-a],[-a,a]]
    rot_current = 0
    rotz_current = 360/12
    times_through = 0
    for posa in hole_positions:
        x, y = pos[0]+posa[0], pos[1]+posa[1]
        z = pos[2]+thickness/2
        connecting_screws.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", sandwich=True, radius_name="m3", depth=thickness, pos=[x, y, z], m="", rotY=rot_current, rotZ=rotz_current))
        if rot_current == 0:
            rot_current = 180
        else:
            rot_current = 0
        times_through += 1
    th.extend(connecting_screws)

    # add bearing cutout and o rings
    if thickness == 9: # in middle
        th.extend(ob.oobb_easy(t="n", s="oobb_bearing", bearing_type=bearing_type, pos=pos, mode="all", m=""))
        th.extend(ob.oe(t="n", s="oobb_oring", oring_type=oring_type, m="#"))
    elif thickness == 15:
        poss = []
        hei = thickness / 2 - 3
        poss.append([pos[0], pos[1], pos[2]-hei])
        poss.append([pos[0], pos[1], pos[2]+hei])
        for p in poss:
            th.extend(ob.oobb_easy(t="n", s="oobb_bearing", bearing_type=bearing_type, pos=p, mode="all", m=""))
            th.extend(ob.oe(t="n", s="oobb_oring", oring_type=oring_type, pos=p, m="#"))

    # halfing it if 3dpr
    inclusion = "3dpr"
    th.append(ob.oobb_easy(t="n", s="cube", size=[500, 500, 500], pos=[pos[0]-500/2, pos[1]-500/2, pos[2]+0], inclusion=inclusion, m=""))

    return thing

def get_bearing_plate_old(**kwargs):
    thing = ob.get_default_thing(**kwargs)

    shaft = kwargs.get("shaft", "m6")
    radius_name = kwargs.get("radius_name", "m6")
    width = kwargs.get("width", "")
    height = kwargs.get("height", "")
    thickness = kwargs.get("thickness", "")
    bearing_type = kwargs.get("bearing_type", "608")
    overwrite = kwargs.get("overwrite", False)
    micro_servo = kwargs.get("micro_servo", False)
    only_screws = kwargs.get("only_screws", False)
    no_screws = kwargs.get("no_screws", False)
    exclude_clearance = kwargs.get("exclude_clearance", False)
    extra2 = kwargs.get("extra", "")
    

    pos = kwargs.get("pos", [0, 0, 0])

    extra_mm = 1 / ob.gv("osp")

    # solid piece
    # don't print for shaft ones
    th = thing["components"]
    if shaft == "":        
        th.append(ob.oe(t="p", s="oobb_plate", width=width + extra_mm, height=height + extra_mm, depth=thickness, pos=[pos[0],pos[1],pos[2]-thickness/2], holes=False, mode="all"))
    else: 
        #add a 24mm cylinder thickness thick
        p1 = copy.deepcopy(kwargs)
        p1.pop("size","")
        p1["t"] = "p"
        p1["s"] = "oobb_cylinder"
        p1["depth"] = thickness
        p1["radius"] = 24/2
        p1["height"] = thickness
        p1["pos"] = [pos[0],pos[1],pos[2]]
        p1["mode"] = "all"
        th.extend(ob.oe(**p1))
        
    
    # for 6804 laser make plate bigger
    if bearing_type == "6804":
        pass
        th.append(ob.oe(t="p", s="oobb_plate", width=width+0.25, height=height+0.25,
                  depth=thickness, pos=[pos[0],pos[1],pos[2]-thickness/2], holes=False, mode="laser", inclusion="laser"))

    # bearing
    th.extend(ob.oobb_easy(t="n", s="oobb_bearing", bearing_type=bearing_type, pos=pos, mode="all", exclude_clearance=exclude_clearance, overwrite=overwrite, m=""))

    # adding corner holes
    # hole_positions = [1,1],[1,height],[width,1],[width,height]
    # for pos in hole_positions:
    #    x,y = ob.get_hole_pos(pos[0],pos[1],width,height)
    #    th.extend(ob.oobb_easy(t="n",s="oobb_hole", pos=[x,y,0], radius_name="m6", overwrite=overwrite, m=""))
    # adding perimieter miss middle holes
    
    holes = "perimeter_miss_middle"
    if bearing_type == "6810":
        holes = ["top", "bottom"]
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", pos=pos, width=5, height=5, holes="corners", m="", radius_name=radius_name))

    th.extend(ob.oobb_easy(t="n", s="oobb_holes", pos=pos, width=width, height=height, holes=holes, m="", radius_name=radius_name))

    # adding middle holes
    wid = ob.gv(f'bearing_{bearing_type}_inner_holes_true')
    th.extend(ob.oobb_easy(t="n", s="oobb_holes", pos=pos, width=wid, height=wid, holes="circle", middle=False, circle_dif=5, m="", radius_name=radius_name))

    # middle hole type
    if shaft == "m6":
        posa = copy.deepcopy(pos)
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", pos=pos, radius_name=radius_name, width=width, height=height, m="", holes="just_middle"))
    elif shaft == "motor_building_block_large_01":
        posa = copy.deepcopy(pos)
        posa[2] = posa[2] - thickness/2
        th.extend(ob.oobb_easy(t="n", s="oobb_motor_building_block_large_01",
                  part="shaft", pos=posa, m=""))        
    elif shaft == "motor_gearmotor_01":
        th.extend(ob.oobb_easy(t="n", s="oobb_motor_gearmotor_01",
                  part="shaft", pos=pos, m=""))
        joint_dis = 15
    elif shaft == "motor_n20":
        th.extend(ob.oobb_easy(t="n", s="oobb_motor_n20",
                  part="shaft", pos=pos, m=""))
        joint_dis = 15        
    elif shaft == "motor_servo_micro_01":
        th.extend(ob.oobb_easy(t="n", s="oobb_motor_servo_micro_01",
                  part="shaft", pos=pos, m=""))
        joint_dis = 15
    elif shaft == "motor_servo_standard_01" and extra2 == "horn_adapter_printed":
        posa = copy.deepcopy(pos)
        posa[2] = posa[2] - thickness/2
        th.extend(ob.oobb_easy(t="n", s="oobb_motor_servo_standard_01",
                  part="shaft", pos=posa, m=""))
        joint_dis = 15
    elif shaft == "motor_servo_standard_01" and extra2 == "horn_adapter_screws":
        posa = copy.deepcopy(pos)
        posa[2] = posa[2] - thickness/2
        th.extend(ob.oobb_easy(t="n", s="oobb_motor_servo_standard_01",
                  part="shaft", pos=posa, m=""))
        joint_dis = 15
    
        
        

    if extra2 != "horn_adapter_screws" and shaft != "motor_building_block_large_01": ## don't add connecting screws for screw servo horn
    # adding connecting screws
        connecting_screws = []
        micro_servo_screws = []
        mid_w = (width - 1) / 2 + 1
        mid_h = (height - 1) / 2 + 1
        adja = 0 / ob.gv("osp")
        adjb = 0
        adjc = 0
        if bearing_type == "6803":
            adja = 2 / ob.gv("osp")
        elif bearing_type == "6804" or bearing_type == "6704":
            #spacing is 18
            adja = 3 / ob.gv("osp")
        elif bearing_type == "6810":
            adjb = 22 / ob.gv("osp")
            adjc = 1
        # hole_positions = [1-adj,mid_h],[mid_w,height+adj],[mid_w,1-adj],[width+adj,mid_h]
        #outer connecting screws
        r = 360/24
        hole_positions = [width+adja-adjc, mid_h-adjb, r], [mid_w-adjb, 1-adja, 0],  [1-adja+adjc, mid_h+adjb, r], [mid_w+adjb, height+adja,0]
        rot_current = 0
        
        
        times_through = 0
        #added to allow gearmotor retaininer to have 3 nuts on top
        gearmotor_screw_twist = True
        for posa in hole_positions:
            x, y = ob.get_hole_pos(pos[0]+posa[0], pos[1]+posa[1], width, height)
            z = pos[2]+thickness/2
            type = "oobb_screw_countersunk"
            if no_screws:
                type = "oobb_hole"
            connecting_screws.extend(ob.oobb_easy(t="n", s=type, sandwich=True, radius_name="m3", depth=thickness, pos=[x, y, z], m="", rotY=rot_current, rotZ=posa[2]))
            micro_servo_screws.extend(ob.oobb_easy(t="n", s="oobb_hole", sandwich=True, radius_name="m3",depth=thickness, pos=[x, y, z], m="", rotY=rot_current, rotZ=posa[2]))
            if rot_current == 0:
                #added to allow gearmotor retaininer to have 3 nuts on top
                if shaft == "motor_gearmotor_01" and gearmotor_screw_twist:
                    rot_current = 0
                    gearmotor_screw_twist = False
                else:
                    rot_current = 180
            else:
                rot_current = 0
            # doing nut twist on the outside ones
            if times_through == 1 or times_through == 2:
                rotz_current = 0
            else:
                rotz_current = 360/24
            times_through += 1
        th.extend(connecting_screws)

        
        # middle holes
        
        hole_positions_mm = []
        
        joint_dis = 15
        joint_dis_laser = 13

        # add the inset connecting standoffs needed for 6704 and 6804 20mm id to laser only
        if not no_screws:
            if bearing_type == "6704" or bearing_type == "6804":
                if shaft == "motor_gearmotor_01" or shaft == "motor_servo_micro_01":
                    hole_positions_mm = [
                    [pos[0]+0, pos[1]+joint_dis/2, pos[2]+z, ["true", "3dpr"], "oobb_screw_countersunk", 0], 
                    [pos[0]+0, pos[1]-joint_dis/2, pos[2]+z, ["true", "3dpr"], "oobb_screw_countersunk", 180], 
                    [pos[0]+0, pos[1]+joint_dis_laser/2, pos[2]+z, ["laser"], "oobb_screw_countersunk", 0], 
                    [pos[0]+0, pos[1]-joint_dis_laser/2, pos[2]+z, ["laser"], "oobb_screw_countersunk", 180],
                    ### bottom nuts intead of threaded inserts
                    [pos[0]+joint_dis/2, 0, pos[2]+z, ["3dpr"], "oobb_screw_countersunk", "tight"], 
                    [pos[0]-joint_dis/2, 0, pos[2]+z, ["3dpr"], "oobb_screw_countersunk", "tight"], 
                    ]
                else:
                    hole_positions_mm = [[pos[0]+0, pos[1]+joint_dis/2, pos[2]+z, ["true", "3dpr"], "oobb_screw_countersunk", 0], [pos[0]+0, pos[1]-joint_dis/2, pos[2]+z, ["true", "3dpr"], "oobb_screw_countersunk", 180], [pos[0]+0, pos[1]+joint_dis_laser/2, pos[2]+z, ["laser"], "oobb_screw_countersunk", 0], [pos[0]+0, pos[1]-joint_dis_laser/2, pos[2]+z, ["laser"], "oobb_screw_countersunk", 0]]
        
        # add head insets 180 to keep them out of the 3dpr one currently and 0 for laser one so both are in the bottom, need to double slice 3dpr one to get it working properly in the middle
        #z = 3 #put threaded insert in the middle onl;y really works if insert is 6mm deep
        #hole_positions_mm.append(
        #    [joint_dis/2, 0, z, ["all"], "oobb_threaded_insert", 0])
        #hole_positions_mm.append(
        #    [-joint_dis/2, 0, z, ["all"], "oobb_threaded_insert", 0])
        for posa in hole_positions_mm:
            x, y, z, mode, type, rotY = posa
            extra=""
            if rotY == "tight":
                rotY = 0
                extra = "tight"
            # z = thickness/2
            th.extend(ob.oobb_easy(t="n", s=type, sandwich=True, radius_name="m3",
                    hole=True, depth=thickness, pos=[x, y, z], m="", rotY=rotY, mode=mode,extra=extra))
    
    bearing_id = ob.gv(f'bearing_{bearing_type}_id',"true")
    ## the holes in the middle
    if bearing_id * 2 > 15 and not no_screws:
        p2 = copy.deepcopy(kwargs)
        p2["holes"] = False
        if shaft == "m6":
            p2["slots"] = True
        else:
            p2["slots"] = False
            p2["inserts"] = True
        #p2["m"] = "#"
        th.extend(get_ci_holes_center(**p2))


    # halfing it if 3dpr
    inclusion = "3dpr"
    
    if extra2 == "horn_adapter_screws":   
        th.append(ob.oobb_easy(t="n", s="cube", size=[500, 500, 500], pos=[pos[0]-500/2, pos[1]-500/2, 0.5], inclusion=inclusion, m=""))
        
    elif shaft == "motor_building_block_large_01":
        #th.append(ob.oobb_easy(t="n", s="cube", size=[500, 500, 500], pos=[pos[0]-500/2, pos[1]-500/2, 4], inclusion=inclusion, m=""))
        # add extra bearing clearance so it can slide in from the top
        # bearing
        pos = [0,0,-3]
        th.extend(ob.oobb_easy(t="n", s="oobb_bearing", bearing_type=bearing_type, pos=pos, mode="all", exclude_clearance=exclude_clearance, overwrite=overwrite, m=""))
        pos = [0,0,-6]
        th.extend(ob.oobb_easy(t="n", s="oobb_bearing", bearing_type=bearing_type, pos=pos, mode="all", exclude_clearance=exclude_clearance, overwrite=overwrite, m=""))
        
    else: # add an extra 1.5 mm
        th.append(ob.oobb_easy(t="n", s="cube", size=[500, 500, 500], pos=[pos[0]-500/2, pos[1]-500/2, 0], inclusion=inclusion, m=""))
    #only include the screws if only_scres
    if only_screws:
        if not micro_servo:
            thing["components"] = connecting_screws
        else:
            thing["components"] = micro_servo_screws

    return thing

def get_bearing_plate_shim(**kwargs):
    # this is a shim for the bearing plate
    bearing_type = kwargs.get("bearing_type", "6803")
    thickness = kwargs.get("thickness", 3)

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    th.extend(ob.oobb_easy(t="p", s="oobb_cylinder",
              radius_name=f'bearing_{bearing_type}_od_catch', depth=thickness, pos=[0, 0, 0]))
    th.extend(ob.oobb_easy(t="n", s="oobb_cylinder",
              radius_name=f'bearing_{bearing_type}_id', depth=thickness, pos=[0, 0, 0]))

    return thing

def get_bearing_plate_jack(**kwargs):
    thing = ob.get_default_thing(**kwargs)

    osp = ob.gv("osp")
    pos = kwargs.get("pos", [0,0,0])

    # solid piece
    th = thing["components"]

    p2 = copy.deepcopy(kwargs)
    #bp = get_bearing_plate(**p2)["components"]
    bp = []
    th.extend(bp)
    p2 = copy.deepcopy(kwargs)
    p2["height"] = 1
    p2["holes"] = True
    ja = get_jack(**p2)["components"]
    shift = [0, -osp * 2+ 1.5, 0]
    #ja = oobb_base.highlight(ja)
    ja = oobb_base.shift(ja, shift)
    th.extend(ja)


    return thing

def get_bearing_plate_jack_basic(**kwargs):
    thing = ob.get_default_thing(**kwargs)

    osp = ob.gv("osp")
    pos = kwargs.get("pos", [0,0,0])

    # solid piece
    th = thing["components"]

    p2 = copy.deepcopy(kwargs)
    #bp = get_bearing_plate(**p2)["components"]
    bp = []
    th.extend(bp)
    p2 = copy.deepcopy(kwargs)
    p2["height"] = 1
    p2["holes"] = False
    ja = get_jack_basic(**p2)["components"]
    shift = [0, -osp * 2+ 1.5, 0]
    #ja = oobb_base.highlight(ja)
    ja = oobb_base.shift(ja, shift)
    th.extend(ja)

    #remove the standard bp slice
    th = oobb_base.remove_if(th, "size", [500,500,500])

    width = 3
    height_cube = 13.5
    thickness = 12
    mode = "all"
    rot_current = 0
    for x in range(0, width-1):
        x = (-width/2*ob.gv("osp")+ob.gv("osp"))+x*ob.gv("osp")
        y = -15
        z = thickness/2

        th.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", radius_name="m3", depth=thickness, pos=[x, y, z], mode=mode, sandwich=True, m="", rotY=rot_current, include_nut=True))
        rot_current = rot_current + 180

    top = copy.deepcopy(th)
    bottom = copy.deepcopy(th)
    bottom = oobb_base.shift(bottom, [50,0,-6])
    bottom = oobb_base.inclusion(bottom, "3dpr")

   

    th = bottom + top

    #3dpr silces
    th.extend(ob.oobb_easy(t="n", s="oobb_slice", pos=[0,0, 0], mode="3dpr", m="")) 
    th.extend(ob.oobb_easy(t="n", s="oobb_slice", pos=[0,0,-506], mode="3dpr", m="")) 

    thing["components"] = th    

    return thing

def get_bracket_2020_aluminium_extrusion(**kwargs):
    
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_pos = [0, 0, 0]

    #add m6 holes
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width,
              height=height, depth=thickness, pos=plate_pos, mode="all"))
    
    th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, holes="all", pos=plate_pos, m=""))
    th.extend(ob.oobb_easy(t="n", s=f"oobe_holes",  holes="all",  pos=plate_pos, width=(width*2)-1, height=(height*2)-1,m="#"))
   
    #add oobb_cube_center 25x40xthickness at 37.5 22.5 0
    

    return thing

def get_bunting_alphabet(**kwargs):
   
    thickness = kwargs.get("thickness", 3)
    width = kwargs.get("width", 7)
    thing = ob.get_default_thing(**kwargs)    
    th = thing["components"]
    extra = kwargs.get("extra", "")

    width_working = width - 2
    text_size = width_working * 95/5

    # plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = "oobb_plate"
    p3["depth"] = thickness
    oobb_base.append_full(thing, **p3)
    
    # holes
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = "oobb_holes"
    p3["height"] = 1
    p3["holes"] = ["all"]
    p3["both_holes"] = True
    p3["m"] = "#"
    oobb_base.append_full(thing, **p3)
    # find the start point needs to be half the width_mm plus half ob.gv("osp")
    


    shift_y = 0
    if width == 3:
        shift_y = -5
    if width == 5:
        shift_y = -5

    p2 = copy.deepcopy(kwargs)
    p2["type"] = "p"
    p2["shape"] = "text"
    p2["text"] = extra.upper()
    p2["size"] = text_size
    p2["pos"] = [0,shift_y,0]
    p2["height"] = thickness
    p2["valign"] = "top"
    p2["halign"] = "center"
    p2["font"] = "DejaVu Sans Mono:style=Bold"
    thinga = ob.oe(**p2)
    th.append(thinga)


    return thing 

def get_circle_old_1(**kwargs):

    diameter_big = kwargs.get("diameter", 1)
    
    #bring diameter down to round down for holes
    if diameter_big != 1.5:
        diameter = int(round(diameter_big, 0))
    else:
        diameter = diameter_big
    #if diameter is even take one off to make it odd
    if diameter % 2 == 0:
        diameter -= 1
    kwargs.update({"diameter": diameter})
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", False)
    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    th.extend(ob.oobb_easy(t="p", s="oobb_circle",
              diameter=diameter_big, depth=thickness, pos=[0, 0, 0]))
    # find the start point needs to be half the width_mm plus half ob.gv("osp")
    
   

    
    if holes:        
        if diameter == 3:
            # add 45 degree rotated ones but do the math
            a = 15
            positions = [[0, 0, 0], [0, a, 0], [0, -a, 0], [-a, 0, 0], [a, 0, 0]]
            exclude_d3_holes = kwargs.get("exclude_d3_holes", False)
            if not exclude_d3_holes:                
                a = 10.607
                positions.extend([[a, a, 0], [a, -a, 0], [-a, a, 0], [-a, -a, 0]])

            for pos in positions:
                th.extend(ob.oobb_easy(t="n", s="oobb_hole",                        radius_name="m6", pos=pos, m=""))
                
        else: ## add regular holes
            th.extend(ob.oobb_easy(t="n", s="oobb_holes", circle_dif=13,
                  width=diameter, height=diameter, holes=["circle","just_middle"], m=""))
        exclude_center_holes = kwargs.get("exclude_center_holes", False)
        if not exclude_center_holes:
            th.extend(get_ci_holes_center(**kwargs))

    if both_holes:
        width = diameter
        height = diameter
        #already added with hooles True
        #th.extend(ob.oobb_easy(t="n", s=f"oobb_holes", width=width, height=height, m="#"))
        th.extend(ob.oobb_easy(t="n", s=f"oobe_holes", holes="circle", extra="trim_down", circle_dif=13, width=(width*2)-1, height=(height*2)-1, m=""))

    extra = kwargs.get("extra", None)
    if extra is not None:
        if extra == "nut_m6":
            th.extend(ob.oobb_easy(t="n", s="oobb_nut", pos=[0, 0, -thickness/2], radius_name="m6", rotZ=360/24, m=""))

            #socket cap screw clearance
            if thickness == 12:
                dep = 3
                th.extend(ob.oobb_easy(t="n", s="oobb_screw_socket_cap", depth=thickness, pos=[15/2, 0, dep], radius_name="m3", include_nut=False, rotZ=360/24, m="#"))
                th.extend(ob.oobb_easy(t="n", s="oobb_screw_socket_cap", depth=thickness, pos=[-15/2, 0, dep], radius_name="m3", include_nut=False, rotZ=360/24, m="#"))
            



    return thing

def get_circle_captive(**kwargs):
    shaft = kwargs.get("shaft", "")
    width = kwargs.get("diameter", 3)
    height = kwargs.get("diameter", 3)
    diameter_big = kwargs.get("diameter", 1)
    
    #bring diameter down to round down for holes
    if diameter_big != 1.5:
        diameter = int(round(diameter_big, 0))
    else:
        diameter = diameter_big
    #if diameter is even take one off to make it odd
    if diameter % 2 == 0:
        diameter -= 1
    kwargs.update({"diameter": diameter})
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", True)

    thing = ob.get_default_thing(**kwargs)
    thing["components"] = get_circle(**kwargs)["components"]    
    th = thing["components"]   
    #remove center hole
    th = oobb_base.remove_if(th, "pos", [0,0,-125]) 

    #add shaft
    th.extend(ob.oobb_easy(t="n", s=f"oobb_{shaft}", width=width, height=height,clearance=True, pos=[0, 0, 0], part="shaft", m =""))

    #add m3 press nuts
    offset = 7.5
    nuts = []
    nuts.append([0,offset,"m3"])
    nuts.append([0,-offset,"m3"])
    nuts.append([-offset,0,"m3"])
    nuts.append([offset,0,"m3"])
    if diameter >= 3:
        offset = 10.607
        nuts.append([offset,offset,"m6"])
        nuts.append([offset,-offset,"m6"])
        nuts.append([-offset,offset,"m6"])
        nuts.append([-offset,-offset,"m6"])
    for nut in nuts:
        x,y,radius_name  = nut
        th.extend(ob.oobb_easy(t="n", s="oobb_nut", width=width, height=height, pos=[x,y,-thickness/2], extra="tight", holes="single", radius_name = radius_name, include_nut=False, depth=thickness, m=""))


    return thing

def get_ci_holes_center(thing, **kwargs):
    th = []
    pos = kwargs.get("pos", [0, 0, 0])
    slots = kwargs.get("slots", True)
    holes = kwargs.get("holes", True)
    inserts = kwargs.get("inserts", False)
    # add m3 holes
    if holes:    
        a = 7.5        
        positions = [0, a, 0], [0, -a, 0]
        for pos in positions:
            ob.append_full(thing, t="n", s="oobb_hole", radius_name="m3", pos=pos, m="")
    # add m3 slots
    if slots:        
        a = 7.75        
        positions = [a, 0, 0], [-a, 0, 0]
        for pos in positions:
            ob.append_full(thing, t="n", s="oobb_slot", radius_name="m3", pos=pos, m="",w=0.5,rotZ=0)
    if inserts:
        a = 7.5        
        positions = [a, 0, 0], [-a, 0, 0]
        for pos in positions:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "n"
            p3["shape"] = "oobb_threaded_insert"
            p3["pos"] = pos
            p3["radius_name"] = "m3"
            p3["insertion_cone"] = False
            ob.append_full(thing, **p3)
    return th

def get_holder_old(**kwargs):
    extra = kwargs.get("extra")
    kwargs.pop("extra")
    kwargs["type"] = f'holder_{extra}'
    if extra != "":
        # Get the module object for the current file
        current_module = __import__(__name__)
        function_name = "get_holder_" + extra
        # Call the function using the string variable
        function_to_call = getattr(current_module, function_name)
        return function_to_call(**kwargs)
    else:
        Exception("No extra")


def get_holder_fan_120_mm(**kwargs):

    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    #set pos
    kwargs["pos"] = pos

    th = thing["components"]

    plate_depth = -(thickness + 6)
    plate_pos = [0,0,0]

    #thin full plate
    pos = [plate_pos[0], plate_pos[1], plate_pos[2]]
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width, height=height, depth=thickness, pos=pos, mode="all"))

    th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height,  holes="perimeter", both_holes= True, pos=plate_pos,radius_name="m6", m=""))        
    th.extend(ob.oobb_easy(t="n", s="oobe_holes", width=(width*2)-1, height=(height*2)-1,  holes="perimeter", pos=plate_pos,radius_name="m3", m=""))  
    
    # fan
    p2 = copy.deepcopy(kwargs)    
    p2.pop("size")
    p2["type"] = "n"
    p2["shape"] = "oobb_fan_120_mm"
    x = 0
    y = 0
    z = 2
    pos = [p2["pos"][0] + x, p2["pos"][1] + y, p2["pos"][2] + z]
    p2["pos"] = pos
    rotZ = 0
    rotY = 0
    rotX = 0
    p2["rotZ"] = rotZ
    p2["rotY"] = rotY
    p2["rotX"] = rotX
    #p2["m"] = "#"
    th.extend(ob.oobb_easy(**p2))

    

    
    return thing

def get_holder_motor_building_block_large_01_bottom(**kwargs):
    kwargs["bottom"] = True
    return get_holder_motor_building_block_large_01(**kwargs)

def get_holder_motor_building_block_small_01_bottom(**kwargs):
    kwargs["bottom"] = True
    kwargs["small"] = True
    return get_holder_motor_building_block_large_01(**kwargs)

def get_holder_motor_building_block_large_01(**kwargs):

    #load in kwargs
    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    kwargs["pos"] = pos
    size = kwargs.get("size", "oobb")
    extra = kwargs.get("extra", "")    
    bottom = kwargs.get("bottom", False)
    small = kwargs.get("small", False)

    # get the default thing
    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size", "") #remove oobb as size to stop error later on with kwargs
    kwargs.pop("type", "") #remove the id as type to avoiderrors later on

    # setting variables
    plate_pos = [0, 0, 0]
    

    thickness_wing = 6
    # add 3x3 tall base plate
    # if bottom is true then add a 3x3 plate to the bottom    
    if bottom:
        thi = thickness - thickness_wing
        pos = [plate_pos[0], plate_pos[1], plate_pos[2]+ thickness_wing]      
        extra_mm = 1 / ob.gv("osp")     
        th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width+ extra_mm, height=height+ extra_mm, depth=thi, pos=pos, mode="all"))
    else: # if it's the top
        thi = thickness_wing
        pos = [plate_pos[0], plate_pos[1], plate_pos[2]]      
        extra_mm = 1 / ob.gv("osp")     
        th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width+ extra_mm, height=height+ extra_mm, depth=thickness_wing, pos=pos, mode="all"))
    
    # add m6 holes
    # add the 3x3 ones
    th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=3, height=3, holes="corner", both_holes= True, pos=plate_pos,radius_name="m6", m=""))
    # add the extra for 5
    if width > 3:
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, holes=["top","bottom"], both_holes= True, pos=plate_pos,radius_name="m6", m=""))
    

    # add holes to join to a 6704 bearing plate
    bearing_plate_mount_hole_spacing = 18
    z = 50 - 12 #(use a 25 mm socket cap)
    poss = [[0,bearing_plate_mount_hole_spacing,z], [0,-bearing_plate_mount_hole_spacing,z]]
    for pos in poss:
        #add scoket_cap screw 25-12 from the top roty 180  and top clearance
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = "oobb_screw_socket_cap"
        p3["radius_name"] = "m3"
        p3["pos"] = pos
        p3["rotY"] = 0
        p3["include_nut"] = False
        p3["top_clearance"] = True
        p3["overhang"] = True
        p3["m"] = ""
        th.extend(ob.oobb_easy(**p3))
    
    ## add a 34mm diameter cutout 3mm off the bottom
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = "oobb_cylinder"
    p3["radius"] = 34/2
    if small:
        p3["radius"] = 27/2
    if bottom:        
        p3["depth"] = thickness - 2 + 1
        p3["pos"] = [0, 0, (thickness-2)/2 - 1/2]
    else: #all the way through if top
        p3["depth"] = 40
        p3["pos"] = [0, 0, (40-2)/2]
    p3["m"] = ""
    th.extend(ob.oobb_easy(**p3))
    ## add an 8mm hole at the bottom
    p3 = copy.deepcopy(kwargs)
    p3["s"] = "oobb_wire_clearance_square"
    p3["depth"] = 10
    p3["pos"] = [0, 0, thickness-2]
    p3["m"] = "#"    
    th.append(get_common(**p3))
    p3 = copy.deepcopy(p3)
    p3["pos"] = [5, 0, thickness-2]
    th.append(get_common(**p3))
    #add a tube to support the motor
    if bottom:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "pp"
        p3["shape"] = "oobb_cylinder"
        p3["radius"] = 12/2
        dep =4.5
        p3["depth"] = dep
        p3["pos"] = [0, 0, thickness - dep]    
        #p3["m"] = ""
        th.extend(ob.oobb_easy(**p3))
        p3 = copy.deepcopy(p3)
        p3["type"] = "nn"
        p3["radius"] = 8/2
        #p3["m"] = "#"
        th.extend(ob.oobb_easy(**p3))

    # add the connecting nuts for the wire piece
    poss = []
    z = 41
    poss.append([-7.5, 7.5, z])
    poss.append([-7.5, -7.5, z])

    for pos in poss:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = "oobb_nut"
        p3["radius_name"] = "m3"
        p3["pos"] = pos
        p3["zz"] = "top"
        p3["overhang"] = False
        p3["hole"]  = True
        p3["m"] = ""
        th.extend(ob.oobb_easy(**p3))



    return thing

def get_holder_motor_gearmotor_01(**kwargs):
    
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_pos = [-ob.gv("osp")/2, 0, 0]

    #add m6 holes
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width,
              height=height, depth=thickness, pos=plate_pos, mode="all"))
    #oobb holes
    holes = [[1, 1, "m6"], [2, 1, "m6"],  [3, 1, "m6"], [5, 1, "m6"], [1, 3, "m6"], [2, 3, "m6"],[3, 3, "m6"], [5, 3, "m6"], [6, 1, "m6"], [6, 2, "m6"], [6, 3, "m6"]]#, [4, 2, "m3"]]
    ##oobb holes m3
    holes_oobb = [[1.5, 1, "m3"],[1.5, 3, "m3"],[6, 1.5, "m3"],[6, 2.5, "m3"]]
    holes.extend(holes_oobb)
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, loc=loc,
                  height=height, holes="single", radius_name=hole[2], pos=plate_pos, m=""))
   
    ##holes for connecting wire retainer
    holes = []
    holes.append([0.5, 1.5, 180,0])
    holes.append([0.5, 2.5, 180,0])
    #for bearing plate
    holes.append([3, 1-3/ob.gv("osp"), 180,1.5])
    holes.append([3, 3+3/ob.gv("osp"), 180,1.5])
    holes.append([4+3/ob.gv("osp"), 2, 180,1.5])
    
    for hole in holes:
        #add countersink
        xy = oobb_base.get_hole_pos(hole[0], hole[1], width-1, height)        
        z = thickness + hole[3]
        rotY = hole[2]
        pos = [xy[0], xy[1], z]
        th.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", radius_name="m3", depth=thickness, pos=pos, m="", rotY=rotY, include_nut=False, top_clearance=True))
        pass

    # add bearing size hole

    th.extend(ob.oobb_easy(t="n", s="oobb_hole",
              radius_name=f'bearing_6704_od_catch', m=""))

    th.extend(ob.oobb_easy(t="n", s="oobb_motor_gearmotor_01", width=width,
              loc=loc, height=height, holes="single", pos=[0, 0, plate_pos[2]], screw_lift=1, m=""))

    
    return thing

def get_holder_motor_gearmotor_01_old_02(**kwargs):
    
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_pos = [-ob.gv("osp")/2, 0, -9]

    #add m6 holes
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width,
              height=height, depth=thickness, pos=plate_pos, mode="all"))
    #oobb holes
    holes = [[1, 1, "m6"], [2, 1, "m6"],  [3, 1, "m6"], [5, 1, "m6"], [1, 3, "m6"], [2, 3, "m6"],[3, 3, "m6"], [5, 3, "m6"], [6, 1, "m6"], [6, 2, "m6"], [6, 3, "m6"]]#, [4, 2, "m3"]]
    ##oobb holes
    holes_oobb = [[1.5, 1, "m3"],[1.5, 3, "m3"],[6, 1.5, "m3"],[6, 2.5, "m3"]]
    holes.extend(holes_oobb)
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, loc=loc,
                  height=height, holes="single", radius_name=hole[2], pos=plate_pos, m=""))
   
    ##holes for connecting wire retainer
    holes = []
    holes.append([0.5, 1.5, 180])
    holes.append([0.5, 2.5, 180])
    holes.append([3, 1-3/ob.gv("osp"), 180])
    holes.append([3, 3+3/ob.gv("osp"), 180])
    for hole in holes:
        #add countersink
        xy = oobb_base.get_hole_pos(hole[0], hole[1], width-1, height)        
        z = -6
        rotY = hole[2]
        pos = [xy[0], xy[1], z]
        th.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", radius_name="m3", depth=thickness, pos=pos, m="", rotY=rotY, include_nut=False))
        pass

    # add bearing size hole

    th.extend(ob.oobb_easy(t="n", s="oobb_hole",
              radius_name=f'bearing_6704_od_catch', m=""))

    th.extend(ob.oobb_easy(t="n", s="oobb_motor_gearmotor_01", width=width,
              loc=loc, height=height, holes="single", pos=[0, 0, plate_pos[2]], m=""))

    
    return thing

def get_holder_motor_gearmotor_01_old_01(**kwargs):
    ######old
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)
    ######old
    th = thing["components"]

    plate_pos = [-ob.gv("osp")/2, 0, -9]

    #add m6 holes
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width,
              height=height, depth=thickness, pos=plate_pos, mode="all"))
    #oobb holes
    ######old
    holes = [[1, 1, "m6"], [2, 1, "m6"],  [3, 1, "m6"], [5, 1, "m6"], [1, 3, "m6"], [2, 3, "m6"],[3, 3, "m6"], [5, 3, "m6"], [6, 1, "m6"], [6, 2, "m6"], [6, 3, "m6"], [4, 1-3/ob.gv("osp"), "m3"], [4, 3+3/ob.gv("osp"), "m3"] ]#, [4, 2, "m3"]]
    ##oobb holes
    holes_oobb = [[1.5, 1, "m3"],[1.5, 3, "m3"],[6, 1.5, "m3"],[6, 2.5, "m3"]]
    holes.extend(holes_oobb)
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, loc=loc,
                  height=height, holes="single", radius_name=hole[2], pos=plate_pos, m=""))
   
    ######old
    holes = []
    holes.append([1, 1.5, "m3"])
    holes.append([1, 2.5, "m3"])
    for hole in holes:
        #add countersink
        xy = oobb_base.get_hole_pos(hole[0], hole[1], width, height)        
        z = -6
        ######old
        pos = [xy[0], xy[1], z]
        th.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", radius_name="m3", depth=thickness, pos=pos, m="", rotY=180, include_nut=False))
        pass

    # add bearing size hole
    ######old
    th.extend(ob.oobb_easy(t="n", s="oobb_hole",
              radius_name=f'bearing_6704_od_catch', m=""))

    th.extend(ob.oobb_easy(t="n", s="oobb_motor_gearmotor_01", width=width,
              loc=loc, height=height, holes="single", pos=[0, 0, plate_pos[2]], m=""))
    ######old
    #adding half a bearing face to 3dpr version
    p2 = {  "type": "bp", 
            "width": 3, 
            "height": 3, 
            "thickness": 12,
            "bearing_type": "6704", 
            "size": "oobb", 
            "shaft": "motor_gearmotor_01"
            }
    p3 = copy.deepcopy(p2)
    
    p3.update({"pos": [0,0,-3]})
    p3.update({"only_screws": True})
    add_items = []
    p2.update({"no_screws": True})
    add_items.extend(get_bearing_plate(**p2)["components"])    
    add_items.extend(get_bearing_plate(**p3)["components"])
    add_items_output = []
    for item in add_items:
        inclusion = item.get("inclusion", "all")
        if inclusion == "all" or inclusion == "3dpr":
            #include
            item.update({"inclusion": "3dpr"})
            #item.update({"m": "#"})
            add_items_output.append(item)
        else:
            #exclude
            pass
    th.extend(add_items_output)
    
    # halfing it if 3dpr
    inclusion = "3dpr"
    th.append(ob.oobb_easy(t="n", s="cube", size=[
              500, 500, 500], pos=[-500/2, -500/2, 0], inclusion=inclusion, m=""))
    ######old

    return thing

def get_holder_motor_servo_standard_01_bottom_old_1(**kwargs):
    height = kwargs.get("height", 10)
    width = kwargs.get("width", 10)
    thickness = kwargs.get("thickness", 3)

    thickness_base_plate = thickness - 12


    thing =  get_holder_motor_servo_standard_01_old_1(**kwargs)
    th = thing["components"]
    #remove all things with type p or positive
    for items in th:
        #if item isn't an array make it one skip if a dict
        if isinstance(items, dict):
            items = [items]
            for item in items:
                #invert the positive pieces
                if item["type"] == "p" or item["type"] == "p":
                    #th.remove(item)
                    item["type"] = "n"

    plate_depth = 0
    plate_pos = [-ob.gv("osp"), 0, plate_depth]

    extra_mm = 1 / ob.gv("osp") 
    pos = [plate_pos[0], plate_pos[1], plate_pos[2]-thickness_base_plate]
    
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width+ extra_mm, height=height+ extra_mm, depth=thickness_base_plate, pos=pos, mode="all"))

    return thing

def get_holder_motor_servo_standard_01_old_1(**kwargs):

    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    t = kwargs.get("type", "n")
    #set pos
    kwargs["pos"] = pos
    th = thing["components"]

    plate_depth = 0
    plate_pos = [-ob.gv("osp"), 0, plate_depth]

    extra_mm = 1 / ob.gv("osp") 
    
    #thin full plate
    pos = [plate_pos[0], plate_pos[1], plate_pos[2]]
    #th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width, height=height, depth=thickness-9, pos=pos, mode="all"))
    #3x3 plate
    #thickness_base_plate = 6
    thickness_base_plate = 15
    pos = [plate_pos[0], plate_pos[1], plate_pos[2]-thickness_base_plate]
    
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width+ extra_mm, height=height+ extra_mm, depth=thickness_base_plate, pos=pos, mode="all"))
    
    #add 01_03s top and bottom
    thickness_full = 15
    #pos = [plate_pos[0]+15*2, plate_pos[1], plate_pos[2]-thickness_full]
    #piece_thickness = 12
    #th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=1+ extra_mm, height=height+ extra_mm, depth=piece_thickness, pos=pos, mode="all"))

    #wid = 1.5+ extra_mm
    #pos = [plate_pos[0]-15*2+(wid-1)*7.5-.5, plate_pos[1], plate_pos[2]#-thickness_full]
    #piece_thickness = 15
    #th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=wid, height=height+ extra_mm, depth=piece_thickness, pos=pos, mode="all"))



    #add m6 holes
    #m6 holes
    holes = []
    #m6 holes
    x = [1,2,3,5]
    y = [1,3]
    #add bottom and top row
    for x1 in x:
        for y1 in y:
            holes.append([x1,y1,"m6"])
    #add middle row
    holes.append([1,2,"m6"])
    # m3 holes
    x = [1.5,2.5]
    y = [1,3]
    #add bottom and top row
    for x1 in x:
        for y1 in y:
            holes.append([x1,y1,"m3"])
    #add middle row
    holes.append([1,1.5,"m3"])
    holes.append([1,2.5,"m3"])
    
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, loc=loc, height=height, holes="single", radius_name=hole[2], pos=plate_pos, m=""))

    # add bearing size hole

    # circle clearance
    
    

    #bearing clearance
    radius = 24/2
    depth = 250
    pos = [0, 0, -depth/2]
    th.extend(ob.oobb_easy(t="n", s="oobb_cylinder", radius=radius, pos=pos, depth=depth, m=""))
    
    #top clearance

    # servo cutout
    # zero is base of shaft
    pos = [0, 0, -2]
    th.extend(ob.oobb_easy(t="n", s="oobb_motor_servo_standard_01", part="all", bottom_clearance=True, include_screws=True, top_clearance=True, overhang=True, pos=pos, m=""))

    # bearing attachments
    holes = []
    holes.append([0,18,0,"m3"])
    holes.append([0,-18,0,"m3"])
    for hole in holes:
        p2 = copy.deepcopy(kwargs)
        p2.pop("size")
        p2["type"] = "n"
        p2["shape"] = "oobb_screw_socket_cap"
        p2["radius_name"] = hole[3]
        p2["pos"][0] = hole[0]
        p2["pos"][1] = hole[1]
        p2["pos"][2] = hole[2]-4
        p2["depth"] = 25
        p2["rotY"] = 180        
        p2["top_clearance"] = True
        p2["include_nut"] = False
        #p2["m"] = "#"
        if "bottom" in t: #the type passed to the routine but not type                         
            screw_extra = 15 # 40 mm screw
            p2["depth"] = p2["depth"] + screw_extra #go to 30
            #p2["m"] = "#"            
            p2["pos"][2] = p2["pos"][2] - screw_extra
            p2["overhang"] = True



        th.append(ob.oobb_easy(**p2))



    
    return thing

def get_holder_motor_servo_standard_01_old(**kwargs):

    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_depth = -(thickness + 6)
    plate_pos = [-ob.gv("osp"), 0, plate_depth]

    
    #thin full plate
    pos = [plate_pos[0], plate_pos[1], plate_pos[2]]
    #th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width, height=height, depth=thickness-9, pos=pos, mode="all"))
    #3x3 plate
    pos = [plate_pos[0], plate_pos[1], plate_pos[2]]
    piece_thickness = 9
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width, height=height, depth=piece_thickness, pos=pos, mode="all"))
    
    #add m6 holes
    #m6 holes
    holes = []
    #m6 holes
    x = [1,2,3,5]
    y = [1,3]
    #add bottom and top row
    for x1 in x:
        for y1 in y:
            holes.append([x1,y1,"m6"])
    #add middle row
    holes.append([1,2,"m6"])
    # m3 holes
    x = [1.5,2.5]
    y = [1,3]
    #add bottom and top row
    for x1 in x:
        for y1 in y:
            holes.append([x1,y1,"m3"])
    #add middle row
    holes.append([1,1.5,"m3"])
    holes.append([1,2.5,"m3"])
    
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, loc=loc, height=height, holes="single", radius_name=hole[2], pos=plate_pos, m=""))

    # add bearing size hole

    # circle clearance
    
    

    #bearing clearance
    radius = 26/2
    depth = 6
    pos = [0, 0, -depth/2]
    th.extend(ob.oobb_easy(t="n", s="oobb_cylinder", radius=radius, pos=pos, depth=depth, m=""))
    
    #top clearance

    # servo cutout
    # zero is base of shaft
    pos = [0, 0, 2]
    th.extend(ob.oobb_easy(t="n", s="oobb_motor_servo_standard_01", part="all", bottom_clearance=True, include_screws=True, pos=pos, m=""))

    #bp screws
    #adding half a bearing face to 3dpr version
    add_items = []
    p2 = {  "type": "bp", 
            "width": 3, 
            "height": 3, 
            "pos": [0,0,-3],
            "thickness": 12,
            "bearing_type": "6704", 
            "size": "oobb", 
            "only_screws": True,  
            "m": "#"          
            }
    add_items.extend(get_bearing_plate(**p2)["components"])    
    add_items_output = []
    #only add 3dpr and remove back hole
    for item in add_items:
        #3dpr
        inclusion = item.get("inclusion", "all")
        if inclusion == "all" or inclusion == "3dpr":
            #include
            item.update({"inclusion": "3dpr"})
            #item.update({"m": "#"})
            pos = item.get("pos", [0,0,0])
            if pos[1] == 0 and pos[0] < 0:
                #exclude
                pass
            else:
                add_items_output.append(item)
        else:
            #exclude
            pass
        
    th.extend(add_items_output)

    
    return thing

def get_holder_motor_servo_micro_01(**kwargs):

    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_depth = -(thickness + 6)
    plate_pos = [-ob.gv("osp")/2, 0, plate_depth]

    
    #thin full plate
    pos = [plate_pos[0], plate_pos[1], plate_pos[2]]
    #th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width, height=height, depth=thickness-9, pos=pos, mode="all"))
    #3x3 plate
    pos = [plate_pos[0], plate_pos[1], plate_pos[2]]
    piece_thickness = 9
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width, height=height, depth=piece_thickness, pos=pos, mode="all"))
    
    #add m6 holes
    #m6 holes
    holes = [[1, 1, "m6"], [2, 1, "m6"],  [4, 1, "m6"], [1, 3, "m6"], [2, 3, "m6"], [4, 3, "m6"], [1, 2, "m6"]]
    #m3 holes
    holes.extend([ [1, 1.5, "m3"] ,[1, 2.5, "m3"] ])
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, loc=loc, height=height, holes="single", radius_name=hole[2], pos=plate_pos, m=""))

    # add bearing size hole

    # circle clearance
    
    

    #bearing clearance
    radius = 26/2
    depth = 6
    pos = [0, 0, -depth/2]
    th.extend(ob.oobb_easy(t="n", s="oobb_cylinder", radius=radius, pos=pos, depth=depth, m=""))
    #screw clearance
    radius = 10/2
    pos = [-20, 0, -depth/2]
    th.extend(ob.oobb_easy(t="n", s="oobb_cylinder", radius=radius, pos=pos, depth=depth, m=""))
    
    #top clearance

    # servo cutout
    # zero is base of shaft
    pos = [0, 0, 0]
    th.extend(ob.oobb_easy(t="n", s="oobb_motor_servo_micro_01", part="all", bottom_clearance=True, pos=pos, m="#"))

    #bp screws
    #adding half a bearing face to 3dpr version
    add_items = []
    p2 = {  "type": "bp", 
            "width": 3, 
            "height": 3, 
            "pos": [0,0,-3],
            "thickness": 12,
            "bearing_type": "6704", 
            "size": "oobb", 
            "only_screws": True,  
            "m": "#"          
            }
    #add_items.extend(get_bearing_plate(**p2)["components"])    
    add_items_output = []
    #only add 3dpr and remove back hole
    for item in add_items:
        #3dpr
        inclusion = item.get("inclusion", "all")
        if inclusion == "all" or inclusion == "3dpr":
            #include
            item.update({"inclusion": "3dpr"})
            #item.update({"m": "#"})
            pos = item.get("pos", [0,0,0])
            if pos[1] == 0 and pos[0] < 0:
                #exclude
                pass
            else:
                add_items_output.append(item)
        else:
            #exclude
            pass
        
    th.extend(add_items_output)

    
    return thing

def get_holder_motor_stepper_motor_nema_17_flat(**kwargs):

    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    shift = kwargs.get("bearing_type", False)
    if shift == "shifted":
        shift = True
    th = thing["components"]

    if shift:
        shifter = width - 4
        plate_pos = [-ob.gv("osp")* shifter, 0, 0]
    else:
        plate_pos = [0, 0, 0]

    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width,
              height=height, depth=thickness, pos=plate_pos, mode="all"))
    #oobb holes
    holes = []
    for w in range(1, width+1):
        w_shif = w
        if shift:
            w_shif = w - shifter + 1
        for h in range(1, height+1):
            if not shift:
                if w == 1:
                    holes.append([w_shif, h, "m6"])            
                if w == width:
                    holes.append([w_shif, h, "m6"])
            else:
                if w < 3:
                    holes.append([w_shif, h, "m6"])
                #include a whole if w isnt one of the three middle holes
            middle = math.floor(height/2)+1
            if h != middle and h != middle-1 and h != middle+1:
                holes.append([w_shif, h, "m6"])
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, loc=loc,
                  height=height, holes="single", radius_name=hole[2], pos=plate_pos, m=""))
    #other holes
    cs = 31/2
    holes = [[cs,cs,"m3"],[-cs,cs,"m3"],[cs,-cs,"m3"],[-cs,-cs,"m3"]]
    holes.append([0,0,28/2])
    for hole in holes:
        loc = hole
        radius_name = hole[2]
        if thickness == 3 or radius_name != "m3":
        
            th.extend(ob.oobb_easy(t="n", s="oobb_hole", pos=[hole[0],hole[1],0], radius_name=radius_name, radius=radius_name, m=""))
        if  thickness > 3 and radius_name == "m3": #use socket cap screws if thickler than 3            
            z=thickness
            th.extend(ob.oobb_easy(t="n", s="oobb_screw_socket_cap", pos=[hole[0],hole[1],z], depth=thickness, radius_name=radius_name, radius=radius_name, flush_top = True, hole= True, include_nut=False, m="#"))
    
    if shift:
        # side belt escape
        size = [20, 20, 20]
        pos = [15, 0, 0]
        th.append(ob.oe(t="n", s="oobb_cube_center", holes="none", size=size, pos=pos, all= True, mode="all", m=""))

    
    return thing

def get_holder_motor_stepper_motor_nema_17_jack(**kwargs):
    osp = ob.gv("osp")
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 2)
    height = kwargs.get("height", 2)
    thickness = kwargs.get("thickness", 3)

    # solid piece
    th = thing["components"]

    height_cube = 13.5
    down_shift = - ob.gv("osp") * (height-1)
    y_plate = osp + (height-1)*ob.gv("osp")/2 + down_shift
    plate_pos = [0, y_plate, -thickness/2]


    th.extend(ob.oe(t="p", s="oobb_pl", holes="none", width=width, height=height,depth=thickness, pos=plate_pos, mode="all"))

    width_cube = ob.gv("osp")*width-ob.gv("osp_minus")

    th.append(ob.oobb_easy(t="p", s="cube", size=[
              width_cube, height_cube, thickness], pos=[-width_cube/2, down_shift, -thickness/2], mode="all", m=""))


    #oobb holes
    holes = []
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, loc=loc,
                  height=height, holes="single", radius_name=hole[2], pos=plate_pos, m=""))
    #middle holes
    holes = [[0,0,28/2]]
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_hole", pos=[hole[0],hole[1],0], radius_name=hole[2], radius=hole[2], m=""))

    #screws
    cs = 31/2
    holes = [[cs,cs,"m3"],[-cs,cs,"m3"],[cs,-cs,"m3"],[-cs,-cs,"m3"]]
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_screw_socket_cap", pos=[hole[0],hole[1],thickness/2], radius_name=hole[2], radius=hole[2], flush_top = True, include_nut = False, depth = thickness, m=""))


    # jack nut and bolt holes
    mode = "all"
    for x in range(0, width):
        x = (-width/2*ob.gv("osp")+ob.gv("osp")/2)+x*ob.gv("osp")
        y = height_cube + down_shift
        z = 0

        th.extend(ob.oobb_easy(t="n", s="oobb_hole", radius_name="m6",
                  depth=height_cube, pos=[x, y, z], rotX=90, mode=mode, m=""))

        # nut height
        y = -22.75 + 1.25
        th.extend(ob.oobb_easy(t="n", s="oobb_nut_through", radius_name="m6",
                  depth=height_cube, pos=[x, y, z], rotX=90, mode=mode, m=""))


    return thing

def get_holder_motor_stepper_motor_nema_17_both(**kwargs):
    
    osp = ob.gv("osp")  

    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 2)
    width = width - 1
    height = kwargs.get("height", 2)
    thickness = kwargs.get("thickness", 3)

    # solid piece
    p2 = copy.deepcopy(kwargs)
    p2["width"] = p2["width"] - 1
    thing["components"] = get_holder_motor_stepper_motor_nema_17_jack(**p2)["components"]
    th = thing["components"]


    y_flat = 0
    flat_pos = [-osp/2,y_flat,-thickness/2]


    #flat mount piece    
    th.extend(ob.oe(t="p", s="oobb_pl", holes="none", width=width+1, height=height,depth=thickness, pos=flat_pos, mode="all", m=""))

    # side belt escape
    size = [20, 20, 20]
    pos = [15, 0, 0]
    th.append(ob.oe(t="n", s="oobb_cube_center", holes="none", size=size, pos=pos, all= True, mode="all", m=""))

    #oobb holes (in reference to extra flat piece)
    holes = [[1,1,"m6"],[1,2,"m6"],[1,3,"m6"]]
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width+1, loc=loc,
                  height=height, holes="single", radius_name=hole[2], pos=flat_pos, m=""))

    return thing

def get_holder_powerbank_anker_323(**kwargs):

    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    #set pos
    kwargs["pos"] = pos

    th = thing["components"]

    plate_depth = -(thickness + 6)
    plate_pos = [0,0,0]

    
    #thin full plate
    pos = [plate_pos[0], plate_pos[1], plate_pos[2]]
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width, height=height, depth=thickness, pos=pos, mode="all"))

    """
    #add m6 holes
    #m6 holes
    holes = []
    #m6 holes
    x = range(1,13)
    y = [1,13]
    #add bottom and top row
    for x1 in x:
        for y1 in y:
            holes.append([x1,y1,"m6"])
    #add middle row
    #holes.append([1,2,"m6"])
    # m3 holes
    x = [1.5]
    y = [1,13]
    #add bottom and top row
    for x1 in x:
        for y1 in y:
            holes.append([x1,y1,"m3"])
    #add middle row
    #holes.append([1,1.5,"m3"])
    #holes.append([1,2.5,"m3"])
    
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, loc=loc, height=height, holes="single", pos=plate_pos,radius_name=hole[2], m=""))
    """
    th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height,  holes="perimeter", pos=plate_pos,radius_name="m6", m=""))        
    th.extend(ob.oobb_easy(t="n", s="oobe_holes", width=(width*2)-1, height=(height*2)-1,  holes="perimeter", pos=plate_pos,radius_name="m3", m=""))  
    
    # powerbank
    p2 = copy.deepcopy(kwargs)    
    p2.pop("size")
    p2["type"] = "n"
    p2["shape"] = "oobb_powerbank_anker_323"
    x = 0
    y = 0
    z = 2
    pos = [p2["pos"][0] + x, p2["pos"][1] + y, p2["pos"][2] + z]
    p2["pos"] = pos
    rotZ = 0
    rotY = 0
    rotX = 0
    p2["rotZ"] = rotZ
    p2["rotY"] = rotY
    p2["rotX"] = rotX
    #p2["m"] = ""
    th.extend(ob.oobb_easy(**p2))

    # cutout
    p2 = copy.deepcopy(kwargs)
    p2.pop("size")
    p2["type"] = "n"
    p2["shape"] = "oobb_cube_center"
    wid = 81
    hei = 160
    depth = 50
    extra = -10
    size = [wid + extra, hei + extra, depth]
    x = 0
    y = 0
    z = -depth/2
    pos = [p2["pos"][0] + x, p2["pos"][1] + y, p2["pos"][2] + z]
    p2["pos"] = pos
    p2["size"] = size
    #p2["m"] = ""
    th.append(ob.oobb_easy(**p2))

    
    return thing

def get_holder_electronics_base_03_03(**kwargs):
    th = []
    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)
    spacer_clearance = kwargs.get("spacer_clearance", False)
    holes = kwargs.get("holes", "all")

    plate_pos = [0, 0, 0]
    plate_pos_shift = [0, ob.gv("osp")/2 * (height-width), thickness-3]
    #3x3 main piece
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=3,
              height=3, depth=thickness, pos=plate_pos, mode="all"))
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width,
              height=height, depth=3, pos=plate_pos_shift, mode="all"))
    #oobb holes
    if holes == "all":
        holes = [[1, 1, "m6"],  [1, 3, "m6"], [3, 1, "m6"], [3, 3, "m6"], [2, 3, "m6"]]
        ##oobb holes m3
        holes_oobb = [[1.5, 3, "m3"],[2.5, 3, "m3"],[1, 1.5, "m3"],[1, 2.5, "m3"],[3, 1.5, "m3"],[3, 2.5, "m3"]]
    elif holes == "top":
        holes = [[1, 3, "m6"], [2, 3, "m6"], [3, 3, "m6"]]
        ##oobb holes m3
        holes_oobb = [[1.5, 3, "m3"],[2.5, 3, "m3"],]
        
    holes.extend(holes_oobb)
    for hole in holes:
        loc = hole
        th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=3, loc=loc,height=3, holes="single", radius_name=hole[2], pos=plate_pos, m=""))

    ### add all the extra holes for width after 3
    for y in range(4, height+1):
        for x in range(1, width+1):
            loc2 = [x, y]
            th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, radius_name="m6", holes="single", pos=plate_pos_shift, loc=loc2, m=""))
            loc2 = [x+.5, y]
            if x != width:
                th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, radius_name="m3", holes="single", pos=plate_pos_shift, loc=loc2, m=""))
            
            pass


   
    #add countersink
    ##holes for connecting wire retainer
    holes = []
    #holes.append([0.5, 1.5, 180])
    #holes.append([0.5, 2.5, 180])
    #for bearing plate
    holes.append([1, 2, 0])
    holes.append([3, 2, 0])
    
    
    for hole in holes:
        #add countersink
        xy = oobb_base.get_hole_pos(hole[0], hole[1], 3, 3)        
        z = thickness
        rotY = hole[2]
        pos = [xy[0], xy[1], z]
        th.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", radius_name="m3", depth=thickness, pos=pos, m="", rotY=rotY, include_nut=False))
        pass

    #add spacer
    if spacer_clearance:        
        p2 = copy.deepcopy(kwargs)
        pos = p2.get("pos", [0, 0, 0])
        p2["pos"] = [pos[0], pos[1], pos[2]]
        p2["type"] = "n"
        wid = 24
        hei = 21
        depth = thickness-3
        size = [wid, hei, depth]
        x = 0
        y = 0
        z = 0 
        pos = [p2["pos"][0] + x, p2["pos"][1] + y, p2["pos"][2] + z]
        p2["shape"] = "rounded_rectangle"
        p2["pos"] = pos
        p2["size"] = size    
        p2["inclusion"] = "all"
        p2["m"] =""          
        th.append(opsc.opsc_easy(**p2))

    # add bearing size hole
    return th

def get_holder_electronics_mcu_atmega328_shennie(**kwargs):
    kwargs["spacer_clearance"] = True
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_pos = [0, 0, 0]

    #add plate
    #th.extend(get_holder_electronics_base_03_03(**kwargs))
    #add oobb_pl
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width, height=height, depth=thickness, pos=plate_pos, mode="all"))
    #add u holes
    th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, radius_name="m6", holes=["top","bottom","right"], pos=plate_pos, m=""))
    th.extend(ob.oobb_easy(t="n", s="oobe_holes", width=(width*2)-1, height=(height*2)-1, radius_name="m3", holes=["top","bottom","right"], pos=plate_pos, m=""))
    
    th.extend(ob.oobb_easy(t="n", s="oobb_electronics_mcu_atmega328_shennie", width=width, height=height, holes="single", clearance=True, pos=[0, -6, plate_pos[2]+thickness-3], screw_lift=3, m =""))

    
    return thing

def get_holder_electronics_microswitch_standard(**kwargs):
    kwargs["spacer_clearance"] = True
    kwargs["holes"] = "top"
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_pos = [0, 0, 0]

    #add plate
    th.extend(get_holder_electronics_base_03_03(**kwargs))
    shift = 0
    if thickness == 12:
        shift = 1.5


    switches = []
    switches.append([0, -2.85, 0])
    switches.append([0, -13.15, 0])
    switches.append([10.3, -3, 90])
    switches.append([-10.3, -3, 90])

    for switch in switches:
        pos = [switch[0], switch[1], thickness+shift]
        th.extend(ob.oobb_easy(t="n", s="oobb_electronics_microswitch_standard", width=width, height=height, holes="single", rotZ=switch[2], nut_offset=-0,clearance=True, pos=pos, m =""))
   
    return thing

def get_holder_electronics_potentiometer_17(**kwargs):
    kwargs["spacer_clearance"] = True
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_pos = [0, 0, 0]

    #add plate
    th.extend(get_holder_electronics_base_03_03(**kwargs))
    shift = 0
    if thickness == 12:
        shift = 1.5

    th.extend(ob.oobb_easy(t="n", s="oobb_electronics_potentiometer_17", width=width, height=height, holes="single", clearance=True, pos=[0, 0, plate_pos[2]+thickness-3+shift], screw_lift=3, m =""))

    
    return thing

def get_holder_electronics_pushbutton_11(**kwargs):
    
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_pos = [0, 0, 0]

    #add plate
    kwargs["spacer_clearance"] = True
    th.extend(get_holder_electronics_base_03_03(**kwargs))
    shift = 0
    if thickness == 18:
        shift = 1.5

    th.extend(ob.oobb_easy(t="n", s="oobb_electronics_pushbutton_11", width=width, height=height, holes="single", clearance=True, pos=[0, 0, plate_pos[2]+thickness-3+shift], screw_lift=3, m =""))

    
    return thing

def get_holder_electronics_pushbutton_11_x4(**kwargs):
    
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_pos = [0, 0, 0]

    #add plate
    kwargs["spacer_clearance"] = True
    th.extend(get_holder_electronics_base_03_03(**kwargs))
    shift = 0
    if thickness == 18:
        shift = 1.5

    poss = []
    space = 6
    shift_y = 0
    shift_z = plate_pos[2]+thickness-3+shift
    poss.append([space, space+shift_y, shift_z])
    poss.append([-space, space+shift_y, shift_z])
    poss.append([space, -space+shift_y, shift_z])
    poss.append([-space, -space+shift_y, shift_z])

    for pos in poss:    
        th.extend(ob.oobb_easy(t="n", s="oobb_electronics_pushbutton_11", width=width, height=height, holes="single", clearance=True, pos=pos, screw_lift=3, m =""))

    
    return thing

def get_jack(**kwargs):
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 2)
    height = kwargs.get("height", 2)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", True)

    # solid piece
    th = thing["components"]

    height_cube = 13.5
    y_plate = height_cube + (height-1)*ob.gv("osp")/2

    th.extend(ob.oe(t="p", s="oobb_pl", holes=holes, width=width, height=height,
              depth=thickness, pos=[0, y_plate, -thickness/2], mode="all"))

    width_cube = ob.gv("osp")*width-ob.gv("osp_minus")

    th.append(ob.oobb_easy(t="p", s="cube", size=[
              width_cube, height_cube, thickness], pos=[-width_cube/2, 0, -thickness/2], mode="all"))

    # bolt holes
    mode = "all"
    for x in range(0, width):
        x = (-width/2*ob.gv("osp")+ob.gv("osp")/2)+x*ob.gv("osp")
        y = height_cube
        z = 0
        th.extend(ob.oobb_easy(t="n", s="oobb_hole", radius_name="m6", depth=height_cube, pos=[x, y, z], rotX=90, mode=mode, m=""))

        # nut height
        y = 9
        th.extend(ob.oobb_easy(t="n", s="oobb_nut_loose", radius_name="m6", depth=height_cube, pos=[x, y, z], rotX=90, mode=mode, m=""))

    rot_current = 0
    for x in range(0, width-1):
        x = (-width/2*ob.gv("osp")+ob.gv("osp"))+x*ob.gv("osp")
        y = height_cube
        z = thickness/2

        th.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", radius_name="m3", depth=thickness, pos=[x, y, z], mode=mode, sandwich=True, m="", rotY=rot_current, include_nut=True))
        rot_current = rot_current + 180

    # halfing it if 3dpr
    inclusion = "3dpr"
    th.append(ob.oobb_easy(t="n", s="cube", size=[
              500, 500, 500], pos=[-500/2, -500/2, 0], inclusion=inclusion, m=""))

    return thing

def get_jack_basic(**kwargs):
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 2)
    height = kwargs.get("height", 2)
    thickness = kwargs.get("thickness", 3)

    # solid piece
    th = thing["components"]

    height_cube = 13.5
    y_plate = height_cube + (height-1)*ob.gv("osp")/2

    plate_pos = [0, y_plate, -thickness/2]
    th.extend(ob.oe(t="p", s="oobb_pl", width=width, height=height,
              depth=thickness, both_holes=True, pos=plate_pos, mode="all"))

    th.extend(ob.oe(t="n", s="oobb_holes", size="oobe", radius_name="m3", width=(width*2)-1, height=(height*2)-1,pos = plate_pos, m="#"))

    width_cube = ob.gv("osp")*width-ob.gv("osp_minus")

    th.append(ob.oobb_easy(t="p", s="cube", size=[
              width_cube, height_cube, thickness], pos=[-width_cube/2, 0, -thickness/2], mode="all"))

    # bolt holes
    mode = "all"
    for x in range(0, width):
        x = (-width/2*ob.gv("osp")+ob.gv("osp")/2)+x*ob.gv("osp")
        y = height_cube
        z = 0

        th.extend(ob.oobb_easy(t="n", s="oobb_hole", radius_name="m6",
                  depth=height_cube, pos=[x, y, z], rotX=90, mode=mode, m=""))

        # nut height
        y = 9
        th.extend(ob.oobb_easy(t="n", s="oobb_nut_through", radius_name="m6",
                  depth=height_cube, pos=[x, y, z], rotX=90, mode=mode, m=""))

# add m3 countersunk joining screws
    rot_current = 0
    for x in range(0, width-1):
        x = (-width/2*ob.gv("osp")+ob.gv("osp"))+x*ob.gv("osp")
        y = height_cube
        z = thickness/2

        th.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", radius_name="m3", depth=thickness, pos=[
                  x, y, z], mode="laser", rotZ=360/12, sandwich=True, m="", rotY=rot_current))
        rot_current = rot_current + 180

    return thing

def get_jig(**kwargs):
    extra = kwargs.get("extra")
    kwargs.pop("extra")
    kwargs["type"] = f'jig_{extra}'
    if extra != "":
        # Get the module object for the current file
        current_module = __import__(__name__)
        function_name = "get_jig_" + extra
        # Call the function using the string variable
        function_to_call = getattr(current_module, function_name)
        return function_to_call(**kwargs)
    else:
        Exception("No extra")

def get_jig_tray_03_03(**kwargs):
   
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_pos = [0, 0, 0]

    #add plate
    th.append(ob.oobb_easy(t="p", s="oobb_plate", pos=plate_pos, width=width, height=height, depth=thickness, m =""))

    th.append(ob.oobb_easy(t="p", s="oobb_holes", pos=plate_pos, width=width, height=height, holes=["top","bottom"], m =""))
    th.append(ob.oobb_easy(t="p", s="oobe_holes", pos=plate_pos, width=(width*2)-1, height=(height*2)-1, radius_name="m3", holes=["top","bottom"], m =""))

    
    #inset 
    inset_depth = 2
    ex = 1
    th.append(ob.oobb_easy(t="n", s="oobb_plate", pos=[plate_pos[0],plate_pos[1],plate_pos[2]+thickness-inset_depth], width=3+ex/15, height=3+ex/15, depth=inset_depth, m =""))
    # flow inset
    th.append(ob.oobb_easy(t="n", s="oobb_plate", pos=[plate_pos[0],plate_pos[1],plate_pos[2]+thickness-inset_depth], width=2.75, height=7, depth=inset_depth, m =""))


    extra = "tr_03_03_jig"


    th.extend(ob.oobb_easy(t="n", text=extra,concate=False,s="oobb_text", size=6, pos=[0,0,0.3], rotY=180, rotZ=90, m=""))

    nuts = []
    nuts.append([2,2])
    nuts.append([4,2])
    nuts.append([2,4])
    nuts.append([4,4])
    #for 3x2
    nuts.append([3,4])
    nuts.append([3,2])
    for nut in nuts:
    
        x,y = ob.get_hole_pos(wid = width,hei=height, x=nut[0], y=nut[1])
        z = thickness - 1
        th.extend(ob.oe(t="n", s="oobb_nut", loose=True,pos=[x,y,z], radius_name="m3", zz="top", overhang=False,m=""))
        th.extend(ob.oe(t="n", s="oobb_hole", pos=[x,y,z], radius_name="m3",m=""))
    
    
    return thing

def get_jig_screw_sorter_m3_03_03(**kwargs):
   
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    

    plate_pos = [0, 0, 0]

    #add plate
    thing["components"] = get_tray(**kwargs)["components"]
    th = thing["components"]

    extra = "tr_03_03_jig"


    #th.extend(ob.oobb_easy(t="n", text=extra,concate=False,s="oobb_text", size=6, pos=[0,0,0.3], rotY=180, rotZ=90, m=""))

    #do a grid width wide and height tall
    for x in range(1, (width*2)):
        for y in range(1, (height*2)): 
            #skip corners   
            if not (x == 1 and y == 1) and not (x == 1 and y == (height*2)-1) and not (x == (width*2)-1 and y == 1) and not (x == (width*2)-1 and y == (height*2)-1):            
                xx,yy = ob.get_hole_pos(size="oobe", wid = (width*2)-1,hei=(height*2)-1, x=x, y=y)
                zz = 3            
                th.extend(ob.oe(t="n", s="oobb_screw_countersunk", pos=[xx,yy,zz], radius_name="m3_sort",top_clearance=True, include_nut=False, m=""))           
            
    
    
    return thing

def get_mounting_plate(**kwargs):
    kwargs = copy.deepcopy(kwargs)
    kwargs["hole_pattern"] = "perimeter"
    #make x_shift 0
    kwargs["x_shift"] = 0
    kwargs["y_shift"] = 0
    return get_mounting_plate_generic(**kwargs)

def get_mounting_plate_side(**kwargs):
    kwargs = copy.deepcopy(kwargs)
    kwargs["hole_pattern"] = "top"
    #make x_shift 0
    kwargs["x_shift"] = ob.gv("osp")/2    
    kwargs["y_shift"] = 0
    return get_mounting_plate_generic(**kwargs)

def get_mounting_plate_top(**kwargs):
    kwargs = copy.deepcopy(kwargs)
    kwargs["hole_pattern"] = "left"
    #make x_shift 0
    kwargs["x_shift"] = 0
    kwargs["y_shift"] = ob.gv("osp")/2    
    return get_mounting_plate_generic(**kwargs)

def get_mounting_plate_generic(**kwargs):
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 2)
    height = kwargs.get("height", 2)
    depth = kwargs.get("depth", 3)
    width_mounting = kwargs.get("width_mounting", 10)
    height_mounting = kwargs.get("height_mounting", 10)
    mounting_holes = kwargs.get("mounting_holes", "")
    radius_hole = kwargs.get("radius_hole", "m3")
    hole_pattern = kwargs.get("hole_pattern", "perimeter")
    x_shift = kwargs.get("x_shift", 0)
    y_shift = kwargs.get("y_shift", 0)
    extra = kwargs.get("extra", "")
    standoff = kwargs.get("standoff", True)
    pos_original = kwargs.get("pos", [0, 0, 0])

    if extra != "":        
        split = extra.split("_")
        #string to dict each element is named it's index
        split_dict = {}
        for i in range(0, len(split)):
            split_dict[str(i)] = split[i]
        extras = {}
        extras["width"] = float(split_dict.get("2", 10))
        extras["height"] = float(split_dict.get("4", 10))
        extras["x"] = float(split_dict.get("6", 0))
        extras["y"] = float(split_dict.get("8", 0))

    th = thing["components"]
    th.append(ob.oobb_easy(t="p", s="oobb_plate", width=width,
              height=height, depth=depth, pos=[0, 0, 0]))
    th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, pos=[0, 0, 0], holes=hole_pattern, radius_name="m6", both_holes=True, diameter=0))
    
    # add mounting holes
    if mounting_holes == "":
        mounting_holes = []
        hole = {}
        hole["x"] = width_mounting/2
        hole["y"] = height_mounting/2
        mounting_holes.append(hole)
        hole = {}
        hole["x"] = -width_mounting/2
        hole["y"] = height_mounting/2
        mounting_holes.append(hole)
        hole = {}
        hole["x"] = width_mounting/2
        hole["y"] = -height_mounting/2
        mounting_holes.append(hole)
        hole = {}
        hole["x"] = -width_mounting/2
        hole["y"] = -height_mounting/2
        mounting_holes.append(hole)
        
    for hole in mounting_holes:
        hole["x"] = hole["x"] + x_shift
        hole["y"] = hole["y"] + y_shift
        pos = [hole["x"], hole["y"], 0]
        th.extend(ob.oobb_easy(t="n", s="oobb_hole", pos=pos, radius_name=radius_hole, m=""))
        pos = [hole["x"], hole["y"], 0]
        depth2 = depth + 4 #should be the right height for a 12 mm countersunk screw
        if standoff:
            th.extend(ob.oobb_easy(t="p", s="oobb_hole_standoff", pos=pos, radius_name=radius_hole, depth = depth2, m=""))
        pos = [hole["x"], hole["y"], 0]
        th.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", rot=[0,180,0], pos=pos, radius_name=radius_hole, depth=depth2, include_nut=False, m=""))

    if extra != "":
        p3 = copy.deepcopy(kwargs)
        pos1 = copy.deepcopy(pos_original)
        p3["type"] = "negative"
        p3["shape"] = "oobb_cube_center"
        p3["size"] = [extras["width"], extras["height"], 100]
        pos1[0] += extras["x"]
        pos1[1] += extras["y"]
        pos1[2] += -100/2
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)

    return thing

def get_mounting_plate_u(**kwargs):
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)
    width_mounting = kwargs.get("width_mounting", 10)
    height_mounting = kwargs.get("height_mounting", 10)
    radius_hole = kwargs.get("radius_hole", "m3")
    overwrite = kwargs.get("overwrite", True)

    th = thing["components"]
    th.append(ob.oobb_easy(t="p", s="oobb_plate", width=width,
              height=height, depth=depth, pos=[0, 0, 0]))
    th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width,
              height=height, pos=[0, 0, 0], holes="u", radius_name=radius_hole))
    # add mounting holes
    th.extend(ob.oobb_easy(t="n", s="oobb_hole", pos=[
              width_mounting/2, height_mounting/2+ob.gv("osp")/2, 0], radius_name=radius_hole, m=""))
    th.extend(ob.oobb_easy(t="n", s="oobb_hole",
              pos=[-width_mounting/2, height_mounting/2+ob.gv("osp")/2, 0], radius_name=radius_hole, m=""))
    th.extend(ob.oobb_easy(t="n", s="oobb_hole", pos=[
              width_mounting/2, -height_mounting/2+ob.gv("osp")/2, 0], radius_name=radius_hole, m=""))
    th.extend(ob.oobb_easy(t="n", s="oobb_hole",
              pos=[-width_mounting/2, -height_mounting/2+ob.gv("osp")/2, 0], radius_name=radius_hole, m=""))

    return thing

def get_plate_old(**kwargs):

    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    hole_type = kwargs.get("hole_type", "all")
    full_object = kwargs.get("full_object", True)

    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    pos = kwargs.get("pos", [0, 0, 0])

    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width,
              height=height, depth=thickness, pos=pos, m=""))
    # find the start point needs to be half the width_mm plus half ob.gv("osp")
    if holes:
        th.extend(ob.oobb_easy(t="n", s=f"{size}_holes", pos=pos, width=width, holes=hole_type, height=height, both_holes=both_holes))   
        
    ##extra
    if "gorm" in extra:
        holes = [10,25,40]
        for h in holes:
            y = (math.floor(height/2) + height%2 ) * ob.gv("osp")
            posa = [h,y,0]
            th.extend(ob.oobb_easy(t="n", s=f"oobb_hole", radius_name="m6", pos=posa, m="#"))
            posa = [-h,0,0]
            th.extend(ob.oobb_easy(t="n", s=f"oobb_hole", radius_name="m6", pos=posa, m="#"))
    if "slip_center" in extra:
        posa = [0,0,0]
        th.extend(ob.oobb_easy(t="n", s=f"oobb_hole", radius=9.4/2, pos=posa, m=""))
        posb = [0,0,thickness/2]
        th.extend(ob.oobb_easy(t="p", s=f"oobb_cylinder", radius=20/2, depth=thickness, pos=posb, m=""))
    if "slip_end" in extra:
        posa = [(width-1)/2 * 15,0,0]
        th.extend(ob.oobb_easy(t="n", s=f"oobb_hole", radius=9.4/2, pos=posa, m=""))
        posb = [(width-1)/2 * 15,0,thickness/2]
        th.extend(ob.oobb_easy(t="p", s=f"oobb_cylinder", radius=20/2, depth=thickness, pos=posb, m=""))
    if "slip_corner" in extra:
        posa = [(width-1)/2 * 15,(height-1)/2 * 15,0]
        th.extend(ob.oobb_easy(t="n", s=f"oobb_hole", radius=9.4/2, pos=posa, m=""))
        posb = [(width-1)/2 * 15,(height-1)/2 * 15,thickness/2]
        th.extend(ob.oobb_easy(t="p", s=f"oobb_cylinder", radius=20/2, depth=thickness, pos=posb, m=""))
    
    if full_object:   
        return thing
    else: # only return the elements
        return th

def get_shaft_coupler(**kwargs):
    thing = ob.get_default_thing(**kwargs)

    diameter = kwargs.get("diameter", "")
    thickness = kwargs.get("thickness", "")
    
    pos = kwargs.get("pos", [0, 0, 0])

    # solid piece
    th = thing["components"]
    #kwargs.update({"exclude_d3_holes": True})
    kwargs.update({"exclude_center_holes": True})
    
    #th.extend(get_circle(**kwargs)["components"])
    # adding connecting screws
    spac = 7.5
    holes = [[0,spac],[spac,0],[-spac,0],[0,-spac]]
    for h in holes:
        th.extend(ob.oobb_easy(t="n", s="oobb_hole", pos=[h[0],h[1],0], radius=7/2, m=""))


    return thing

def get_shaft(**kwargs):
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    radius_hole = kwargs.get("radius_hole", "m3")
    extra = kwargs.get("extra", "")

    top_radius = 14/2
    if "small" in extra:
        top_radius = 10/2
    if "washer" in extra:
        top_radius = 2/2


    th = thing["components"]

    th.extend(ob.oobb_easy(t="p", s="oobb_cylinder", radius=top_radius, depth=3, pos=[0, 0, 0]))
    
    th.extend(ob.oobb_easy(t="p", s="oobb_cylinder", radius_name="hole_radius_little_m6", depth=thickness+3, pos=[0, 0, thickness/2]))    
    th.extend(ob.oobb_easy(t="n", s="oobb_hole", radius_name="m3", pos=[0, 0, 0]))
    
    if "countersunk" in extra:
        th.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk",
              radius_name="m3", pos=[0, 0, -1.5], depth= thickness + 3, include_nut = False, rot = [0,180,0], m=""))
    
    if "nut" in extra:
        th.extend(ob.oobb_easy(t="n", s="oobb_nut", radius_name="m3", pos=[0, 0, -1.5], zz="bottom", overhang=True, m=""))

    return thing

def get_smd_magazine_old_1(**kwargs):

    width = kwargs.get("width", 1)
    width_mm = width * ob.gv("osp") - ob.gv("osp_minus")
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    plate_pos = [0, 0, 0]

    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width, 
    height=height, depth=thickness, pos=plate_pos, m=""))
    #add holes
    holes = []
    holes.append([1,1])
    holes.append([1,height])
    holes.append([width,1])
    
    if extra <= 2:
         #holes.append([width,height])
         pass
    for h in holes:
        if h[0] == 1:
            x = -((width) / 2 * ob.gv("osp")) + h[0] * ob.gv("osp") - ob.gv("osp") /2
            y = -((height) / 2 * ob.gv("osp")) + h[1] *  ob.gv("osp") - ob.gv("osp") /2
            z = -125
            w = 15
            x= x - w/2
            depth = 250
            pos = [x,y,z]
            rotZ = 0
            th.append(ob.oobb_easy(t="n", s="oobb_slot", radius_name="m6", pos=pos, rotZ=rotZ, depth=depth, w=w, m =""))
        else:
            th.append(ob.oobb_easy(t="p", s="oobb_holes", pos=plate_pos, width=width, height=height, holes=["single"], loc=h, m =""))

    #cutout
    diameter = width*ob.gv("osp")-ob.gv("osp_minus")-3
    thickness_wall = 1
    

    cosmetic_extra = 3
    thickness_cylinder = thickness-thickness_wall + cosmetic_extra
    z_cylinder = thickness_cylinder/2 + thickness_wall
    #extra cutout for 3x3
    if width == 3:
        diameter = diameter - 7
        th.append(ob.oobb_easy(t="n", s="oobb_cube_center", size=[11,8,thickness_cylinder], pos = [5.5,15,z_cylinder-thickness_cylinder/2], rotZ=0, m="") )
    
    
    th.append(ob.oobb_easy(t="n", s=f"oobb_cylinder", radius=diameter/2, 
    height=height, depth=thickness_cylinder, pos=[0, 0, z_cylinder], m=""))
    # center cylinder
    s = "oobb_cylinder"
    diameter = 20
    thi = thickness
    pos = [0,0,0]
    th.append(ob.oobb_easy(t="n", s=s, radius=diameter/2, depth=thi, pos=pos, m=""))

    #escape
    s = "oobb_cube_center"
    height_escape = extra
    top_space = 3
    #      main    
    wid = width_mm/2 
    hei = height_escape
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm / 4
    y = width_mm/2 - top_space - height_escape/2
    z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    #      top cutout    
    wid = width_mm/8 
    hei = height_escape + top_space
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm / 16 * 7
    y = width_mm/2 - hei / 2
    #z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    #      ape escape
    wid = 7.5
    hei = 1.5
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm / 6
    y = width_mm/2+1.5
    #z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, rotZ=-45, m="")) 


    return thing

def get_smd_magazine_lid(**kwargs):
    
    width = kwargs.get("width", 1)
    width_mm = width * ob.gv("osp") - ob.gv("osp_minus")
    height = kwargs.get("height", 1)
    thickness = 0.6
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    if width == 2:
        plate_pos = [-7.5, 0, 0]

        #main plate
        th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width, 
        height=height, depth=thickness, pos=plate_pos, m=""))
        #hole extension plate
        import copy
        pos = copy.deepcopy(plate_pos)
        pos[0] = pos[0] + 7.5
        pos[1] = pos[1] - 7.5
        th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=2, 
        height=1, depth=thickness, pos=pos, m=""))
        s = "oobb_hole"
        radius_name = "m6"
        pos = [7.5,-7.5,0]
        th.append(ob.oobb_easy(t="n", s=s, radius_name=radius_name, pos=pos, m=""))
            
    else:
        

        plate_pos = [0, 0, 0]

        th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width, 
        height=height, depth=thickness, pos=plate_pos, m=""))
        #add holes
        holes = []
        holes.append([1,1])
        holes.append([1,height])
        holes.append([width,1])
        if width == 13:
            minus = [1,2]
            for minu in minus:
                holes.append([1+minu,1])
                holes.append([1,1+minu])

                holes.append([width-minu,1])
                holes.append([width,1+minu])

                holes.append([1+minu,height])
                holes.append([1,height-minu])
                
                #holes.append([width-minu,height])
                holes.append([width,height-minu])
            

        for h in holes:
            if h[0] == 1 and h[1] == 1 or h[0] == 1 and h[1] == height:
                x = -((width) / 2 * ob.gv("osp")) + h[0] * ob.gv("osp") - ob.gv("osp") /2
                y = -((height) / 2 * ob.gv("osp")) + h[1] *  ob.gv("osp") - ob.gv("osp") /2
                z = -125
                w = 15
                x= x - w/2
                depth = 250
                pos = [x,y,z]
                rotZ = 0
                th.append(ob.oobb_easy(t="n", s="oobb_slot", radius_name="m6", pos=pos, rotZ=rotZ, depth=depth, w=w, m =""))
            else:
                th.append(ob.oobb_easy(t="p", s="oobb_holes", pos=plate_pos, width=width, height=height, holes=["single"], loc=h, m =""))

    #topcorner square off cube
    s = "oobb_cube_center"
    wid = 6
    hei = 6
    thi = thickness
    size = [wid,hei,thi]
    x = plate_pos[0] - width_mm / 2 + wid/2
    y = width_mm/2 - hei/2
    z = 0
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="p", s=s, size=size, pos=pos, m=""))


    # center cylinder
    s = "oobb_cylinder"
    diameter = 13
    thi = thickness
    pos = [plate_pos[0],plate_pos[1],thi/2]
    th.append(ob.oobb_easy(t="n", s=s, radius=diameter/2, depth=thi, pos=pos, m=""))

    
    return thing

def get_smd_magazine(**kwargs):
    #label size 4 + 25 x thickness - 1
    # 3 25 x 9
    # 2 
    # 8mm tape 25 x 9 
    #   
    width = kwargs.get("width", 1)
    
    if width < 3:
        return get_smd_magazine_small(**kwargs)
    elif width > 12:
        return get_smd_magazine_large(**kwargs)
    
    width_mm = width * ob.gv("osp") - ob.gv("osp_minus")
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    tape_thickness = extra
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    plate_pos = [0, 0, 0]

    #main_plate
    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width, 
    height=height, depth=thickness, pos=plate_pos, m=""))
    
    #topcorner square off cube
    s = "oobb_cube_center"
    wid = 6
    hei = 6
    thi = thickness
    size = [wid,hei,thi]
    x = plate_pos[0] - width_mm / 2 + wid/2
    y = width_mm/2 - hei/2
    z = 0
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="p", s=s, size=size, pos=pos, m=""))
    
    #label_inset
    s = "oobb_cube_center"
    inset = 0.5
    wid = 32
    if width == 3:
        wid = 25
    hei = 1
    thi = min(thickness - inset * 2, 16)
    size = [wid,hei,thi]
    centering_extra = (thickness - thi - inset * 2) / 2
    x = plate_pos[0] - width_mm / 2 + wid/2 + inset + centering_extra
    y = width_mm/2 - hei/2
    z = pos[2]+inset
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    
    
    
    #add holes
    holes = []
    holes.append([1,1])
    holes.append([1,height])
    holes.append([width,1])
    if width == 13:
        minus = [1,2]
        for minu in minus:
            holes.append([1+minu,1])
            holes.append([1,1+minu])

            holes.append([width-minu,1])
            holes.append([width,1+minu])

            holes.append([1+minu,height])
            holes.append([1,height-minu])
            
            #holes.append([width-minu,height])
            holes.append([width,height-minu])
        

    for h in holes:
        if h[0] == 1 and h[1] == 1 or h[0] == 1 and h[1] == height:
            x = -((width) / 2 * ob.gv("osp")) + h[0] * ob.gv("osp") - ob.gv("osp") /2
            y = -((height) / 2 * ob.gv("osp")) + h[1] *  ob.gv("osp") - ob.gv("osp") /2
            z = -125
            w = 15
            x= x - w/2
            depth = 250
            pos = [x,y,z]
            rotZ = 0
            th.append(ob.oobb_easy(t="n", s="oobb_slot", radius_name="m6", pos=pos, rotZ=rotZ, depth=depth, w=w, m =""))
        else:
            th.append(ob.oobb_easy(t="p", s="oobb_holes", pos=plate_pos, width=width, height=height, holes=["single"], loc=h, m =""))

    """
    label bracket not used anymore
    #add hole for label bracket
    hole_depth = 9
    x = -width_mm/2
    y = width_mm/2 - (15-1)/2
    z = thickness/2
    dep = hole_depth    
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s="oobb_hole", pos=pos, rotY=90, depth = dep, radius_name="m3", m =""))
    #add cube for nut insertion
    s = "oobb_cube_center"   
    wid = 3
    hei = 6
    thi = thickness/2 + 3.5
    size = [wid,hei,thi]
    x = x + hole_depth - wid / 2
    y = y
    z = thickness - thi
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    """



    #cutout
    diameter = width*ob.gv("osp")-ob.gv("osp_minus")-6
    #thickness_wall = 1 # 4 layers maybe
    thickness_wall = 0.6 # two layers
    #if width == 13:
    #    thickness_wall = 0.3 # two maybe one layer
    cosmetic_extra = 3
    thickness_cylinder = thickness-thickness_wall + cosmetic_extra
    z_cylinder = thickness_cylinder/2 + thickness_wall
    #extra cutout for 3x3
    if width == 3:
        diameter = diameter -4
        th.append(ob.oobb_easy(t="n", s="oobb_cube_center", size=[11,8,thickness_cylinder], pos = [5.5,15,z_cylinder-thickness_cylinder/2], rotZ=0, m="") )
    
    
    th.append(ob.oobb_easy(t="n", s=f"oobb_cylinder", radius=diameter/2, 
    height=height, depth=thickness_cylinder, pos=[0, 0, z_cylinder], m=""))
    
    # center cylinder
    s = "oobb_cylinder"
    diameter = 13
    if width > 7:
        diameter = 30
    thi = thickness
    pos = [0,0,0]
    th.append(ob.oobb_easy(t="n", s=s, radius=diameter/2, depth=thi, pos=pos, m=""))

    #escape
    s = "oobb_cube_center"
    height_escape = tape_thickness
    top_space = 3
    #      main    
    wid = width_mm/2 
    hei = height_escape
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm / 4
    y = width_mm/2 - top_space - height_escape/2
    z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    #      top cutout    
    wid = 10
    if width == 3:
        wid = 6 
    hei = height_escape + top_space
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm / 2 - wid / 2
    y = width_mm/2 - hei / 2
    #z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    #      cutout to allow tape to peel back
    wid = 20+1
    if width == 3:
        wid = 15 + 1
    hei = height_escape + top_space
    thi = 1.5
    size = [wid,hei,thi]
    x = width_mm  / 2 - wid / 2
    y = width_mm/2 - hei / 2
    z = thickness - thi
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))

    #      tape escape
    wid = 7.5
    hei = 1.5
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm /2 - 20
    if width == 3:
        x = width_mm /2 - 15
    y = width_mm/2+1.5
    z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, rotZ=-45, m="")) 



    # tape guidance cylinder
    s = "oobb_slot"
    diameter = 2
    if width == 3:
        diameter = 5
    w = 5
    
    thi = thickness    
    start_x = 8.811
    shift_x = w/2 + 3
    shift_x_per = 2
    
    start_y = 25
    shift_y = -diameter/2
    shift_y_per = 7.5
    dot_guide_loc = {}
    dot_guide_loc[3] = [14,15]
    sh = 0
    x = start_x + shift_x + shift_x_per * sh
    
    y = start_y + shift_y + shift_y_per * sh
    dot_guide_loc[4] = [x,y]
    sh = 1
    dot_guide_loc[5] = [start_x+shift_x+shift_x_per*sh,start_y+shift_y+ shift_y_per * sh]
    sh = 3
    dot_guide_loc[7] = [start_x+shift_x+shift_x_per*sh,start_y+shift_y+ shift_y_per * sh]
    sh = 5
    x = start_x+shift_x+shift_x_per*sh -3
    dot_guide_loc[9] = [x,start_y+shift_y+ shift_y_per * sh]
    sh = 9
    x = start_x+shift_x+shift_x_per*sh -7
    dot_guide_loc[13] = [x,start_y+shift_y+ shift_y_per * sh]
    try:
        x = dot_guide_loc[width][0]
        y = dot_guide_loc[width][1]    
    except:
        x = 0
        y = 0
    z = 0

    ####add extra for thickness
    y = y - tape_thickness + 1.5
    if tape_thickness >= 8:
        x = x + 8


    pos = [x,y,z]
    th.append(ob.oobb_easy(t="pp", s=s, radius=diameter/2, depth=thi, pos=pos, w=w, m="#"))

    # extra cutout square for tape guiadance
    s = "oobb_cube_center"
    wid = (w + diameter)/2 + 4
    hei = diameter
    thi = thickness - thickness_wall
    size = [wid,hei,thi]
    x = x -wid + 2
    y = y
    z = z + thickness_wall
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))

    

    return thing

def get_smd_magazine_large(**kwargs):
    #label size 4 + 25 x thickness - 1
    # 3 25 x 9
    # 2 
    # 8mm tape 25 x 9 
    #   
    width = kwargs.get("width", 1)
    
    if width < 3:
        return get_smd_magazine_small(**kwargs)
    
    width_mm = width * ob.gv("osp") - ob.gv("osp_minus")
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    tape_thickness = extra
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    plate_pos = [0, 0, 0]

    #main_plate
    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width, 
    height=height, depth=thickness, pos=plate_pos, m=""))
    
    #topcorner square off cube
    s = "oobb_cube_center"
    wid = 6
    hei = 6
    thi = thickness
    size = [wid,hei,thi]
    x = plate_pos[0] - width_mm / 2 + wid/2
    y = width_mm/2 - hei/2
    z = 0
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="p", s=s, size=size, pos=pos, m=""))
    
    #label_inset
    s = "oobb_cube_center"
    inset = 0.5
    wid = 32
    if width == 3:
        wid = 25
    hei = 1
    thi = min(thickness - inset * 2, 16)
    size = [wid,hei,thi]
    centering_extra = (thickness - thi - inset * 2) / 2
    x = plate_pos[0] + width_mm/2  - 45
    y = width_mm/2 - hei/2
    z = pos[2]+inset
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    
    
    
    #add holes
    holes = []
    holes.append([1,1])
    holes.append([1,height])
    holes.append([width,1])
    if width == 13:
        minus = [1,2]
        for minu in minus:
            holes.append([1+minu,1])
            holes.append([1,1+minu])

            holes.append([width-minu,1])
            holes.append([width,1+minu])

            holes.append([1+minu,height])
            holes.append([1,height-minu])
            
            #holes.append([width-minu,height])
            holes.append([width,height-minu])
        

    for h in holes:
        if h[0] == 1 and h[1] == 1 or h[0] == 1 and h[1] == height:
            x = -((width) / 2 * ob.gv("osp")) + h[0] * ob.gv("osp") - ob.gv("osp") /2
            y = -((height) / 2 * ob.gv("osp")) + h[1] *  ob.gv("osp") - ob.gv("osp") /2
            z = -125
            w = 15
            x= x - w/2
            depth = 250
            pos = [x,y,z]
            rotZ = 0
            th.append(ob.oobb_easy(t="n", s="oobb_slot", radius_name="m6", pos=pos, rotZ=rotZ, depth=depth, w=w, m =""))
        else:
            th.append(ob.oobb_easy(t="p", s="oobb_holes", pos=plate_pos, width=width, height=height, holes=["single"], loc=h, m =""))

    """
    label bracket not used anymore
    #add hole for label bracket
    hole_depth = 9
    x = -width_mm/2
    y = width_mm/2 - (15-1)/2
    z = thickness/2
    dep = hole_depth    
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s="oobb_hole", pos=pos, rotY=90, depth = dep, radius_name="m3", m =""))
    #add cube for nut insertion
    s = "oobb_cube_center"   
    wid = 3
    hei = 6
    thi = thickness/2 + 3.5
    size = [wid,hei,thi]
    x = x + hole_depth - wid / 2
    y = y
    z = thickness - thi
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    """



    #cutout
    diameter = width*ob.gv("osp")-ob.gv("osp_minus")-6
    #thickness_wall = 1 # 4 layers maybe
    thickness_wall = 0.6 # two layers
    #if width == 13:
    #    thickness_wall = 0.3 # two maybe one layer
    cosmetic_extra = 3
    thickness_cylinder = thickness-thickness_wall + cosmetic_extra
    z_cylinder = thickness_cylinder/2 + thickness_wall
    #extra cutout for 3x3
    if width == 3:
        diameter = diameter -4
        th.append(ob.oobb_easy(t="n", s="oobb_cube_center", size=[11,8,thickness_cylinder], pos = [5.5,15,z_cylinder-thickness_cylinder/2], rotZ=0, m="") )
    
    
    
    th.append(ob.oobb_easy(t="n", s=f"oobb_cylinder", radius=diameter/2, 
    height=height, depth=thickness_cylinder, pos=[0,0,z_cylinder],m=""))

    w = 100
    rotZ = -20
    dep = thickness_cylinder
    # shift x and y based on the angle in rotZ and the width of the cutout use trigonometry 
    x = -w/2 * math.cos(math.radians(rotZ))
    y = -w/2 * math.sin(math.radians(rotZ))
    z = z_cylinder - dep/2
    dia = diameter - 10
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=f"oobb_slot", radius=dia/2, 
    height=height, depth=dep, w=w, pos=pos, rotZ = rotZ,m=""))
    
    # center cylinder
    s = "oobb_cylinder"
    diameter = 13
    if width > 7:
        diameter = 30
    thi = thickness
    pos = [0,0,0]
    th.append(ob.oobb_easy(t="n", s=s, radius=diameter/2, depth=thi, pos=pos, m=""))

    #escape
    s = "oobb_cube_center"
    height_escape = tape_thickness
    top_space = 3
    #      main    
    wid = width_mm/2 
    hei = height_escape
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm / 4
    y = width_mm/2 - top_space - height_escape/2
    z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    #      top cutout    
    wid = 10
    if width == 3:
        wid = 6 
    hei = height_escape + top_space
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm / 2 - wid / 2
    y = width_mm/2 - hei / 2
    #z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    #      cutout to allow tape to peel back
    wid = 20+1
    if width == 3:
        wid = 15 + 1
    hei = height_escape + top_space
    thi = 1.5
    size = [wid,hei,thi]
    x = width_mm  / 2 - wid / 2
    y = width_mm/2 - hei / 2
    z = thickness - thi
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))

    #      tape escape
    wid = 7.5
    hei = 1.5
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm /2 - 20
    if width == 3:
        x = width_mm /2 - 15
    y = width_mm/2+1.5
    z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, rotZ=-45, m="")) 



    # tape guidance cylinder
    s = "oobb_slot"
    diameter = 2
    if width == 3:
        diameter = 5
    w = 5
    thi = thickness    
    start_x = 8.811
    shift_x = w/2 + 3
    shift_x_per = 2
    
    start_y = 25
    shift_y = -diameter/2
    shift_y_per = 7.5
    dot_guide_loc = {}
    dot_guide_loc[3] = [14,15]
    sh = 0
    x = start_x + shift_x + shift_x_per * sh
    y = start_y + shift_y + shift_y_per * sh
    dot_guide_loc[4] = [x,y]
    sh = 1
    dot_guide_loc[5] = [start_x+shift_x+shift_x_per*sh,start_y+shift_y+ shift_y_per * sh]
    sh = 3
    dot_guide_loc[7] = [start_x+shift_x+shift_x_per*sh,start_y+shift_y+ shift_y_per * sh]
    sh = 5
    x = start_x+shift_x+shift_x_per*sh -3
    dot_guide_loc[9] = [x,start_y+shift_y+ shift_y_per * sh]
    sh = 9
    x = start_x+shift_x+shift_x_per*sh -7
    dot_guide_loc[13] = [x,start_y+shift_y+ shift_y_per * sh]
    try:
        x = dot_guide_loc[width][0]
        y = dot_guide_loc[width][1]    
    except:
        x = 0
        y = 0
    z = 0

    ####add extra for thickness
    y = y - tape_thickness + 1.5
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="pp", s=s, radius=diameter/2, depth=thi, pos=pos, w=w, m=""))

    # extra cutout square for tape guiadance
    s = "oobb_cube_center"
    wid = (w + diameter)/2 + 4
    hei = diameter
    thi = thickness - thickness_wall
    size = [wid,hei,thi]
    x = x -wid + 2
    y = y
    z = z + thickness_wall
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))

    

    return thing

def get_smd_magazine_small(**kwargs):
    #label size 14 x thickness - 1
    # 8mm tape 14x9
    width = kwargs.get("width", 1)
    
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    plate_extra = 3
    width_mm = width * ob.gv("osp") - ob.gv("osp_minus")  + plate_extra
    
    
    plate_pos = [0, 0, 0]

    #main plate
    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width+plate_extra/15, 
    height=height+plate_extra/15, depth=thickness, pos=plate_pos, m=""))
    #hole extension plate
    import copy
    pos = copy.deepcopy(plate_pos)
    pos[0] = pos[0] + 7.5 
    pos[1] = pos[1] - 7.5 - plate_extra/2
    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=2, 
    height=1, depth=thickness, pos=pos, m=""))
    
    #topcorner square off cube
    s = "oobb_cube_center"
    wid = 6
    hei = 6
    thi = thickness
    size = [wid,hei,thi]
    x = plate_pos[0] - width_mm / 2 + wid/2
    y = plate_pos[1] + width_mm/2 - hei/2
    z = pos[2]
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="p", s=s, size=size, pos=pos, m=""))
    
    #label_inset
    s = "oobb_cube_center"
    inset = 0.5
    wid = 14
    hei = 0.5
    thi = thickness - inset * 2
    size = [wid,hei,thi]
    x = plate_pos[0] - width_mm / 2 + wid/2 + inset
    y = width_mm/2 - hei/2
    z = pos[2]+inset
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    """
    #front square off
    #front  square off cube
    s = "oobb_cube_center"
    wid = 6
    wid_block = wid
    hei = 15-1
    thi = thickness
    size = [wid,hei,thi]
    x = width_mm / 2 + wid/2
    y = -width_mm/2 + hei/2
    z = 0
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="p", s=s, size=size, pos=pos, m=""))
    
    #front label_inset
    s = "oobb_cube_center"
    inset = 0.5
    wid = 1
    hei = 12
    thi = thickness - inset * 2
    size = [wid,hei,thi]
    x = x  + wid_block/2 - wid/2
    y = y
    z = pos[2]+inset
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    """
    s = "oobb_hole"
    radius_name = "m6"
    pos = [7.5+7.5,-7.5-plate_extra/2,0]
    th.append(ob.oobb_easy(t="n", s=s, radius_name=radius_name, pos=pos, m=""))
    
    
    #cutout for label cylinder
    extra_diameter = 3
    diameter = width_mm-6 + extra_diameter
    #thickness_wall = 1 # 4 layers maybe
    thickness_wall = 0.6 # two layers
    cosmetic_extra = 3
    thickness_cylinder = thickness-thickness_wall + cosmetic_extra
    z_cylinder = thickness_cylinder/2 + thickness_wall    
    s = "oobb_cylinder"
    diameter = diameter
    radius = diameter/2
    thi = thickness_cylinder
    x = plate_pos[0] - extra_diameter/2 + 1
    y = 0 - extra_diameter/2 + plate_extra/2
    z = z_cylinder
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, radius=radius, depth=thi, pos=pos, m=""))
    
    # center cylinder
    s = "oobb_cylinder"
    diameter = 13
    thi = thickness
    pos = [pos[0],pos[1],0]
    th.append(ob.oobb_easy(t="n", s=s, radius=diameter/2, depth=thi, pos=pos, m=""))
    
    #escape
    s = "oobb_cube_center"
    height_escape = extra
    top_space = 3
    #      main escape
    wid = width_mm/2 
    hei = height_escape
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm / 4
    y = width_mm/2 - top_space - height_escape/2 + plate_extra/2
    z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    
      
    #      cutout to allow tape to peel back
    wid = width_mm/2 - 2
    
    hei = height_escape + top_space
    thi = 1.5
    size = [wid,hei,thi]
    x = width_mm  / 2 - wid / 2
    y = width_mm/2 - hei / 2 + plate_extra/2
    z = thickness - thi
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))

    #      tape escape
    wid = 10
    hei = 1.5
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm /2 - 14
    
    y = width_mm/2 + 3.5 
    z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, rotZ=-45, m="")) 



    # tape guidance cylinder
    s = "oobb_slot"
    diameter = 2
    w = 5
    thi = thickness    
    dot_guide_loc = {}
    dot_guide_loc[2] = [plate_pos[0]+11.5,9+plate_extra]
    sh = 0
    
    try:
        x = dot_guide_loc[width][0]
        y = dot_guide_loc[width][1]    
    except:
        x = 0
        y = 0
    z = 0
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="pp", s=s, radius=diameter/2, depth=thi, pos=pos, w=w, m=""))

    # extra cutout square for tape guiadance
    s = "oobb_cube_center"
    wid = (w + diameter)/2 + 4
    hei = diameter
    thi = thickness - thickness_wall
    size = [wid,hei,thi]
    x = x -wid + 2
    y = y 
    z = z + thickness_wall
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))

      

    return thing

def get_smd_magazine_small_old(**kwargs):
    #label size 12 x thickness - 1
    # 8mm tape 12x9
    width = kwargs.get("width", 1)
    width_mm = width * ob.gv("osp") - ob.gv("osp_minus")
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    plate_pos = [-7.5, 0, 0]

    #main plate
    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width, 
    height=height, depth=thickness, pos=plate_pos, m=""))
    #hole extension plate
    import copy
    pos = copy.deepcopy(plate_pos)
    pos[0] = pos[0] + 7.5
    pos[1] = pos[1] - 7.5
    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=2, 
    height=1, depth=thickness, pos=pos, m=""))
    
    #topcorner square off cube
    s = "oobb_cube_center"
    wid = 6
    hei = 6
    thi = thickness
    size = [wid,hei,thi]
    x = plate_pos[0] - width_mm / 2 + wid/2
    y = width_mm/2 - hei/2
    z = pos[2]
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="p", s=s, size=size, pos=pos, m=""))
    
    #label_inset
    s = "oobb_cube_center"
    inset = 0.5
    wid = 12
    hei = 1
    thi = thickness - inset * 2
    size = [wid,hei,thi]
    x = plate_pos[0] - width_mm / 2 + wid/2 + inset
    y = width_mm/2 - hei/2
    z = pos[2]+inset
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))

    #front square off
    #front  square off cube
    s = "oobb_cube_center"
    wid = 6
    wid_block = wid
    hei = 15-1
    thi = thickness
    size = [wid,hei,thi]
    x = plate_pos[0] + width_mm / 2 - wid/2 + 7.5
    y = -width_mm/2 + hei/2
    z = 0
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="p", s=s, size=size, pos=pos, m=""))
    
    #front label_inset
    s = "oobb_cube_center"
    inset = 0.5
    wid = 1
    hei = 12
    thi = thickness - inset * 2
    size = [wid,hei,thi]
    x = x  + wid_block/2 - wid/2
    y = y
    z = pos[2]+inset
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))

    #add holes
    holes = []
    #holes.append([1,1])
    #holes.append([1,height])
    #holes.append([width,1])
    
    for h in holes:
        if h[0] == 1 and h[1] == 1:
            x = -((width) / 2 * ob.gv("osp")) + h[0] * ob.gv("osp") - ob.gv("osp") /2
            y = -((height) / 2 * ob.gv("osp")) + h[1] *  ob.gv("osp") - ob.gv("osp") /2
            z = -125
            w = 15
            x= x - w/2
            depth = 250
            pos = [x,y,z]
            rotZ = 0
            th.append(ob.oobb_easy(t="n", s="oobb_slot", radius_name="m6", pos=pos, rotZ=rotZ, depth=depth, w=w, m =""))
        else:
            th.append(ob.oobb_easy(t="p", s="oobb_holes", pos=plate_pos, width=width, height=height, holes=["single"], radius_name="m3", loc=h, m =""))
    
    s = "oobb_hole"
    radius_name = "m6"
    pos = [7.5,-7.5,0]
    th.append(ob.oobb_easy(t="n", s=s, radius_name=radius_name, pos=pos, m=""))
    s = "oobb_hole"
    radius_name = "m3"
    pos = [plate_pos[0]-7.5-7.5,7.5,0]
    #th.append(ob.oobb_easy(t="n", s=s, radius_name=radius_name, pos=pos, m=""))
    
    #cutout for label cylinder
    extra_diameter = 2.5
    diameter = width*ob.gv("osp")-ob.gv("osp_minus")-6 + extra_diameter
    #thickness_wall = 1 # 4 layers maybe
    thickness_wall = 0.6 # two layers
    cosmetic_extra = 3
    thickness_cylinder = thickness-thickness_wall + cosmetic_extra
    z_cylinder = thickness_cylinder/2 + thickness_wall    
    s = "oobb_cylinder"
    diameter = diameter
    radius = diameter/2
    thi = thickness_cylinder
    x = plate_pos[0] - extra_diameter/2
    y = 0 - extra_diameter/2
    z = z_cylinder
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, radius=radius, depth=thi, pos=pos, m=""))
    
    # center cylinder
    s = "oobb_cylinder"
    diameter = 13
    thi = thickness
    pos = [plate_pos[0],0,0]
    th.append(ob.oobb_easy(t="n", s=s, radius=diameter/2, depth=thi, pos=pos, m=""))

    #escape
    s = "oobb_cube_center"
    height_escape = extra
    top_space = 3
    #      main escape
    wid = width_mm/2+16 
    hei = height_escape
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm / 4
    y = width_mm/2 - top_space - height_escape/2
    z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    
    #      top cutout    
    wid = 10
    if width == 3:
        wid = 6 
    hei = height_escape + top_space
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm / 2 - wid / 2
    y = width_mm/2 - hei / 2
    #z = thickness_wall 
    pos = [x,y,z]
    #th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))
    
    #      cutout to allow tape to peel back
    wid = 20+1
    if width == 3:
        wid = 15 + 1
    hei = height_escape + top_space
    thi = 1.5
    size = [wid,hei,thi]
    x = width_mm  / 2 - wid / 2
    y = width_mm/2 - hei / 2
    z = thickness - thi
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))

    #      tape escape
    wid = 10
    hei = 1.5
    thi = thickness_cylinder
    size = [wid,hei,thi]
    x = width_mm /2 - 20 +1.25
    if width == 3:
        x = width_mm /2 - 15
    y = width_mm/2+1.5
    z = thickness_wall 
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, rotZ=-45, m="")) 



    # tape guidance cylinder
    s = "oobb_slot"
    diameter = 2
    w = 5
    thi = thickness    
    dot_guide_loc = {}
    dot_guide_loc[2] = [plate_pos[0]+10,9]
    sh = 0
    
    try:
        x = dot_guide_loc[width][0]
        y = dot_guide_loc[width][1]    
    except:
        x = 0
        y = 0
    z = 0
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="pp", s=s, radius=diameter/2, depth=thi, pos=pos, w=w, m=""))

    # extra cutout square for tape guiadance
    s = "oobb_cube_center"
    wid = (w + diameter)/2 + 4
    hei = diameter
    thi = thickness - thickness_wall
    size = [wid,hei,thi]
    x = x -wid + 2
    y = y
    z = z + thickness_wall
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))

    

    return thing

def get_smd_magazine_joiner(**kwargs):

    width = kwargs.get("width", 1)
    width_mm = width * ob.gv("osp") - ob.gv("osp_minus")
    height = 1
    thickness = 3        
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    plate_pos = [0,0,0]

    #long joiing plate
    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width, 
    height=height, depth=thickness, pos=plate_pos, m=""))

    
    #covering the side plate   
    pos =  [7.5, (width-1)/2*15-7.5, 0]
    width_minus= width - 1
    if width == 7:
        width_minus= width - 2
        pos =  [15, 30, 0]
    elif width == 9:
        width_minus= width - 2
        pos =  [15, 45, 0]
    elif width == 13:
        width_minus= width - 4
        pos =  [30, 60, 0]
    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width_minus, 
    height=width_minus, depth=thickness, pos=pos, m=""))
    
    
    
    
    
    #add holes
    th.append(ob.oobb_easy(t="p", s=f"oobb_holes", width=width, 
    height=height, depth=thickness, pos=plate_pos, m=""))
    #add holes
    #end pieces    
    x = (width-1) / 2 * 15
    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=1, 
    height=1, depth=thickness+6, pos=[x,0,0], m=""))
    
    #long extension
    wid = width - width_minus + 1 
    x = -x  + ((wid /2) * 15)  - 7.5
    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=wid,                            
    height=1, depth=thickness+6, pos=[x,0,0], m=""))
    
    #nut clearance
    x=(-width/2*15) +7.5 + ((width - width_minus) * 15)
    z= 9
    th.append(ob.oobb_easy(t="n", s=f"oobb_nut_loose", radius_name="m6", depth=thickness+3, pos=[x,0,z], zz="top", m=""))
    
    return thing

def get_smd_magazine_refiller(**kwargs):

    width = kwargs.get("width", 1)
    width_mm = width * ob.gv("osp") - ob.gv("osp_minus")
    height = width
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    

    thickness_knob = 6
    plate_pos = [0, 0, thickness_knob/2]
    th.append(ob.oobb_easy(t="p", s=f"oobb_cylinder", radius=width_mm/2, depth=thickness_knob, pos=plate_pos, m=""))
    #add holes
    holes = []
    if width == 3:
        holes.append([1,2])
        holes.append([2,1])
        holes.append([2,3])
        holes.append([3,2])
    #holes.append([2,2])  
    if width == 4:
        holes.append([2.5,1])
        holes.append([2.5,4])
        holes.append([4,2.5])
        holes.append([1,2.5])

    for h in holes:
        th.append(ob.oobb_easy(t="p", s="oobb_holes", pos=plate_pos, width=width, height=height, holes=["single"], loc=h, m =""))
    
    ##catcher
    thickness_catcher = 20
    diameter_catcher = 13-1
    if extra == "big":
        diameter_catcher = 30-1
    pos = [0,0,thickness_catcher/2+thickness_knob/2]
    plate_pos = copy.deepcopy(plate_pos)
    th.append(ob.oobb_easy(t="p", s=f"oobb_cylinder", radius=diameter_catcher/2, depth=thickness_catcher, pos=pos, m=""))
    

    #cutout for tape
    #escape
    s = "oobb_cube_center"
    #      main    
    
    wid = width_mm + 10
    hei = 1.75
    if extra == "big":
        hei = 4.5
    thi = thickness_catcher
    size = [wid,hei,thi]
    x = 0
    y = 0
    z = thickness_knob
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))  

    return thing

def get_smd_magazine_label_holder(**kwargs):

    width = kwargs.get("width", 1)
    width_mm = width * ob.gv("osp") - ob.gv("osp_minus")
    height = width
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    

    #cutout for tape
    #escape
    s = "oobb_cube_center"
    #      main    
    
    width_holder = 30
    if width == 5:
        width_holder = 40
    height_holder = thickness
    thickness_holder = 2

    wid = width_holder
    hei = height_holder
    thi = thickness_holder
    size = [wid,hei,thi]
    x = 0
    y = 0
    z = 0
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="p", s=s, size=size, pos=pos, m=""))  


    s = "oobb_cube_center"
    #      window
    
    wid = width_holder - 4
    hei = height_holder   -4 
    thi = thickness_holder
    size = [wid,hei,thi]
    x = 0
    y = 0
    z = 0
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))  

    #label_curout
    wid = width_holder - 1
    hei = height_holder   - 2
    thi = thickness_holder- 1
    size = [wid,hei,thi]
    x = -0.5
    y = 0
    z = 1
    pos = [x,y,z]
    th.append(ob.oobb_easy(t="n", s=s, size=size, pos=pos, m=""))  

    #bracket_bit
    width_bracket = 3    
    wid = width_bracket
    hei = height_holder
    thi = 15
    size = [wid,hei,thi]
    x = -width_holder/2 - width_bracket / 2
    y = 0
    z = 0
    pos = [x,y,z]

    #hole
    x = -width_holder/2 - 10
    y = 0
    z = 9
    dep = 20
    th.append(ob.oobb_easy(t="n", s="oobb_hole", pos=[x,y,z], rotY=90, depth=dep, radius_name="m3", m="#"))

    th.append(ob.oobb_easy(t="p", s=s, size=size, pos=pos, m=""))  

    return thing

def get_soldering_jig(**kwargs):
    extra = kwargs.get("extra")
    kwargs.pop("extra")
    kwargs["type"] = f'soldering_jig_{extra}'
    if extra != "":
        # Get the module object for the current file
        current_module = __import__(__name__)
        function_name = "get_soldering_jig_" + extra
        # Call the function using the string variable
        function_to_call = getattr(current_module, function_name)
        return function_to_call(**kwargs)
    else:
        Exception("No extra")

def get_soldering_jig_electronics_mcu_pi_pico_socket(**kwargs):
    
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_pos = [0, 0, 0]

    #add plate
    kwargs["spacer_clearance"] = True
    th.append(ob.oobb_easy(t="p", s="oobb_plate", pos=plate_pos, width=width, height=height, depth=thickness, m =""))

    th.append(ob.oobb_easy(t="p", s="oobb_holes", pos=plate_pos, width=width, height=height, holes=["left","right","top","bottom"], m =""))
    th.append(ob.oobb_easy(t="p", s="oobe_holes", pos=plate_pos, width=(width*2)-1, height=(height*2)-1, radius_name="m3", holes=["left","right","top","bottom"], m =""))

    i2 = ob.gv("i2d54", "true")
    x = 3.5*i2
    y = (20-1)/2*i2
    z = thickness+1.5# lift ti up a bit
    zz = "top"
    th.append(ob.oobb_easy(t="n", s="oobb_electronics_socket_i2d54_20", pos=[x,y,z], zz = zz, m ="#"))
    th.append(ob.oobb_easy(t="n", s="oobb_electronics_socket_i2d54_20", pos=[-x,y,z], zz = zz, m ="#"))

    extra = "mcu_pi_pico_s"
    

    th.extend(ob.oobb_easy(t="n", text=extra,concate=False,s="oobb_text", size=6, pos=[0,0,0.3], rotY=180, rotZ=90, m="#"))

    
    return thing

def get_tool_holder(**kwargs):
    extra = kwargs.get("extra")
    kwargs.pop("extra")
    kwargs["type"] = f'th_{extra}'
    if extra != "":
        # Get the module object for the current file
        current_module = __import__(__name__)
        function_name = "get_tool_holder_" + extra
        # Call the function using the string variable
        function_to_call = getattr(current_module, function_name)
        return function_to_call(**kwargs)
    else:
        Exception("No extra")

def get_tool_holder_tool_holder_basic(**kwargs):
    thing = ob.get_default_thing(**kwargs)


    pos = kwargs.get("pos", [0, 0, 0])
    
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    pos[2] = pos[2] - thickness/2

    # solid piece
    th = thing["components"]    
    
    th.append(ob.oobb_easy(t="p", s="oobb_plate", width=width, height=height, depth=thickness, pos=pos))
    #add corner holes
    th.extend(ob.oobb_easy(t="n", s="oobb_holes", pos=pos, width=width, height=height, holes="corners", m=""))
    tool_pos_z = 3
    tools = []
    tools.append(["oobb_tool_side_cutters_generic_110_mm_red",4,2,3])
    tools.append(["oobb_tool_pliers_needlenose_generic_130_mm_blue",4,3,3])
    tools.append(["oobb_tool_wire_strippers_generic_120_red",4,4,3])    
    wera_row = 5.5
    wera_col = 1.5
    tools.append(["oobb_tool_screwdriver_hex_m1d5_wera_60_mm",wera_col,wera_row,3])
    tools.append(["oobb_tool_screwdriver_hex_m2_wera_60_mm",wera_col+1.5,wera_row,3])
    tools.append(["oobb_tool_screwdriver_hex_m2d5_wera_60_mm",wera_col+3,wera_row,3])
    tools.append(["oobb_tool_screwdriver_multi_quikpik_200_mm",2,8,3])
    tools.append(["oobb_tool_wrench_m7",6,wera_row,3])
    tools.append(["oobb_tool_wrench_m8",6,wera_row+1,3])    
    tools.append(["oobb_tool_wrench_m10",6,wera_row+2,3])    
    tools.append(["oobb_tool_wrench_m10",6,wera_row+3,3])
    tools.append(["oobb_tool_knife_exacto_17mm_black",4,8,3])
    #hex tools
    tools.append(["oobb_tool_allen_key_set_small_generic",2.5,1,thickness-40])
    tools.append(["oobb_tool_marker_black_sharpie",6,9.5,3])

    for tool in tools:
        x,y = oobb_base.get_hole_pos(tool[1], tool[2],width,height)
        tool_pos = [x, y, pos[2]+tool[3]]
        rv = ob.oobb_easy(t="n", s=tool[0], pos=tool_pos, m="#")
        #if rv is an array extend if its an array of arrays append
        if isinstance(rv[0], list):
            th.append(rv)
        else:
            th.extend(rv)     
    

    return thing

def get_tool_holder_tool_holder_basic_old_01(**kwargs):
    thing = ob.get_default_thing(**kwargs)


    pos = kwargs.get("pos", [0, 0, 0])
    
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    pos[2] = pos[2] - thickness/2

    # solid piece
    th = thing["components"]    
    
    th.append(ob.oobb_easy(t="p", s="oobb_plate", width=width, height=height, depth=thickness, pos=pos))
    #add corner holes
    th.extend(ob.oobb_easy(t="n", s="oobb_holes", pos=pos, width=width, height=height, holes="corners", m=""))
    tool_pos_z = 3
    tools = []
    tools.append(["oobb_tool_side_cutters_generic_110_mm_red",4,2,3])
    tools.append(["oobb_tool_pliers_needlenose_generic_130_mm_blue",4,3,3])
    tools.append(["oobb_tool_wire_strippers_generic_120_red",4,4,3])    
    wera_row = 5.5
    wera_col = 1.5
    tools.append(["oobb_tool_screwdriver_hex_m1d5_wera_60_mm",wera_col,wera_row,3])
    tools.append(["oobb_tool_screwdriver_hex_m2_wera_60_mm",wera_col+1.5,wera_row,3])
    tools.append(["oobb_tool_screwdriver_hex_m2d5_wera_60_mm",wera_col+3,wera_row,3])
    tools.append(["oobb_tool_screwdriver_multi_quikpik_200_mm",2,8,3])
    tools.append(["oobb_tool_wrench_m7",6,wera_row,3])
    tools.append(["oobb_tool_wrench_m8",6,wera_row+1,3])    
    tools.append(["oobb_tool_wrench_m10",6,wera_row+2,3])    
    tools.append(["oobb_tool_wrench_m10",6,wera_row+3,3])
    tools.append(["oobb_tool_knife_exacto_17mm_black",4,8,3])
    
    for tool in tools:
        x,y = oobb_base.get_hole_pos(tool[1], tool[2],width,height)
        tool_pos = [x, y, pos[2]+tool[3]]
        rv = ob.oobb_easy(t="n", s=tool[0], pos=tool_pos, m="#")
        #if rv is an array extend if its an array of arrays append
        if isinstance(rv[0], list):
            th.append(rv)
        else:
            th.extend(rv)     
    

    return thing

def get_tool_holder_vertical(**kwargs):
    kwargs["spacer_clearance"] = True
    thing = ob.get_default_thing(**kwargs)

    width = kwargs.get("width", 10)
    height = kwargs.get("height", 10)
    thickness = kwargs.get("thickness", 3)

    th = thing["components"]

    plate_pos = [0, 0, -1]

    #add plate
    #th.extend(get_holder_electronics_base_03_03(**kwargs))
    #add oobb_pl
    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width, height=height, depth=thickness, pos=plate_pos, mode="all"))
    #add u holes
    th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, radius_name="m6", holes=["bottom","top","left"], pos=plate_pos, m=""))
    th.extend(ob.oobb_easy(t="n", s="oobe_holes", width=(width*2)-1, height=(height*2)-1, radius_name="m3", holes=["bottom","top","left"], pos=plate_pos, m=""))
    
    # if extra is a string turn it itno an array
    extra = kwargs.get("extra", [])
    shift = 15
    cur_x = 0
    two_faces = False
    if extra == "tool_screwdriver_hex_wera_60_mm_x4":
        extra = []
        extra.append("tool_screwdriver_hex_m2d5_wera_60_mm")
        extra.append("tool_screwdriver_hex_m2d5_wera_60_mm")
        extra.append("tool_screwdriver_hex_m2d5_wera_60_mm")
        extra.append("tool_screwdriver_hex_m2d5_wera_60_mm")
        shift = 25/2
        cur_x = -37.5
    if extra == "tool_screwdriver_hex_wera_60_mm_x5":
        extra = []
        extra.append("tool_screwdriver_hex_m2d5_wera_60_mm")
        extra.append("tool_screwdriver_hex_m2d5_wera_60_mm")
        extra.append("tool_screwdriver_hex_m2d5_wera_60_mm")
        extra.append("tool_screwdriver_hex_m2d5_wera_60_mm")
        extra.append("tool_screwdriver_hex_m2d5_wera_60_mm")
        shift = 25/2
        cur_x = -50
    
    if extra == "tool_screwdriver_hex_wera_60_mm_x2":
        extra = []
        extra.append("tool_screwdriver_hex_m2d5_wera_60_mm")
        extra.append("tool_screwdriver_hex_m2d5_wera_60_mm")
        shift = 15
        cur_x = -15
    if extra == "tool_marker_bic_clear_lid_x6":
        extra = []
        extra.append("tool_marker_bic_clear_lid")
        extra.append("tool_marker_bic_clear_lid")
        extra.append("tool_marker_bic_clear_lid")
        extra.append("tool_marker_bic_clear_lid")
        extra.append("tool_marker_bic_clear_lid")
        extra.append("tool_marker_bic_clear_lid")
        shift = 15/2
        cur_x = -37.5    
    if extra == "tool_marker_german_big_x4":
        extra = []
        extra.append("tool_marker_german_big")
        extra.append("tool_marker_german_big")
        extra.append("tool_marker_german_big")
        extra.append("tool_marker_german_big")
        shift = 25/2
        cur_x = -37.5       
    if extra == "tool_marker_ikea_mala_x5":
        extra = []
        extra.append("tool_marker_ikea_mala")
        extra.append("tool_marker_ikea_mala")
        extra.append("tool_marker_ikea_mala")
        extra.append("tool_marker_ikea_mala")
        extra.append("tool_marker_ikea_mala")
        shift = 18.75/2
        cur_x = -37.5    
    if extra == "tool_marker_patterned_thicker_x6":
        extra = []
        extra.append("tool_marker_patterned_thicker")
        extra.append("tool_marker_patterned_thicker")
        extra.append("tool_marker_patterned_thicker")
        extra.append("tool_marker_patterned_thicker")
        extra.append("tool_marker_patterned_thicker")
        extra.append("tool_marker_patterned_thicker")
        shift = 15/2
        cur_x = -37.5    
    if extra == "tool_marker_sharpie_x2":
        extra = []
        extra.append("tool_marker_sharpie")
        extra.append("tool_marker_sharpie")
        shift = 15
        cur_x = -15
    if extra == "tool_marker_sharpie_x5":
        extra = []
        extra.append("tool_marker_sharpie")
        extra.append("tool_marker_sharpie")
        extra.append("tool_marker_sharpie")
        extra.append("tool_marker_sharpie")
        extra.append("tool_marker_sharpie")
        shift = 18.75/2
        cur_x = -37.5  
    if extra == "tool_marker_sharpie_x6":
        extra = []
        extra.append("tool_marker_sharpie")
        extra.append("tool_marker_sharpie")
        extra.append("tool_marker_sharpie")
        extra.append("tool_marker_sharpie")
        extra.append("tool_marker_sharpie")
        extra.append("tool_marker_sharpie")
        shift = 18.75/2
        cur_x = -46.875
    
    if extra == "tool_wrench_m10_x2":
        extra = []
        extra.append("tool_wrench_m10")
        extra.append("tool_wrench_m10")
        shift = 15
        cur_x = -15
    if extra == "tool_wrench_m10_x3":
        extra = []
        extra.append("tool_wrench_m10")
        extra.append("tool_wrench_m10")
        extra.append("tool_wrench_m10")
        shift = 15
        cur_x = -30
    if extra == "tool_wrench_m10_x4":
        extra = []
        extra.append("tool_wrench_m10")
        extra.append("tool_wrench_m10")
        extra.append("tool_wrench_m10")
        extra.append("tool_wrench_m10")
        shift = 15
        cur_x = -45
    if extra == "tool_tdpb_glue_stick_prit_medium_knife":
        extra = []        
        extra.append("tool_knife_exacto_17mm_black")
        extra.append("tool_tdpb_glue_stick_prit_medium")
        shift = 13
        cur_x = -15
        two_faces = True
    if extra == "tool_screwdriver_multi_quikpik_200_mm_knife":
        extra = []        
        extra.append("tool_knife_exacto_17mm_black")
        extra.append("tool_screwdriver_multi_quikpik_200_mm")
        shift = 15
        cur_x = -15
    if extra == "tool_screwdriver_driver_bit_x4":
        extra = []        
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        shift = 15/2
        cur_x = -22.5
    if extra == "tool_screwdriver_driver_bit_x6":
        extra = []        
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        shift = 15/2
        cur_x = -37.5
    if extra == "tool_screwdriver_driver_bit_x8":
        extra = []        
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        extra.append("tool_screwdriver_driver_bit")
        shift = 15/2
        cur_x = -52.5
    if extra == "tool_screwdriver_hex_key_set_small":
        extra = []        
        extra.append("tool_allen_key_hex_m1d5_small_generic")
        extra.append("tool_allen_key_hex_m2_small_generic")
        extra.append("tool_allen_key_hex_m2d5_small_generic")
        extra.append("tool_allen_key_hex_m3_small_generic")
        extra.append("tool_allen_key_hex_m4_small_generic")
        extra.append("tool_allen_key_hex_m5_small_generic")
        shift = 9/2
        cur_x = -22.5
        
    if extra == "tool_screwdriver_hex_key_set_small_reverse":
        extra = []        
        extra.append("tool_allen_key_hex_m5_small_generic")
        extra.append("tool_allen_key_hex_m4_small_generic")
        extra.append("tool_allen_key_hex_m3_small_generic")
        extra.append("tool_allen_key_hex_m2d5_small_generic")
        extra.append("tool_allen_key_hex_m2_small_generic")
        extra.append("tool_allen_key_hex_m1d5_small_generic")
        shift = 9/2
        cur_x = -22.5
        
    
    if isinstance(extra, str):
        extra = [extra]
    

    
    
    
    for e in extra:
        default_y = -30
        default_z = 0
        if "wera_60_mm" in e:
            default_y = -25
            default_z = -1
        elif "tdpb_nozzle_changer" in e:            
            default_y = -25
            default_z = -1
        elif "tool_tdpb_drill_cleaner_m3" in e:            
            default_y = -25
            default_z = -1
        elif "tool_tdpb_drill_cleaner_m6" in e:            
            default_y = -25
            default_z = -1

        elif "sharpie" in e:
            default_y = -25
            default_z = -1
        elif "bic" in e:
            default_y = -25
            default_z = -1
        elif "tool_marker_german_big" in e:
            default_y = -25
            default_z = -1
        elif "tool_marker_ikea_mala" in e:
            default_y = -25
            default_z = -1
        elif "tool_marker_patterned_thicker" in e:
            default_y = -25
            default_z = -1
        elif "jst" in e:
            default_y = -25
            default_z = 1.5
        elif "molex" in e:
            default_y = -25
            default_z = 0      
        elif "tool_tdpb_glue_stick_prit_medium" in e:
            default_y = -25
            default_z = 28/2      
        elif "tool_screwdriver_multi_quikpik_200_mm" in e:
            default_y = -25
            default_z = 36/2 
        elif "tool_screwdriver_driver_bit" in e:
            default_y = -10
            default_z = 8/2
        elif "tool_knife_exacto_17mm_black" in e:
            default_y = -37.5
            default_z = 0      
        #hex keys
        elif "tool_allen_key_hex_" in e:
            default_z = -1
            #do all the diameters a different default_y
            bottom = -25
            if "m1d5" in e:
                default_y = bottom + 48 / 2
            elif "m2d5" in e:
                default_y = bottom + 36 / 2
            elif "m2" in e:
                default_y = bottom + 40 / 2         
            elif "m3" in e:
                default_y = bottom + 24 /2
            elif "m4" in e:
                default_y = bottom + 12 / 2
            elif "m5" in e:
                default_y = bottom
        elif "tool_knife_utility_blade_disposal_can_olfa_dc_3" in e:
            default_y = 27.5
        elif "tool_timer_80_mm_diameter_30_mm_depth_black" in e:
            default_y = 33
            


        th.extend(ob.oobb_easy(t="n", s=f"oobb_{e}", rotX=-90, pos=[cur_x, default_y, default_z], m ="#"))
        cur_x += shift

        ##test for drawing tools
        #th.extend(ob.oobb_easy(t="n", s=f"oobb_{e}", rotX=-90, pos=[0,0,0], m ="#"))
        cur_x += shift

    #add text
    if "wrench" in e:
        text = e.replace("tool_wrench_","tw")
        text = text.replace("_","")
        #th.extend(ob.oobb_easy(t="n", text=text,concate=False,s="oobb_text", pos=[0,0,plate_pos[2]], rotZ=90, m=""))
    elif "wera" in e or "tdpb_drill" in e or "sharpie" in e:
        concate = True        
        if len(e) < 20:
            concate = False
            e = e.replace("tool_","")
        #th.extend(ob.oobb_easy(t="n", text=e,concate=concate,s="oobb_text", pos=[0,3.5,plate_pos[2]+thickness/2-0.3], rotZ=90, size=6, m="#"))
    else:
        pass
        #th.extend(ob.oobb_easy(t="n", text=e,concate=True,s="oobb_text", pos=[0,0,plate_pos[2]+0.3], rotY=180, m="#"))

    ## two faces
    if "jst" in e or two_faces:
        top = copy.deepcopy(th)
        bottom = copy.deepcopy(th)
        bottom = oobb_base.shift(bottom, [width*15+5,0,-thickness/2])
        bottom = oobb_base.inclusion(bottom, "3dpr")

    

        th = bottom + top

        #3dpr silces
        th.extend(ob.oobb_easy(t="n", s="oobb_slice", pos=[0,0, -500 + plate_pos[2]], mode="3dpr", m="")) 
        th.extend(ob.oobb_easy(t="n", s="oobb_slice", pos=[0,0, plate_pos[2]+ thickness/2] , mode="3dpr", m="")) 

        thing["components"] = th    
    

    else:
        #single face
        th.extend(ob.oobb_easy(t="n", s="oobb_slice", pos=[0,0, thickness/2+plate_pos[2]], mode="3dpr", m="")) 
        

    return thing

def get_tray(**kwargs):
    pos = kwargs.get("pos", [0, 0, 0])
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width, 
    height=height, depth=thickness, pos=[0, 0, 0], extra_mm=True, m=""))

    #take out the inside    
    bottom_thickness = 3
    sphere_radius = 4
    p3 = {}
    p3["type"] = "n"
    p3["shape"] = "sphere_rectangle"
    wid = width * 15 - 3
    hei = height * 15 - 3
    dep = thickness + sphere_radius - bottom_thickness
    p3["size"] = [wid,hei,dep]
    pos1 = copy.deepcopy(pos)
    pos1[2] = bottom_thickness
    p3["pos"] = pos1
    p3["r"] = sphere_radius
    p3["m"] = "#"
    th.append(ob.oobb_easy(**p3))
    
    #th.append(ob.oobb_easy(t="n", s=f"sphere_rectangle", size=[(width*15)-3,(height*15)-3,thickness+20], pos=[0, 0, 3], r=4, m=""))


    #add countersunk to four corners
    holes = [[1,1],[width,1],[1,height],[width,height]]
    for h in holes:            
        x,y = ob.get_hole_pos(h[0], h[1], width, height)
        th.extend(ob.oobb_easy(t="n", shape=f"oobb_screw_countersunk", width=width, height=height, clearance = "top", radius_name="m3", depth=6, pos=[x, y, 2], include_nut=False, m=""))


    return thing

def get_tray_lid(**kwargs):

    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width, 
    height=height, depth=1, pos=[0, 0, 0], m=""))

    #inset for connection
    #positive for smaller
    inset = 3 + 0.1
    wid=(width * 15)-inset
    hei=(height*15)- inset
    depth=thickness
    th.append(ob.oobb_easy(t="p", s=f"rounded_rectangle", r=6, size = [wid,hei,depth],  pos=[0, 0, 0], m=""))

    #add pull tab
    x = (width * ob.gv("osp"))/2-0.5
    depth = 1
    th.append(ob.oe(t="p", s="oobb_cylinder", radius=5, depth=depth, pos=[x, 0, depth/2], m=""))

    extra = "3+0.1"
    th.extend(ob.oobb_easy(t="n", text=extra,concate=False,s="oobb_text", size=6, pos=[0,0,0.3], rotY=180, rotZ=90, m=""))

    return thing

def get_tray_lid_thin(**kwargs):

    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    size = kwargs.get("size", "oobb")
    base_pos = kwargs.get("pos", [0,0,0])
    fast = kwargs.get("fast", False)
    rotY = kwargs.get("rotY", 0)

#janky way to be able to draw them either way up
    if rotY == 0:

        wall_thickness = 0.5

        thing = ob.get_default_thing(**kwargs)
        th = thing["components"]

        #lid
        th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width+1/15, 
        height=height+1/15, depth=wall_thickness, pos=base_pos, m=""))

        #inset for connection
        #positive for smaller
        lid_inset = 2
        wid=(width * 15)- lid_inset
        hei=(height*15)- lid_inset
        depth=thickness
        radius = (10 - lid_inset)  / 2
        

        #straight bit
        lip_depth = 2
        size = [wid,hei,lip_depth]
        pos = [base_pos[0], base_pos[1], base_pos[2]-lip_depth]
        th.append(ob.oobb_easy(t="p", s=f"rounded_rectangle_extra", r=radius, inset=0,size = size,  pos=pos, m=""))
        
        #lip
        inset = 2
        #pos = [base_pos[0], base_pos[1], base_pos[2]-lip_depth]
        pos = [base_pos[0], base_pos[1], base_pos[2]-depth]
        size = [wid,hei,depth-lip_depth]
        th.append(ob.oobb_easy(t="p", s=f"rounded_rectangle_extra", r=radius, inset=inset,size = size,  rotY=180, pos=pos, m=""))
        #middle clearance
        pos = [base_pos[0], base_pos[1], base_pos[2]-depth] 
        if not fast:
            th.append(ob.oobb_easy(t="n", s=f"rounded_rectangle", r=radius-inset/2, size = [wid-wall_thickness*2-inset,hei-wall_thickness*2-inset,depth-wall_thickness],  pos=pos, m=""))

        #add pull tab
        #x = (width * ob.gv("osp"))/2-0.5
        #depth = 1
        #th.append(ob.oe(t="p", s="oobb_cylinder", radius=5, depth=depth, pos=[x, 0, depth/2], m=""))

        #extra = "3+0.1"
        #th.extend(ob.oobb_easy(t="n", text=extra,concate=False,s="oobb_text", size=6, pos=[0,0,0.3], rotY=180, rotZ=90, m=""))

        #add countersunk to four corners
        holes = [[1,1],[width,1],[1,height],[width,height]]
        for h in holes:    
                
            x,y = ob.get_hole_pos(h[0], h[1], width, height)
            pos = [x+base_pos[0], y+base_pos[1], base_pos[2]] 
            th.extend(ob.oobb_easy(t="n", s=f"oobb_screw_socket_cap", radius_name="m3", depth=10, pos=pos, rotY=180, include_nut=False, m="#"))

        return thing
    elif rotY ==180:
        
        wall_thickness = 0.5

        thing = ob.get_default_thing(**kwargs)
        th = thing["components"]

        #lid
        th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width+1/15, 
        height=height+1/15, depth=wall_thickness, pos=base_pos, m=""))

        #inset for connection
        #positive for smaller
        lid_inset = 2
        wid=(width * 15)- lid_inset
        hei=(height*15)- lid_inset
        depth=thickness
        radius = (10 - lid_inset)  / 2
        

        #straight bit
        lip_depth = 2
        size = [wid,hei,lip_depth]
        pos = [base_pos[0], base_pos[1], base_pos[2]+wall_thickness]
        th.append(ob.oobb_easy(t="p", s=f"rounded_rectangle_extra", r=radius, inset=0,size = size,  pos=pos, m=""))
        
        #lip
        inset = 2
        #pos = [base_pos[0], base_pos[1], base_pos[2]-lip_depth]
        pos = [base_pos[0], base_pos[1], base_pos[2]+lip_depth]
        size = [wid,hei,depth-lip_depth]
        th.append(ob.oobb_easy(t="p", s=f"rounded_rectangle_extra", r=radius, inset=inset,size = size,  rotY=0, pos=pos, m=""))
        #middle clearance
        pos = [base_pos[0], base_pos[1], base_pos[2]+wall_thickness] 
        if not fast:
            th.append(ob.oobb_easy(t="n", s=f"rounded_rectangle", r=radius-inset/2, size = [wid-wall_thickness*2-inset,hei-wall_thickness*2-inset,depth-wall_thickness],  pos=pos, m=""))

        #add pull tab
        #x = (width * ob.gv("osp"))/2-0.5
        #depth = 1
        #th.append(ob.oe(t="p", s="oobb_cylinder", radius=5, depth=depth, pos=[x, 0, depth/2], m=""))

        #extra = "3+0.1"
        #th.extend(ob.oobb_easy(t="n", text=extra,concate=False,s="oobb_text", size=6, pos=[0,0,0.3], rotY=180, rotZ=90, m=""))

        #add countersunk to four corners
        holes = [[1,1],[width,1],[1,height],[width,height]]
        for h in holes:    
                
            x,y = ob.get_hole_pos(h[0], h[1], width, height)
            pos = [x+base_pos[0], y+base_pos[1], base_pos[2]+wall_thickness] 
            th.extend(ob.oobb_easy(t="n", s=f"oobb_screw_socket_cap", radius_name="m3", depth=10, pos=pos, include_nut=False, m=""))

        return thing

def get_tray_lid_thin_spin(**kwargs):

    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    size = kwargs.get("size", "oobb")
    base_pos = kwargs.get("pos", [0,0,0])
    fast = kwargs.get("fast", False)
    rotY = kwargs.get("rotY", 0)

#janky way to be able to draw them either way up
    if rotY == 0:

        wall_thickness = 2

        thing = ob.get_default_thing(**kwargs)
        th = thing["components"]

        #lid
        pos = [base_pos[0], base_pos[1], base_pos[2]+wall_thickness]
        th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width+1/15, 
        height=height+1/15, depth=wall_thickness, pos=pos, m=""))

        #inset for connection
        #positive for smaller
        lid_inset = 2
        #wid=(width * 15)- lid_inset
        #hei=(height*15)- lid_inset
        wid=(1 * 15)- lid_inset
        hei=(1*15)- lid_inset
        x_sh, y_sh = ob.get_hole_pos(1, 1, width, height)
        x_sh += (width - 1) * 15 
        y_sh += (height - 1) * 15
        pos_lip = [base_pos[0]+x_sh, base_pos[1]+y_sh, base_pos[2]+ wall_thickness]
        depth=thickness
        radius = (10 - lid_inset)  / 2
        

        #straight bit
        lip_depth = 2
        size = [wid,hei,lip_depth]
        pos = [pos_lip[0], pos_lip[1], pos_lip[2]-lip_depth]
        th.append(ob.oobb_easy(t="p", s=f"rounded_rectangle_extra", r=radius, inset=0,size = size,  pos=pos, m=""))
        
        #lip
        inset = 2
        #pos = [base_pos[0], base_pos[1], base_pos[2]-lip_depth]
        pos = [pos_lip[0], pos_lip[1], pos_lip[2]-depth]
        size = [wid,hei,depth-lip_depth]
        th.append(ob.oobb_easy(t="p", s=f"rounded_rectangle_extra", r=radius, inset=inset,size = size,  rotY=180, pos=pos, m=""))
        #middle clearance
        pos = [pos_lip[0], pos_lip[1], pos_lip[2]-depth] 
        if not fast:
            th.append(ob.oobb_easy(t="n", s=f"rounded_rectangle", r=radius-inset/2, size = [wid-wall_thickness*2-inset,hei-wall_thickness*2-inset,depth-wall_thickness],  pos=pos, m=""))

        #add pull tab
        #x = (width * ob.gv("osp"))/2-0.5
        #depth = 1
        #th.append(ob.oe(t="p", s="oobb_cylinder", radius=5, depth=depth, pos=[x, 0, depth/2], m=""))

        #extra = "3+0.1"
        #th.extend(ob.oobb_easy(t="n", text=extra,concate=False,s="oobb_text", size=6, pos=[0,0,0.3], rotY=180, rotZ=90, m=""))

        #add countersunk to four corners
        holes = [[1,1],[width,1],[1,height],[width,height]]
        for h in holes:    
                
            x,y = ob.get_hole_pos(h[0], h[1], width, height)
            pos = [x+base_pos[0], y+base_pos[1], base_pos[2]-50] 
            th.extend(ob.oobb_easy(t="n", s=f"oobb_hole", radius_name="m3", depth=100, pos=pos, m=""))

        #captive_nut
    holes = [[1,1]]
    for h in holes:
        #add 1x1 rounded rectangle 3mm deep
        
        x,y = ob.get_hole_pos(h[0], h[1], width, height)
        
        
        
        r = 5
        depth = 4        
        shift = 0
        x_shift = shift
        y_shift = shift
        pos = [x + x_shift + base_pos[0], y + y_shift + base_pos[1], base_pos[2] - depth/2 + wall_thickness]
        #add corner support
        
        th.append(ob.oobb_easy(t="p", s=f"oobb_cylinder", radius=r, depth=depth, pos=pos, m=""))
        #add nut
        pos = [x + base_pos[0], y + base_pos[1], base_pos[2]+wall_thickness*2]
        th.append(ob.oobb_easy(t="n", s=f"oobb_nut", radius_name="m3", zz="top", pos=pos, m="#"))


        return thing

def get_tray_thin(**kwargs):

    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    size = kwargs.get("size", "oobb")
    fast = kwargs.get("fast", False)

    base_pos = kwargs.get("pos", [0,0,0])

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width+1/15, 
    height=height+1/15, depth=thickness, pos=base_pos, m=""))

    #take out the inside    
    wall_thickness = 1
    radius = 9.5/2
    pos = [base_pos[0], base_pos[1], base_pos[2]+wall_thickness]
    if not fast:
        th.append(ob.oobb_easy(t="n", s=f"sphere_rectangle", size=[(width*15)-wall_thickness,(height*15)-wall_thickness,thickness+20], pos=pos, r=radius, m=""))


    #add countersunk to four corners
    holes = [[1,1],[width,1],[1,height],[width,height]]
    for h in holes:          
        x,y = ob.get_hole_pos(h[0], h[1], width, height)        
        pos = [x + base_pos[0], y + base_pos[1], base_pos[2]+wall_thickness]  
        th.extend(ob.oobb_easy(t="n", s=f"oobb_screw_socket_cap", radius_name="m3", depth=10, pos=pos, include_nut=False, m="", overhang = False))


    return thing

def get_tray_thin_spin(**kwargs):

    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    size = kwargs.get("size", "oobb")
    fast = kwargs.get("fast", False)

    base_pos = kwargs.get("pos", [0,0,0])

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]


    #take out the inside    
    wall_thickness = 1
    radius = 9.5/2
    pos = [base_pos[0], base_pos[1], base_pos[2]+wall_thickness]
    
    th.append(ob.oobb_easy(t="p", s=f"tray", width=width*15, 
    height=height*15, depth=thickness, wall_thickness=wall_thickness, pos=base_pos, m=""))

    

    #add hole to four corners
    holes = [[1,1],[width,1],[1,height],[width,height]]
    for h in holes:          
        x,y = ob.get_hole_pos(h[0], h[1], width, height)        
        pos = [x + base_pos[0], y + base_pos[1], base_pos[2]-50]  
        th.append(ob.oobb_easy(t="n", s=f"oobb_hole", radius_name="m3", depth=100, pos=pos,  m=""))
    #add tubes to bl and tr
    holes = [[1,1],[width,height]]
    for h in holes:
        x,y = ob.get_hole_pos(h[0], h[1], width, height)        
        pos = [x + base_pos[0], y + base_pos[1], base_pos[2]]  
        th.append(ob.oobb_easy(t="p", wall_thickness=1,s=f"oobb_tube", radius_name="m3", depth=thickness-4, pos=pos, m=""))
    #add countersunk to bl
    holes = [[1,1], [width,height]]
    for h in holes:
        #add 1x1 rounded rectangle 3mm deep
        
        x,y = ob.get_hole_pos(h[0], h[1], width, height)
        
        wid = 13
        hei = wid
        depth = 3
        if h[0] == 1:
            depth = thickness - 4
        size = [wid, hei, depth]
        shift = -1
        x_shift = shift
        y_shift = shift
        if h[0] == 1:
            pos = [x + x_shift + base_pos[0], y + y_shift + base_pos[1], base_pos[2]]
        else:
            pos = [x - x_shift + base_pos[0], y - y_shift + base_pos[1], base_pos[2]]
        #add corner support
        th.append(ob.oobb_easy(t="p", s=f"rounded_rectangle", size=size,pos=pos, m=""))
        #add countersunk
        pos = [x + base_pos[0], y + base_pos[1], base_pos[2]+thickness]
        th.append(ob.oobb_easy(t="n", s=f"oobb_screw_countersunk", radius_name="m3", depth=thickness, rotY=180, pos=pos, include_nut=False, m=""))


    return thing

def get_trt_old(**kwargs):

    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    th = thing["components"]

    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width, 
    height=height, depth=thickness, pos=[0, 0, 0], m=""))

    #take out the inside    
    wall_thickness = 1
    radius = 9.5/2
    th.append(ob.oobb_easy(t="n", s=f"sphere_rectangle", size=[(width*15)-1-wall_thickness,(height*15)-1-wall_thickness,thickness+20], pos=[0, 0, wall_thickness], r=radius, m=""))


    #add countersunk to four corners
    holes = [[1,1],[width,1],[1,height],[width,height]]
    for h in holes:            
        x,y = ob.get_hole_pos(h[0], h[1], width, height)
        th.extend(ob.oobb_easy(t="n", s=f"oobb_screw_socket_cap", radius_name="m3", depth=10, pos=[x, y, wall_thickness], include_nut=False, m=""))


    return thing

def get_tray_vertical(**kwargs):
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    holes = kwargs.get("holes", False)
    both_holes = kwargs.get("both_holes", False)
    extra = kwargs.get("extra", "")
    size = kwargs.get("size", "oobb")

    thing = ob.get_default_thing(**kwargs)
    thing["components"] = get_tray(**kwargs)["components"]
    th = thing["components"]
    
    thick = 3
    x=-width*15/2+thick
    y=0
    z=thickness
    
    wid = 2 * 15
    hei = height * 15
    rotY=90
    th.append(opsc.opsc_easy(type="p", shape="rounded_rectangle", size = [wid,hei,thick],  pos=[x, y, z], rotY=rotY, m=""))
    ### add holes
    for xx in range(0, int(height)):
        x = -width * 15 / 2 - 15
        y = -(height/2*15) + 7.5 + xx * 15
        z = 7.5 + thickness
        rotY=90
        th.extend(ob.oe(type="n", shape="oobb_hole", radius_name="m6",  pos=[x, y, z], rotY=rotY, depth = 20, m="#"))


    """
    th.append(ob.oobb_easy(t="p", s=f"{size}_plate", width=width, 
    height=height, depth=thickness, pos=[0, 0, 0], m=""))

    #take out the inside    
    th.append(ob.oobb_easy(t="n", s=f"sphere_rectangle", size=[(width*15)-3,(height*15)-3,thickness+20], pos=[0, 0, 3], r=6, m=""))


    #add countersunk to four corners
    holes = [[1,1],[width,1],[1,height],[width,height]]
    for h in holes:            
        x,y = ob.get_hole_pos(h[0], h[1], width, height)
        th.extend(ob.oobb_easy(t="n", s=f"oobb_screw_countersunk", top_clearance=True, width=width, height=height, radius_name="m3", depth=6, pos=[x, y, 3], include_nut=False, m=""))
    """

    return thing

def get_wheel_old_1(**kwargs):
    oring_type = kwargs.get("oring_type", "327")
    #figuring out radius
    od = ob.gv(f"oring_{oring_type}_od", "true")
    id = ob.gv(f"oring_{oring_type}_id", "true")
    idt = ob.gv(f"oring_{oring_type}_id_tight", "true")
    minus_bit = 1.5
    radius = idt + (od-id)/2 + 0.5 - minus_bit #(to account for the minusing) 
    diameter_big = radius*2/ob.gv("osp")
    diameter = int(round(diameter_big, 0))
    #if diameter is even take one off to make it odd
    if diameter % 2 == 0:
        diameter -= 1

    kwargs.update({"diameter": diameter})
    thing = ob.get_default_thing(**kwargs)
    
    # solid piece
    th = thing["components"]
    #kwargs.update({"exclude_d3_holes": True})
    #kwargs.update({"exclude_center_holes": True})
    
    kwargs.update({"diameter": diameter_big})
    th.extend(get_circle(**kwargs)["components"])

    th.extend(ob.oe(t="n", s="oobb_oring", oring_type=oring_type, m="#"))

    return thing

def get_wire_old(**kwargs):
    extra = kwargs.get("extra")
    kwargs.pop("extra")
    kwargs["type"] = f'wire_{extra}'
    
    clearance = kwargs.get("clearance", False)

    if extra != "":
        osp = ob.gv("osp")
        thing = ob.get_default_thing(**kwargs)
        
        width = kwargs.get("width", 2)
        height = kwargs.get("height", 2)
        thickness = kwargs.get("thickness", 3)
        
        

        pos = kwargs.get("pos", [0, 0, 0])
        shift = width/2 * osp
        base_pos = copy.deepcopy(pos)
        plate_pos = kwargs.get("pos", [pos[0]+shift, pos[1], 0])
        wi_pos =  [plate_pos[0]-22.5, plate_pos[1], plate_pos[2]]
        

        type = kwargs.get("type", "")        
        extra_code = f'{type}'.replace("_base", "")
        

        # solid piece
        th = thing["components"]

        th.extend(ob.oe(t="p", s="oobb_pl", holes="none", width=width, height=height,depth=thickness, pos=plate_pos, mode="all"))

        #oobb holes
        if width == 3 and height == 3:
            th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, pos=plate_pos, holes=["corners"], radius_name="m6", m=""))
            th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=(width*2)-1, height=(height*2)-1, pos=plate_pos, holes=["left","right","bottom"], radius_name="m3", size="oobe", m=""))

            th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, pos=plate_pos, holes="single", loc = [[3,2]],radius_name="m6", m=""))   
            # add the side ones to3d printed ones
            th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, pos=plate_pos, holes="single", loc = [[2,1],[2,3]],radius_name="m6", m="", inclusion = ["true","3dpr"]))            
            poss = []
            poss.append([plate_pos[0],base_pos[1]+15,base_pos[2]])
            poss.append([plate_pos[0],base_pos[1]-15,base_pos[2]])
            
            for pos in poss:
                #main joining countersunk or standoffs
                if "_base" in extra:
                    thi = 4.5
                    posa = [pos[0], pos[1], pos[2]+thickness-thi]
                    #posa = [pos[0], pos[1], pos[2]+thickness-thi+20]
                    th.extend(ob.oobb_easy(t="n", s="oobb_standoff", width=width, height=height, pos=posa, holes="single", inclusion="laser", radius_name = "m3", extra="support_bottom", depth=thi, m=""))
                elif "base" in extra:                    
                    posa = [pos[0], pos[1], pos[2]+thickness]
                    th.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", width=width, height=height, pos=posa, holes="single", radius_name = "m3", include_nut=False, depth=thickness, m=""))
                    
                else:
                    posa = [pos[0], pos[1], pos[2]]
                    th.extend(ob.oobb_easy(t="n", s="oobb_standoff", width=width, height=height, pos=posa, holes="single", inclusion="laser", depth=thickness, radius_name = "m3", m=""))

        else:
            th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, pos=plate_pos, holes=["left","right"], radius_name="m6", size="oobb",m=""))
            th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=(width*2)-1, height=(height*2)-1, pos=plate_pos, holes=["left","right"], radius_name="m3", size="oobe", m=""))
            if width > 2:
                for w in range(3, width+1):
                    th.extend(ob.oobb_easy(t="n", s="oobb_holes", width=width, height=height, pos=plate_pos, holes="single", loc = [w,2],radius_name="m6", m=""))                    

        #joining screws in the middle
        #m3 hole extras
        holes = []
        x = 15
        y = 7.5
        con_string = "oobb_nut"
        con_z = 3
        #if "base" in extra and "_base" not in extra:
        if "base" in extra:
            con_string = "oobb_screw_countersunk"
            con_z = thickness
        holes.extend([[x,y,0,"m3","oobb_hole"],
                    [x,-y,0,"m3","oobb_hole"],
                    [x,y,con_z,"m3",con_string],
                    [x,-y,con_z,"m3",con_string]])
        pos = kwargs.get("pos", [0, 0, 0])
        for hole in holes:
            loc = hole
            posa = [pos[0] + loc[0], pos[1] + loc[1], pos[2] + loc[2]]
            th.extend(ob.oobb_easy(t="n", s=hole[4], width=width, loc=loc,
                    height=height, include_nut=False, radius_name=hole[3], pos=posa, m=""))                             

        #add screw holes for holder piece
        if "holder" in extra:
            holes = []
            start_x = 7.5
            start_y = -7.5
            #do a grid 3 x 3 of holes add an array of cordinates to skip
            skip = []
            skip.append([1,0])
            skip.append([1,2])
            skip.append([3,1])

            wid = 4
            hei = 3
            for x in range(wid):
                for y in range(hei):
                    if [x,y] not in skip:
                        holes.append([start_x+x*7.5,start_y+y*7.5])
            for hole in holes:
                #moze z down 3
                posa = [pos[0] + hole[0], pos[1] + hole[1], pos[2] + 3]
                th.extend(ob.oobb_easy(t="n", s="oobb_screw_countersunk", width=width, height=height, pos=posa, holes="single", radius_name = "m3", rotY=180, include_nut=False, depth=thickness, m=""))
        
        #add a cube for wire clearnce using pos and size arrays
        if "holder" in extra or "cap" in extra or clearance:
            p3 = copy.deepcopy(kwargs)
            p3["s"] = "oobb_wire_clearance_square"
            p3["depth"] = thickness
            #p3["m"] = "#"
            th.append(get_common(**p3))

        #wire piece
        if "base" not in extra and "cap" not in extra or "_" in extra and "base_cap" not in extra:
            through = True
            if "_base" in extra:
                through = False
            th.extend(ob.oe(t="n", s=f"oobb_{extra_code}", holes="none", pos=wi_pos, mode="all", width=width, height=height, through = through, m=""))
        else:
            pass
        
        
        return thing

def get_ziptie_holder_jack(**kwargs):
    thickness = 12
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thing = ob.get_default_thing(**kwargs)

    # solid piece
    th = thing["components"]

    height_cube = 13.5
    y_plate = height_cube + (height-1)*ob.gv("osp") / 2

    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width, height=height,
              depth=thickness, pos=[0, y_plate, -thickness/2], mode="all"))

    width_cube = ob.gv("osp")*width-ob.gv("osp_minus")

    th.append(ob.oobb_easy(t="p", s="cube", size=[
              width_cube, height_cube, thickness], pos=[-width_cube/2, 0, -thickness/2], mode="all"))

    # bolt holes
    mode = "all"
    for x in range(0, width):
        x = (-width/2*ob.gv("osp")+ob.gv("osp")/2)+x*ob.gv("osp")
        y = height_cube
        z = 0
        for hei in range(0, height):
            pos_zt = [x, height_cube+1.5+ob.gv("osp")*hei, 0]
            th.extend(ob.oobb_easy(t="n", s="oobb_ziptie",
                      pos=pos_zt, mode=mode, m=""))

        x2 = x
        y2 = 8
        z2 = z
        th.extend(ob.oobb_easy(t="n", s="oobb_hole", radius_name="m6",
                  depth=y2, pos=[x2, y2, z2], rotX=90, mode=mode, m=""))

        # nut height
        y = 9
        th.extend(ob.oobb_easy(t="n", s="oobb_nut_through", radius_name="m6",
                  depth=height_cube, pos=[x, y, z], rotX=90, mode=mode, m=""))

    return thing

def get_ziptie_holder(**kwargs):
    thickness = 6
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thing = ob.get_default_thing(**kwargs)

    # solid piece
    th = thing["components"]

    height_cube = 13.5

    th.extend(ob.oe(t="p", s="oobb_pl", holes=False, width=width,
              height=height, depth=thickness, pos=[0, 0, -thickness/2], m=""))
    th.extend(ob.oe(t="n", s="oobb_holes", holes="right",
              width=width, height=height, m=""))
    th.extend(ob.oe(t="n", s="oobb_holes", holes="left",
              width=width, height=height, m=""))

    width_cube = ob.gv("osp")*width-ob.gv("osp_minus")

    # bolt holes
    mode = "all"
    for hei in range(2, height):
        for wid in range(1, width+1):
            x, y = ob.get_hole_pos(wid, hei, width, height)
            th.extend(ob.oobb_easy(t="n", s="oobb_ziptie",
                      clearance=True, pos=[x, y, 0], mode=mode, m=""))

    return thing
