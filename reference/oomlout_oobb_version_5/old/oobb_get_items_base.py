import copy

from oobb_get_items_base_old import *
from solid2 import *

# circle
def get_oobb_circle(**kwargs):
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    extra_mm = kwargs.get("extra_mm", False)
    pos = kwargs.get("pos", [0, 0, 0])
    depth = kwargs.get("depth", 3)
    zz = kwargs.get("zz", "bottom")

    
    #add extra_mm
    if extra_mm:
        width = width + 1/15 
        height = height + 1/15
    
    #zz 
    if zz == "bottom":
        pos[2] += 0
    elif zz == "top":
        pos[2] += -depth
    elif zz == "middle":
        pos[2] += -depth/2

    width_mm = width * oobb.gv("osp") - oobb.gv("osp_minus")
    height_mm = height * oobb.gv("osp") - oobb.gv("osp_minus")
    


       
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "cylinder"
    p3["r"] = (width * oobb.gv("osp") - oobb.gv("osp_minus"))/2
    p3["h"] = depth
    return [opsc.opsc_easy(**p3)]

# coupler
#      coupler_flanged
def get_oobb_coupler_flanged(**kwargs):
    typ = kwargs.get("type", "p")
    kwargs["type"] = "p" #setting it to positive because it's a rotation object
    

    rot = get_rot(**kwargs)   
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
        pass
    elif part == "shaft":
        
        pos = copy.deepcopy(pos)
        
        p3 = copy.deepcopy(kwargs)        
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = "m3"
        poss = []
        shift = 5.657
        pos1 = copy.deepcopy(pos)
        pos1[0] += shift
        pos1[1] += shift
        pos2 = copy.deepcopy(pos)
        pos2[0] += -shift
        pos2[1] += -shift
        pos3 = copy.deepcopy(pos)
        pos3[0] += shift
        pos3[1] += -shift
        pos4 = copy.deepcopy(pos)
        pos4[0] += -shift
        pos4[1] += shift        
        poss.append(pos1)
        poss.append(pos2)
        poss.append(pos3)
        poss.append(pos4)
        p3["pos"] = poss
        #p3["m"] = "#"
        return_value.extend(oobb.oobb_easy(**p3))

        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = "m8"
        return_value.extend(oobb.oobb_easy(**p3))

        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]

        return return_value_2

# cube
def get_oobb_cube(**kwargs):
    return get_oobb_cube_center(**kwargs)

def get_oobb_cube_center(**kwargs):


    p3 = copy.deepcopy(kwargs)
    zz = kwargs.get("zz", "bottom")
    
    p3["shape"] = "cube"
    pos1 = copy.deepcopy(p3["pos"])
    pos1[0] = pos1[0] - p3["size"][0]/2
    pos1[1] = pos1[1] - p3["size"][1]/2
    if zz == "center" or zz == "middle":
        pos1[2] = pos1[2] - p3["size"][2]/2
    elif zz == "top":
        pos1[2] = pos1[2] - p3["size"][2]
    elif zz == "bottom":
        pos1[2] = pos1[2]

    p3["pos"] = pos1
    return oobb.oobb_easy(**p3)

# hole
def get_oobb_cube_new(**kwargs):
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    depth = kwargs.get("depth", 100)
    zz = kwargs.get("zz", "bottom")
    radius_name = kwargs.get("radius_name", "")
    radius = kwargs.get("radius", 0)

    # setting up for rotation object
    typ = kwargs.get("type", "p")
    kwargs["type"] = "positive" #needs to be positive for the difference to work
    rot_original = get_rot(**kwargs)       
    kwargs.pop("rot", None)
    kwargs.pop("rot_x", None)
    kwargs.pop("rot_y", None)
    kwargs.pop("rot_z", None)
    rot_shift_original = copy.deepcopy(kwargs.get("rot_shift", None))
    kwargs.pop("rot_shift", None)

    # storing pos and popping it out to add it in rotation element     
    pos_original = copy.deepcopy(copy.deepcopy(kwargs.get("pos", [0, 0, 0])))
    pos_original_original = copy.deepcopy(pos_original)
    kwargs.pop("pos", None)
    pos = [0,0,0]
    kwargs["pos"] = pos


    return_value = []
    p3 = copy.deepcopy(kwargs)
    zz = kwargs.get("zz", "bottom")
    
    p3["shape"] = "cube"
    pos1 = copy.deepcopy(p3["pos"])
    pos1[0] = pos1[0] - p3["size"][0]/2
    pos1[1] = pos1[1] - p3["size"][1]/2
    if zz == "center" or zz == "middle":
        pos1[2] = pos1[2] - p3["size"][2]/2
    elif zz == "top":
        pos1[2] = pos1[2] - p3["size"][2]
    elif zz == "bottom":
        pos1[2] = pos1[2]

    p3["pos"] = pos1
    return_value.append(opsc.opsc_easy(**p3))

    
    #components_second = copy.deepcopy(thing["components"])

    #put into a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    pos1 = copy.deepcopy(pos)
    #pos1[0] += 50
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    if rot_shift_original != None:
        return_value_2["rot_shift"] = rot_shift_original
    return_value_2 = [return_value_2]


    return return_value_2


def get_oobb_cylinder_hollow(**kwargs):
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

    return_value = []

    wall_thickness = kwargs.get("wall_thickness", 2)

    depth = kwargs.get("depth", None)
    if depth != None:
        kwargs["h"] = depth
    
    if "radius" in kwargs:
        kwargs["r"] = kwargs["radius"]
        kwargs.pop("radius", None)

    #positive_cylinder
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "cylinder"
    p3["type"] = "positive"
    return_value.append(opsc.opsc_easy(**p3))

    #negative_cylinder
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "cylinder"
    p3["type"] = "negative"
    if "r1" in p3:
        p3["r1"] = p3["r1"] - wall_thickness
        p3["r2"] = p3["r2"] - wall_thickness
    else:
        p3["r"] = p3["r"] - wall_thickness
    return_value.append(opsc.opsc_easy(**p3))

    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]

    return return_value_2

def get_oobb_rounded_rectangle_hollow(**kwargs):
    extra = kwargs.get("extra", "")
    wall_thickness = kwargs.get("wall_thickness", 2)
    if extra == "interior":
        return_value = []
        #negative_cylinder
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "rounded_rectangle"
        if "size" in p3:
            size1 = copy.deepcopy(p3["size"])
            size1[0] = size1[0] - wall_thickness * 2
            size1[1] = size1[1] - wall_thickness * 2
            p3["size"] = size1
        else:
            p3["width"] += - wall_thickness * 2
            p3["height"] += - wall_thickness * 2
        if "radius" in p3:
            rad = p3.get("radius")
            rad = rad - wall_thickness
            p3["radius"] = rad
        elif "r1" in p3:
            rad1 = p3.get("r1")
            rad1 += - wall_thickness
            p3["r1"] = rad1
            rad2 = p3.get("r2")
            rad2 += - wall_thickness
            p3["r2"] = rad2
            p3.pop("r", None)
        else:
            rad = 5
        return_value.append(opsc.opsc_easy(**p3))
        return return_value
    else:

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

        return_value = []

        

        #positive_rounded_rectangle
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "rounded_rectangle"
        p3["type"] = "positive"
        return_value.append(opsc.opsc_easy(**p3))

        #negative_cylinder
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "rounded_rectangle"
        p3["type"] = "negative"
        if "size" in p3:
            size1 = copy.deepcopy(p3["size"])
            size1[0] = size1[0] - wall_thickness * 2
            size1[1] = size1[1] - wall_thickness * 2
            p3["size"] = size1
        else:
            p3["width"] += - wall_thickness * 2
            p3["height"] += - wall_thickness * 2
        if "radius" in p3:
            rad = p3.get("radius")
            rad = rad - wall_thickness
            p3["radius"] = rad
        elif "r1" in p3:
            rad1 = p3.get("r1")
            rad1 += - wall_thickness
            p3["r1"] = rad1
            rad2 = p3.get("r2")
            rad2 += - wall_thickness
            p3["r2"] = rad2
            p3.pop("r", None)
        else:
            rad = 5
        
        #pos = copy.deepcopy(p3.get("pos", [0, 0, 0]))
        #pos[2] += 50
        #p3["pos"] = pos

        
        #p3["m"] = "#"
        return_value.append(opsc.opsc_easy(**p3))

        # packaging as a rotation object
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot_original
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]

        return return_value_2        

def get_oobb_rounded_rectangle_rounded(**kwargs):
    extra = kwargs.get("extra", "")
    pos = kwargs.get("pos", [0, 0, 0])
    #rot = kwargs.get("rot",[0,0,0])
    rot = [0,0,0]
    radius = kwargs.get("radius", 5)
    radius_rounded = kwargs.get("radius_rounded", 2.5)
    size = kwargs.get("size", [20, 10, 5])
    wid = size[0]
    hei = size[1]
    dep = size[2]
    if True:

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

        return_value = []

        
        #main_piece
        if True:
            size_main = copy.deepcopy(size)
            size_main[2] = size_main[2] - radius_rounded * 2

            #positive_rounded_rectangle
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "rounded_rectangle"
            p3["type"] = "positive"
            p3["size"] = size_main
            pos1 = copy.deepcopy(pos)
            pos1[2] += radius_rounded
            p3["pos"] = pos1
            return_value.append(opsc.opsc_easy(**p3))
        #top and bottom piece and rounding
        shift_z_1 = 0
        shift_z_2 = dep - radius_rounded
        if True:
            shift_z = dep/2 - radius_rounded/2
            dep_2 = radius_rounded
            wid_little = wid - radius_rounded * 2
            hei_little = hei - radius_rounded * 2
            dep_little = radius_rounded
            size_little = [wid_little, hei_little, dep_little]
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "rounded_rectangle"
            p3["type"] = "positive"
            p3["size"] = size_little
            p3["radius"] = radius - radius_rounded
            poss = []
            pos1 = copy.deepcopy(pos)
            pos11 = copy.deepcopy(pos1)
            pos11[2] += shift_z_1
            poss.append(pos11)
            pos12 = copy.deepcopy(pos1)
            pos12[2] = shift_z_2
            poss.append(pos12)
            p4 = copy.deepcopy(p3)
            p4["pos"] = pos11
            return_value.append(opsc.opsc_easy(**p4))
            p5 = copy.deepcopy(p3)
            p5["pos"] = pos12
            return_value.append(opsc.opsc_easy(**p5))
            #cylinders
            shift_x_cyl = wid/2 - radius_rounded
            dep_cyl = hei - radius*2
            dep_cyl_short = wid - radius*2
            shift_y_cyl = dep_cyl/2
            shift_z_cyl = dep_cyl/2 + radius_rounded
            shift_x_cyl_short = -dep_cyl_short/2# - radius
            shift_y_cyl_short = hei/2 - radius_rounded
            shift_z_cyl_short = dep_cyl_short/2 + radius_rounded
            if True:
                #cylinder long                
                rad_cyl = radius_rounded
                p3 = copy.deepcopy(kwargs)
                p3["shape"] = "oobb_cylinder"
                p3["type"] = "positive"
                p3["depth"] = dep_cyl
                p3["radius"] = rad_cyl
                pos1 = copy.deepcopy(pos)
                pos1[0] += shift_x_cyl
                pos1[1] += shift_y_cyl
                pos1[2] += shift_z_cyl
                pos11 = copy.deepcopy(pos1)
                p3["pos"] = pos11
                #p3["m"] = "#"
                rot1 = copy.deepcopy(rot)
                rot1[0] += 90
                p3["rot"] = rot1
                p3.pop("size", None)
                return_value.append(oobb.oobb_easy(**p3))
                p4 = copy.deepcopy(p3)
                pos12 = copy.deepcopy(pos1)
                pos12[0] += -(wid - radius_rounded*2)
                p4["pos"] = pos12
                return_value.append(oobb.oobb_easy(**p4))
                p5 = copy.deepcopy(p3)
                pos13 = copy.deepcopy(pos1)
                pos13[2] += dep - radius_rounded*2
                p5["pos"] = pos13
                return_value.append(oobb.oobb_easy(**p5))
                p6 = copy.deepcopy(p3)
                pos14 = copy.deepcopy(pos1)
                pos14[0] += -(wid - radius_rounded*2)
                pos14[2] += dep - radius_rounded*2
                p6["pos"] = pos14
                return_value.append(oobb.oobb_easy(**p6))
                #cylinder_short
                rad_cyl = radius_rounded
                p3 = copy.deepcopy(kwargs)
                p3["shape"] = "oobb_cylinder"
                p3["type"] = "positive"
                p3["depth"] = dep_cyl_short
                p3["radius"] = rad_cyl
                pos1 = copy.deepcopy(pos)
                pos1[0] += shift_x_cyl_short
                pos1[1] += shift_y_cyl_short
                pos1[2] += shift_z_cyl_short
                pos11 = copy.deepcopy(pos1)
                p3["pos"] = pos11
                #p3["m"] = "#"
                rot1 = copy.deepcopy(rot)
                rot1[1] += 90
                p3["rot"] = rot1
                p3.pop("size", None)
                return_value.append(oobb.oobb_easy(**p3))
                p4 = copy.deepcopy(p3)
                pos12 = copy.deepcopy(pos1)
                pos12[1] += -(hei - radius_rounded*2)
                p4["pos"] = pos12
                return_value.append(oobb.oobb_easy(**p4))
                p5 = copy.deepcopy(p3)
                pos13 = copy.deepcopy(pos1)
                pos13[2] += dep - radius_rounded*2
                p5["pos"] = pos13
                return_value.append(oobb.oobb_easy(**p5))
                p6 = copy.deepcopy(p3)
                pos14 = copy.deepcopy(pos1)
                pos14[1] += -(hei - radius_rounded*2)
                pos14[2] += dep - radius_rounded*2
                p6["pos"] = pos14
                return_value.append(oobb.oobb_easy(**p6))
                #corner_spheres
                if True:
                    p3 = copy.deepcopy(kwargs)
                    p3["shape"] = "oring"
                    p3["depth"] = radius_rounded * 2
                    p3["id"] = radius - radius_rounded*2
                    pos1 = copy.deepcopy(pos)
                    pos1[2] += radius_rounded
                    pos11 = copy.deepcopy(pos1)
                    pos11[0] += -wid/2 + radius
                    pos11[1] += -hei/2 + radius
                    pos11[2] += 0
                    p3["pos"] = pos11
                    p3.pop("size", None)
                    #p3["m"] = "#"   
                    return_value.append(oobb.oobb_easy(**p3))
                    p4 = copy.deepcopy(p3)
                    pos12 = copy.deepcopy(pos1)
                    pos12[0] += wid/2 - radius
                    pos12[1] += -hei/2 + radius
                    p4["pos"] = pos12
                    return_value.append(oobb.oobb_easy(**p4))
                    p5 = copy.deepcopy(p3)
                    pos13 = copy.deepcopy(pos1)
                    pos13[0] += wid/2 - radius
                    pos13[1] += hei/2 - radius
                    p5["pos"] = pos13
                    return_value.append(oobb.oobb_easy(**p5))
                    p6 = copy.deepcopy(p3)
                    pos14 = copy.deepcopy(pos1)
                    pos14[0] += -wid/2 + radius
                    pos14[1] += hei/2 - radius
                    p6["pos"] = pos14
                    return_value.append(oobb.oobb_easy(**p6))
                    p7 = copy.deepcopy(p3)
                    pos15 = copy.deepcopy(pos1)
                    pos15[0] += -wid/2 + radius
                    pos15[1] += -hei/2 + radius
                    pos15[2] += dep - radius_rounded*2
                    p7["pos"] = pos15
                    return_value.append(oobb.oobb_easy(**p7))
                    p8 = copy.deepcopy(p3)
                    pos16 = copy.deepcopy(pos1)
                    pos16[0] += wid/2 - radius
                    pos16[1] += -hei/2 + radius
                    pos16[2] += dep - radius_rounded*2
                    p8["pos"] = pos16
                    return_value.append(oobb.oobb_easy(**p8))
                    p9 = copy.deepcopy(p3)
                    pos17 = copy.deepcopy(pos1)
                    pos17[0] += wid/2 - radius
                    pos17[1] += hei/2 - radius
                    pos17[2] += dep - radius_rounded*2
                    p9["pos"] = pos17
                    return_value.append(oobb.oobb_easy(**p9))
                    p10 = copy.deepcopy(p3)
                    pos18 = copy.deepcopy(pos1)
                    pos18[0] += -wid/2 + radius
                    pos18[1] += hei/2 - radius
                    pos18[2] += dep - radius_rounded*2
                    p10["pos"] = pos18
                    return_value.append(oobb.oobb_easy(**p10))

        
        
        #pos = copy.deepcopy(p3.get("pos", [0, 0, 0]))
        #pos[2] += 50
        #p3["pos"] = pos

        
        #p3["m"] = "#"
        return_value.append(opsc.opsc_easy(**p3))

        # packaging as a rotation object
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot_original
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]

        return return_value_2     


#sphere with squash ability
def get_oobb_sphere(**kwargs):
    radius_1 = kwargs.get("radius_1", None)
    if radius_1 != None:
        radius = radius_1
    else:
        radius = kwargs.get("radius", 10)    
    radius_2 = kwargs.get("radius_2", None)
    if radius_2 == None:
        radius_2 = radius    
    pos = kwargs.get("pos", [0, 0, 0])
    zz = kwargs.get("zz", "bottom")
    depth = radius_1 * 2
    #zz 
    if zz == "bottom":
        pos[2] += 0
    elif zz == "top":
        pos[2] += -depth
    elif zz == "middle":
        pos[2] += -depth/2

    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "sphere"
    p3["r"] = radius
    sc = (radius_2 / radius_1) * 2
    return_value = ([opsc.opsc_easy(**p3)])
    return_value[0]["scale"] = [1,1,sc]
    return return_value


# cylinder
def get_oobb_cylinder(**kwargs):
    zz = kwargs.get("zz", "center")
    radius_name = kwargs.get("radius_name", "")
    
    modes = ["laser", "3dpr", "true"]
    return_value = []
    # deciding how to define depth either string or name
    try:
        depth = kwargs["depth"]
    except:
        try:
            depth = kwargs["depth_mm"]
        except:
            depth = 250
    # figuring out z so it is in the middle of the object
    try:
        kwargs["pos"][2] = kwargs["pos"][2] - depth / 2
    except:
        try:
            kwargs["z"] = kwargs["z"] - depth / 2
        except:
            pass
    if zz == "bottom":
        kwargs["pos"][2] += depth / 2
    if zz == "top":
        kwargs["pos"][2] -= depth / 2

    for mode in modes:
        kwargs["shape"] = "cylinder"
        if radius_name != "":
            kwargs.update({"r": oobb.gv(radius_name, mode)})
        else:
            try:
                kwargs.update({"r": kwargs["radius"]})
            except:
                try:
                    kwargs.update({"r": kwargs["r"]})
                except:
                    #using r1 and r2
                    try:
                        kwargs.update({"r1": kwargs["radius_1"]})
                        kwargs.update({"r2": kwargs["radius_2"]})
                    except:
                        try:
                            kwargs.update({"r1": kwargs["r1"]})
                            kwargs.update({"r2": kwargs["r2"]})
                        except:
                            print("no radius defined errror in oobb_get_items get_oobb_cylinder")
                            pass

                    pass
                
        if isinstance(depth, str):
            kwargs.update({"h": oobb.gv(depth, mode)})
        else:
            kwargs.update({"h": depth})
        kwargs.update({"inclusion": mode})
        return_value.append(opsc.opsc_easy(**kwargs))
    return return_value

# electronic

#      battery_box
def get_oobb_electronic_battery_box_aa_battery_4_cell(**kwargs):    
    typ = kwargs.get("type", "positive")
    kwargs["type"] = "positive" #setting it to positive because it's a rotation object
    depth_screw = kwargs.get("depth_screw", 6)
    extra = kwargs.get("extra", "")
    rot_original = get_rot(**kwargs)       
    rot = [0,0,0]
    kwargs["rot"] = rot
    thickness = kwargs.get("thickness", 100)
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    pos_original = copy.deepcopy(pos)
    pos = [0,0,0]
    kwargs["pos"]  = pos    
    part = kwargs.get("part", "all")

    return_value = []


    if part == "all":
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_cube_center"
        p3["size"] = [62, 58, 15]
        pos1 = copy.deepcopy(pos)        
        p3["pos"] = pos1
        p3["zz"] = "bottom"
        return_value.append((oobb.oe(**p3)))

        #add screws
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_screw_countersunk"
        p3["radius_name"] = "m3"
        p3["depth"] = depth_screw
        pos1 = copy.deepcopy(pos)
        pos1[2] += 2
        posa = copy.deepcopy(pos1)
        posa[0] += 22.5
        posb = copy.deepcopy(pos1)
        posb[0] += -22.5
        posc = copy.deepcopy(pos1)
        posc[0] += 7.5
        posd = copy.deepcopy(pos1)
        posd[0] += -7.5
        p3["pos"] = [posa, posb, posc, posd]
        p3["zz"] = "top"
        #p3["m"] = "#"
        return_value.append((oobb.oe(**p3)))

        #add through clearance cube
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_cube_center"
        p3["size"] = [10, 10, thickness]
        pos1 = copy.deepcopy(pos)
        pos1[0] += 16        
        pos1[1] += 24
        
        p3["pos"] = pos1
        p3["zz"] = "top"
        #p3["m"] = "#"
        return_value.append((oobb.oe(**p3)))

        #add thin clearance cube
        p4 = copy.deepcopy(p3)
        p4["size"] = [30, 10, 3]
        pos1 = copy.deepcopy(p3["pos"])
        pos1[0] += -10
        pos1[1] += 0
        pos1[2] += 0
        p4["pos"] = pos1
        #p4["m"] = "#"
        return_value.append((oobb.oe(**p4)))
        

        #add wire cutout
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_wire_higher_voltage"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -6
        pos1[1] += 15
        pos1[2] += 0
        p3["pos"] = pos1
        rot = [0,0,180]
        p3["rot"] = rot
        p3["zz"] = "top"
        #p3["m"] = "#"
        return_value.append((oobb.oe(**p3)))


    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]

    return return_value_2

#      button
def get_oobb_electronic_button_11_mm_panel_mount(**kwargs):
    clearance = kwargs.get("clearance", ["top", "bottom"])
    typ = kwargs.get("type", "positive")
    kwargs["type"] = "positive" #setting it to positive because it's a rotation object
    
    extra = kwargs.get("extra", "")
    rot_original = get_rot(**kwargs)       
    rot = [0,0,0]
    kwargs["rot"] = rot
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    pos_original = copy.deepcopy(pos)
    pos = [0,0,0]
    kwargs["pos"]  = pos    
    part = kwargs.get("part", "all")

    return_value = []

    if part == "all":
        clearance = kwargs.get("clearance", False)
        extra_clearance = 0
        if clearance:
            extra_clearance = 20
        return_value = []
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [12/2, 7/2]
        p2["h"] = [18, 12]
        return_value.extend((get_cylinders(**p2)))
        return_value = oobb.shift(return_value, [0, 0, -18-extra_clearance])
        
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]

    return return_value_2


#      potentiometer
def get_oobb_electronic_potentiometer_17_mm(**kwargs):
    clearance = kwargs.get("clearance", ["top", "bottom"])
    typ = kwargs.get("type", "positive")
    kwargs["type"] = "positive" #setting it to positive because it's a rotation object
    
    extra = kwargs.get("extra", "")
    rot_original = get_rot(**kwargs)       
    rot = [0,0,0]
    kwargs["rot"] = rot
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    pos_original = copy.deepcopy(pos)
    pos = [0,0,0]
    kwargs["pos"]  = pos    
    part = kwargs.get("part", "all")

    return_value = []


    if part == "all":
        clearance = kwargs.get("clearance", False)
        extra_clearance = 0
        if clearance:
            extra_clearance = 20
        return_value = []
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [18/2, 7.5/2, 6/2]
        p2["h"] = [9+extra_clearance, 7, 14]
        return_value.extend((get_cylinders(**p2)))
        return_value = oobb.shift(return_value, [0, 0, -9-extra_clearance])
        #return_value = oobb.shift(return_value, [0, 0, -30])

        #add a keying cube 1.2 x 2.8 x 2.5 plus 0.5 at 0,8
        p2 = copy.deepcopy(kwargs)
        extra = 0.5
        height = 2.8
        width = 1.2
        depth = 2.6
        p2["size"] = [width+extra, height+extra, depth+extra]
        #offset pos for center postion
        p2["pos"] = [p2["pos"][0]-8, p2["pos"][1], p2["pos"][2]]
        return_value.append((get_oobb_cube_center(**p2)))

        # add a cube for the wires 18 x 25.5 x 3 at 0, -3.75, 0
        p2 = copy.deepcopy(kwargs)
        extra = 0
        height = 12.5
        width = 18
        depth = 3+extra_clearance
        p2["size"] = [width+extra, height+extra, depth+extra]
        #offset pos for center postion    
        p2["pos"] = [p2["pos"][0], p2["pos"][1]-5.75, p2["pos"][2] - depth]
        return_value.append((get_oobb_cube_center(**p2)))

        # add a cube for the wire bottoms
        p2 = copy.deepcopy(kwargs)
        extra = 0
        height = 5.5
        width = 13
        #depth = 3
        p2["size"] = [width+extra, height+extra, depth+extra]
        #offset pos for center postion    
        p2["pos"] = [p2["pos"][0], p2["pos"][1]-13.75, p2["pos"][2] -depth]
        return_value.append((get_oobb_cube_center(**p2)))
    elif part == "shaft":
        return_value = []  
        p2 = copy.deepcopy(kwargs)
        p2["r"] = 5.9/2
        p2["type"] = typ
        p2["shape"] = "oobb_hole"                
        return_value.extend(oobb.oe(**p2))        
        return return_value


    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]

    return return_value_2

def get_oobb_electronic_potentiometer_stick_single_axis_16_mm(**kwargs):
    clearance = kwargs.get("clearance", ["top", "bottom"])
    typ = kwargs.get("type", "positive")
    kwargs["type"] = "positive" #setting it to positive because it's a rotation object
    
    extra = kwargs.get("extra", "")
    rot_original = get_rot(**kwargs)       
    rot = [0,0,0]
    kwargs["rot"] = rot
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    pos_original = copy.deepcopy(pos)
    pos = [0,0,0]
    kwargs["pos"]  = pos    
    part = kwargs.get("part", "all")
    width_stick = kwargs.get("width_stick", 2)

    return_value = []


    if part == "all":
        clearance = kwargs.get("clearance", False)
        extra_clearance = 0
        if clearance:
            extra_clearance = 20
        return_value = []
        
        # main cube
        p3 = copy.deepcopy(kwargs)
        pos1 = copy.deepcopy(pos)        
        p3["shape"] = "oobb_cube_center"      
        cube_depth = 12  
        p3["size"] = [16,16,cube_depth]
        p3["zz"] = "bottom"
        p3["pos"] = pos1
        #p3["m"] = "#"        
        return_value.extend(oobb.oobb_easy(**p3))

        # feet cubes
        p3 = copy.deepcopy(kwargs)        
        pos1 = copy.deepcopy(pos)        
        poss = []
        shift_y = 15/2
        shift_x = 13.5/2
        poss.append([pos1[0]+shift_x, pos1[1]+shift_y, pos1[2]])
        poss.append([pos1[0]-shift_x, pos1[1]+shift_y, pos1[2]])
        poss.append([pos1[0]+shift_x, pos1[1]-shift_y, pos1[2]])
        poss.append([pos1[0]-shift_x, pos1[1]-shift_y, pos1[2]])
        p3["shape"] = "oobb_cube_center"        
        p3["size"] = [3,1.5,4]
        p3["zz"] = "top"
        p3["pos"] = poss
        #p3["m"] = "#"        
        return_value.extend(oobb.oobb_easy(**p3))

        # extra side plastics
        # feet cubes
        p3 = copy.deepcopy(kwargs)        
        pos1 = copy.deepcopy(pos)        
        poss = []
        shift_x = 11/2
        poss.append([pos1[0]+shift_x, pos1[1], pos1[2]])
        poss.append([pos1[0]-shift_x, pos1[1], pos1[2]])
        p3["shape"] = "oobb_cube_center"        
        p3["size"] = [2,19,3.5]
        p3["zz"] = "bottom"
        p3["pos"] = poss
        #p3["m"] = "#"        
        return_value.extend(oobb.oobb_easy(**p3))


        # pot cube
        p3 = copy.deepcopy(kwargs)
        pos1 = copy.deepcopy(pos)        
        pos1[0] += 16/2 + 4/2
        pos1[2] += -4
        p3["shape"] = "oobb_cube_center"        
        p3["size"] = [4,12,16]
        p3["zz"] = "bottom"
        p3["pos"] = pos1        
        #p3["m"] = "#"        
        return_value.extend(oobb.oobb_easy(**p3))
        
        # other side clearance cube
        p3 = copy.deepcopy(p3)
        p3["size"] = [1.5,12,16]
        pos1 = copy.deepcopy(pos)
        pos1[0] -= 16/2 + 1.5/2        
        pos1[2] += -4
        p3["pos"] = pos1
        
        return_value.extend(oobb.oobb_easy(**p3))

        # stick
        p3 = copy.deepcopy(kwargs)
        pos1 = copy.deepcopy(pos)                
        pos1[2] += cube_depth
        p3["shape"] = "oobb_cube_center"        
        p3["size"] = [width_stick,1,9]
        p3["zz"] = "bottom"
        p3["pos"] = pos1        
        #p3["m"] = "#"        
        return_value.extend(oobb.oobb_easy(**p3))
        


    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]

    return return_value_2



# helpers
def get_oobb_overhang(**kwargs):
    return_value = []
    height_layer = 0.3
    radius_name = kwargs.get("radius_name", "m3")    
    zz = kwargs.get("zz", "bottom")
    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_cube_center" 
    p2["rotX"] = 0           
    p2["rotY"] = 0           
    p2["rotZ"] = 0           
    p2["inclusion"] = "3dpr"
    
    #get the size
    if radius_name == "m3":    
        width = 3.5
        height = 6.5
    elif radius_name == "m3_nut":            
        height = (oobb.gv("nut_radius_m3_3dpr") * 2) / 1.154
        width = (oobb.gv("hole_radius_m3_3dpr") * 2)
    elif radius_name == "m2":    
        width = 2.5
        height = 5.5    
    elif radius_name == "m6":    
        width = 5.75
        height = 10    
    else:
        width = 3.5
        height = 6.5


    p2["size"] = [width, height, height_layer] 
    if zz == "bottom":
        p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2]]            
    else:
        p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2]]
    
    #p2["m"] = "#"
    return_value.append(oobb.oe(**p2))
    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_cube_center"  
    p2["rotX"] = 0           
    p2["rotY"] = 0           
    p2["rotZ"] = 0            
    p2["inclusion"] = "3dpr"
    p2["size"] = [width, width, height_layer] 
    if zz == "bottom":
        p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2]+height_layer]        
    else:
        p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2]-height_layer]        
    #p2["m"] = "#"
    return_value.append(oobb.oe(**p2))

    return return_value

def get_rot(**kwargs):
    rot = kwargs.get("rot", "")
    if rot == "":
        rot_x = kwargs.get('rot_x',0)
        rot_y = kwargs.get('rot_y',0)
        rot_z = kwargs.get('rot_z',0)
        rot = [rot_x, rot_y, rot_z]        
        kwargs["rot"] = rot
        kwargs.pop('rot_x', None)
        kwargs.pop('rot_y', None)
        kwargs.pop('rot_z', None)
        kwargs.pop("rot", None)
        
    return rot

def get_oobb_slice(**kwargs):
    p3 = copy.deepcopy(kwargs)
    
    modes = p3.get("mode", ["laser", "3dpr", "true"])
    pos = copy.deepcopy(p3.get("pos", [0, 0, 0]))
    size = copy.deepcopy(p3.get("size", [500, 500, 500]))
    p3["pos"] = pos
    zz = p3.get("zz", "bottom")

    return_value = []


    if pos[0] == 0 and pos[1] == 0:
        pos = [-size[0]/2,-size[1]/2,pos[2]]
        p3["pos"] = pos
    
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    
    if type(modes) == str:
        modes = [modes]

    shift = -size[2]
    p4 = copy.deepcopy(p3)
    for mode in modes:
        p3 = copy.deepcopy(p4)        
        p3["shape"] = "cube"
        p3["size"] = copy.deepcopy(size)
        
        #shift 250
        if zz == "bottom":
            p3["pos"][2] += 0
        elif zz == "top":
            p3["pos"][2] += shift
        kwargs.update({"inclusion": mode})
        #p3["m"] = "#"
        return_value.append(opsc.opsc_easy(**p3))
    return return_value

# hole
def get_oobb_hole_new(**kwargs):
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    depth = kwargs.get("depth", 100)
    default_zz = "bottom"
    if depth == 100:
        default_zz = "middle"
    zz = kwargs.get("zz", default_zz)
    radius_name = kwargs.get("radius_name", "")
    radius = kwargs.get("radius", 0)

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


    # modes
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]

    # zz
    pos1 = copy.deepcopy(pos)
    if zz == "bottom":
        pos1[2] += 0
    elif zz == "top":
        pos1[2] += -depth
    elif zz == "middle":
        pos1[2] += -depth/2
    kwargs["pos"] = pos1

    return_value = []
    for mode in modes:
        p3 = copy.deepcopy(kwargs)
        p3["inclusion"] = mode
        p3["shape"] = "cylinder"
        # radius
        if radius_name != "":
            r = ob.gv("hole_radius_"+radius_name, mode)
        else:
            r = radius
        p3["r"] = r
        p3["h"] = depth
        return_value.append(opsc.opsc_easy(**p3))
    
    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]


    return return_value_2


# motor

#      motor_servo_standard_01
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
def get_oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible(**kwargs):
    part = kwargs.get("part", "all")


    typ = kwargs.get("type", "p")
    kwargs["type"] = "p" #setting it to positive because it's a rotation object    
    
    rot = get_rot(**kwargs)
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

    if part == "all":        
        pos = kwargs.get("pos", [0, 0, 0])

             
        # shaft hole
        p3 = copy.deepcopy(kwargs)
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        p3["shape"] = "oobb_hole"
        p3["radius"] = 12/2        
        #p3["m"] = "#"
        return_value.append(ob.oobb_easy(**p3))

        # add screw holes
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = "m2_5"
        poss = []
        pos1 = copy.deepcopy(pos)
        split = 15.75
        pos1[0] += split /2
        pos2 = copy.deepcopy(pos1)
        pos2[0] = -pos2[0]
        poss.append(pos1)
        poss.append(pos2)
        p3["pos"] = poss
        #p3["m"] = "#"
        return_value.append(ob.oobb_easy(**p3))

        
        
        
    
        
    
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]

        return return_value_2

    

# nut
def get_oobb_nut(**kwargs):
    l_string = ""
    pos = kwargs.get("pos", [0, 0, 0])
    kwargs["pos"] = pos
    pos = copy.deepcopy(pos)
    extra = kwargs.get("extra", "")
    depth = kwargs.get("depth", "")
    overhang = kwargs.get("overhang", False)
    zz = kwargs.get("zz", "bottom")
    clearance = kwargs.get("clearance", "")
    hole = kwargs.get("hole", False) #whether or not to include a hole
    extra_clearance = kwargs.get("extra_clearance", 0)
    clearance_tightness = kwargs.get("clearance_tightness", 0) #tight or loose

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
    pos = [0,0,0]
    kwargs["pos"]  = pos

    
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]
    return_value = []

    for mode in modes:        
        p2 = copy.deepcopy(kwargs)
        p2["shape"] = "polyg"
        p2["sides"] = 6
        p2["inclusion"] = mode
        radius_name = p2["radius_name"]
        extra_str = ""
        #extra loose or tight
        #if extra != "":
        #    extra_str = f"_{extra}"
        
        r = oobb.gv(f"nut_radius_{l_string}{radius_name}{extra_str}", mode)
        r = r + clearance_tightness
        p2.update({"r": r})
        
        #getting depth of nut
        if depth == "":
            depth = oobb.gv(f"nut_depth_{l_string}{radius_name}", mode)
        
        #setting anchor point zz
        if zz == "top":
            p2["pos"][2] += -depth            
        elif zz == "middle":
            p2["pos"][2] += -depth/2            
        else:
            p2["pos"][2] += 0
        
        #clearance
        if "top" in clearance:
            depth += 50
        if "bottom" in clearance:
            depth += 50
            p2["pos"][2] -= 100
        #side clearance
        if True:
            p4 = copy.deepcopy(p2)
            p4["shape"] = "cube"
            hei = r*2 + extra_clearance * 0.866
            wid = 20
            dep = depth
            if extra_clearance > 0:
                dep += extra_clearance          
            p4.pop("r", "")
            p4.pop("radius", "")
            p4.pop("radius_name", "")
            p4["size"] = [wid, hei, dep]
            pos1 = copy.deepcopy(p2["pos"])
            pos1[0] += -wid/2
            pos1[1] += -hei/2
            if "left" in clearance:                
                pos1[0] += wid/2
                p4["pos"] = pos1
                return_value.append(oobb.oobb_easy(**p4))
            if "right" in clearance:                
                pos1[0] += -wid/2
                p4["pos"] = pos1
                return_value.append(oobb.oobb_easy(**p4))
            
            


        p2["height"] = depth
        return_value.append(opsc.opsc_easy(**p2))
        
        


        # overhang
        if overhang:
            p3 = copy.deepcopy(kwargs)
            if zz == "top":
                p3["pos"][2] += -depth            
            elif zz == "middle":
                p3["pos"][2] += -depth/2            
            else:
                p3["pos"][2] += 0
            p3["shape"] = "oobb_overhang" 
            #p3["radius_name"] = "m3_nut"
            p3["inclusion"] = "3dpr"
            pos1 = copy.deepcopy(p3["pos"])                   
            pos1[2] += 0
            p3["pos"] = pos1
            #p3["m"] = "#"
            p3["zz"] = "top"
            return_value.append(oobb.oe(**p3))
            p4 = copy.deepcopy(p3)
            pos1 = copy.deepcopy(p3["pos"])
            pos1[2] += depth
            p4["pos"] = pos1
            #p4["m"] = "#"
            p4["zz"] = "bottom"
            return_value.append(oobb.oe(**p4))
        # hole
        if hole:
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_hole"
            p3.pop("depth", "")
            return_value.extend(oobb.oobb_easy(**p3))

            # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]


    return return_value_2

# plate
def get_oobb_pl(**kwargs):
    return get_oobb_plate(**kwargs)

def get_oobb_plate(**kwargs):
    kwargs = copy.deepcopy(kwargs)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    extra_mm = kwargs.get("extra_mm", False)
    depth_mm = kwargs.get("depth", 3)
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    zz = kwargs.get("zz", "bottom")
    holes = kwargs.get("holes", False)
    include = kwargs.get("include", "")

    return_value = []

    if zz == "top":
        pos[2] += -depth_mm
    elif zz == "middle":
        pos[2] += -depth_mm/2
    else:
        pos[2] += 0
    kwargs["pos"] = pos

    
    #add extra_mm
    if extra_mm:
        width = width + 1/15 
        height = height + 1/15
    
    width_mm = width * oobb.gv("osp") - oobb.gv("osp_minus")
    height_mm = height * oobb.gv("osp") - oobb.gv("osp_minus")
    


    # if 1 x 1 than just cylinder
    if kwargs["width"] == 1 and kwargs["height"] == 1:
        
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "cylinder"
        p3["r"] = (width * oobb.gv("osp") - oobb.gv("osp_minus"))/2
        p3["h"] = depth_mm
        return_value.append(opsc.opsc_easy(**p3))

    else:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "rounded_rectangle"
        p3["width_mm"] = width_mm
        p3["height_mm"] = height_mm
        p3["size"] = [ width_mm, height_mm, depth_mm]
        return_value.append(opsc.opsc_easy(**p3))
        

    if holes or "hole" in include:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_holes"
        p3["both_holes"] = True  
        p3.pop("holes", None)
        rot = p3.get("rot", [0, 0, 0])
        if rot[2] == 90:   #if rotated 90 degrees do the hole swap
            wid = p3["width"]
            hei = p3["height"]
            p3["width"] = hei
            p3["height"] = wid
        return_value.extend(oobb.oobb_easy(**p3))

    return return_value

#screw
def get_oobb_screw_countersunk(**kwargs):
    kwargs["style"] =  "countersunk"
    return get_oobb_screw(**kwargs)

def get_oobb_screw_self_tapping(**kwargs):
    kwargs["style"] =  "self_tapping"
    return get_oobb_screw(**kwargs)
    
def get_oobb_screw_socket_cap(**kwargs):
    kwargs["style"] =  "socket_cap"
    return get_oobb_screw(**kwargs)

def get_oobb_screw(**kwargs):
    
    hole = kwargs.get("hole", True)
    style = kwargs.get("style", "socket_cap")
    kwargs.pop("style", None)
    clearance = kwargs.get("clearance", "")
    nut_include = kwargs.get("nut_include", kwargs.get("include_nut",kwargs.get("nut", False)))    
    overhang = kwargs.get("overhang", True)
    radius_name = kwargs.get("radius_name", "m3")
    loose = kwargs.get("loose", "")
    depth = float(kwargs.get("depth", 250))
    zz = kwargs.get("zz", "none")
    
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
    

    
    return_value = []
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes] 

    
    for mode in modes: 
        depth_clearance_top = 250       
        pos_for_overhang = [0, 0, 0]
        pos_base = [0, 0, 0]
        #socket_cap stuff 
        if style == "socket_cap" or style == "self_tapping":
            depth_head = oobb.gv(f'screw_{style}_height_{radius_name}', mode)
            
            #sort out zz by adjusting pos
            pos = copy.deepcopy(pos_base)
            if zz == "top":
                pos_for_overhang[2] = pos_for_overhang[2] - depth_head
            elif zz == "bottom":
                pos_for_overhang[2] = pos_for_overhang[2] + depth 

            #needs to happen after zz is sorted
            if "top" in clearance and mode == "3dpr":            
                depth_head = depth_head + depth_clearance_top            

            pos1 = copy.deepcopy(pos_for_overhang)
            # screw top
            p3 = copy.deepcopy(kwargs)        
            p3["shape"] = "cylinder"
            p3["pos"] = [pos1[0], pos1[1], pos1[2]]
            p3["r"] = oobb.gv(f"screw_{style}_radius_{radius_name}", mode)
            p3["h"] = depth_head        
            p3["inclusion"] = mode        
            p3.pop("radius_name", None)
            p3.pop("radius", None)
            #p3["m"] = ""
            return_value.append(oobb.oobb_easy(**p3))
        #countersunk stuff
        if style == "countersunk":
            if zz == "top":
                pass
            elif zz == "bottom":
                pos_original[2] = copy.deepcopy(pos_original_original[2]) + depth
            shifts = [0, -depth, -depth]
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "cylinder"
            p3["inclusion"] = mode
            dep = oobb.gv(f"screw_countersunk_depth_{radius_name}", mode)
            p3["h"] = dep
            pos1 = copy.deepcopy(pos_base)
            #pos1[2] = pos1[2] - dep / 2 #hold over mistake but fixed now maybe in bearing plate works check trays
            pos1[2] = pos1[2] - dep

            p3["pos"] = pos1            
            p3["r2"] = oobb.gv(f"screw_countersunk_radius_{radius_name}", mode)
            p3["r1"] = oobb.gv(f"hole_radius_{radius_name}", mode)
            #p3["m"] = "#"
            return_value.extend(oobb.oobb_easy(**p3))   
            #clearance = kwargs.get("clearance", "")
            if "top" in clearance:      
                      
                depth_head = depth_clearance_top  
                # screw top
                p3 = copy.deepcopy(kwargs)        
                p3["shape"] = "cylinder"                
                p3["pos"] = [pos1[0], pos1[1], pos1[2]+dep/2]
                if style == "countersunk":
                    p3["pos"] = [pos1[0], pos1[1], pos1[2]+dep]
                p3["r"] = oobb.gv(f"screw_{style}_radius_{radius_name}", mode)
                p3["h"] = depth_head        
                p3["inclusion"] = mode        
                p3.pop("radius_name", None)
                p3.pop("radius", None)
                #p3["m"] = ""
                return_value.append(oobb.oobb_easy(**p3))  
        # hole    
        if hole:
            radius = oobb.gv(f"hole_radius_{radius_name}", mode)
            if style == "self_tapping":
                if "screw" in loose:    
                    radius = oobb.gv(f"screw_self_tapping_hole_loose_radius_{radius_name}", mode)
                else:
                    radius = oobb.gv(f"screw_self_tapping_hole_radius_{radius_name}", mode)
            p3 = copy.deepcopy(kwargs)
            p3.pop("radius_name", "")
            p3["radius"] = radius
            p3["shape"] = "oobb_hole"
            pos1 = copy.deepcopy(pos_for_overhang)
            p3["pos"] = [pos1[0], pos1[1], pos1[2] - depth]
            p3["inclusion"] = mode        
            #p3["m"] = "#"
            return_value.extend(oobb.oobb_easy(**p3))
        # nut
        if nut_include:
            pos1 = copy.deepcopy(pos_for_overhang)
            p3 = copy.deepcopy(kwargs)
            clearance_copy = copy.deepcopy(clearance)
            if "top" in clearance_copy:
                if clearance_copy == "top":
                    p3.pop("clearance", "")
                elif "top" in clearance_copy:
                    for i in range(len(clearance_copy)):
                        if clearance_copy[i] == "top":
                            clearance_copy.pop(i) 
                            p3["clearance"] = clearance_copy
                            break                           

            p3.pop("zz","")
            # maybe add a nut level argument later
            p3["shape"] = "oobb_nut"
            p3["inclusion"] = mode   
            p3["overhang"] = overhang
            p3["pos"] = [pos1[0], pos1[1], pos1[2] -depth]
            p3.pop("loose", "")
            if "nut" in loose:
                p3["loose"] = True
            p3.pop("extra", "")
            if "bottom" in clearance:
                h_nut = oobb.gv(f'nut_depth_{radius_name}', mode)
                dep = depth_clearance_top
                p3["depth"] = dep
                p3["pos"][2] = p3["pos"][2] + h_nut #- dep
                p3["zz"] = "top"
                p3.pop("clearance", "")
            else:
                p3.pop("depth", None)
            #dealing with rot_Z
            rotation_nut = kwargs.get("rotation_nut", None)
            if rotation_nut != None:
                p3["rot"] = rotation_nut    

            #p3["m"] = "#"
            return_value.extend(oobb.oobb_easy(**p3))
        # overhang    
        if overhang and style != "countersunk" and mode == "3dpr":        
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_overhang"
            p3["zz"] = "top"
            p3["inclusion"] = "3dpr"  
            p3.pop("width", "")      
            p3.pop("height", "")
            #p3["m"] = "#"
            pos1 = copy.deepcopy(pos_for_overhang)
            p3["pos"] = [pos1[0],pos1[1],pos1[2]]
            
            
            #if rot_y == 180:
            #    p3["zz"] = "bottom"     
            #    p3["pos"] = [pos[0], pos[1], pos[2]-0.3]         
            return_value.extend(oobb.oobb_easy(**p3))

    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]


    return return_value_2


# slot
def get_oobb_slot(**kwargs):
    
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    depth = kwargs.get("depth", "")
    pos = kwargs.get("pos", [0, 0, 0])
    pos = copy.deepcopy(pos)
    zz = kwargs.get("zz", "middle")
    radius = kwargs.get("radius", "")
    radius_name = kwargs.get("radius_name", "")
    radius_1 = kwargs.get("radius_1", "")
    radius_2 = kwargs.get("radius_2", "")
    
    
    #      mode sorting
    if modes == "all":
        modes = ["laser", "3dpr", "true"]    
    if type(modes) != list:
        modes = [modes]

    #      depth sorting
    if depth == "":
            depth = 250
            pos[2] = pos[2] - depth / 2

    #      zz sorting
    if zz == "middle":
        pos[2] = pos[2] - depth / 2
        kwargs["pos"] = pos
    elif zz == "bottom":
        pos[2] = pos[2] - depth
        kwargs["pos"] = pos
    elif zz == "top":
        pass



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


    return_value = []
    p3 = copy.deepcopy(kwargs)
    for mode in modes:
        if radius_name != "":
            radius = ob.gv("hole_radius_"+radius_name, mode)
        p3["shape"] = "slot"
        if radius_1 == "":        
            p3["r"] = radius
        else:
            p3["r1"] = radius_1
            p3["r2"] = radius_2
        p3["h"] = depth
        p3.update({"inclusion": mode})
        return_value.append(opsc.opsc_easy(**p3))
    
    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]


    return return_value_2

#tube
def get_oobb_tube(**kwargs):
    
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
    
    m_original = kwargs.get("m", "")
    kwargs.pop("m", None)

    r = kwargs.get("r", kwargs.get("r", ""))
    if r == "":
        r = kwargs.get("radius", "")
        #update r
        kwargs["r"] = r
        # pop radius
        kwargs.pop("radius", "")


    if kwargs["type"] == "p" or kwargs["type"] == "positive":
        kwargs["type"] = "negative"
    else:
        kwargs["type"] = "positive"
    kwargs["wall_thickness"] = kwargs.get("wall_thickness", 0.5)
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]

    z = kwargs.get("z", 0)
    if z == 0:
        pos = kwargs.get("pos", [0, 0, 0])
        pos = copy.deepcopy(pos)
    return_value = []
    try:
        depth = kwargs["depth"]
    except:
        depth = 250
        try:
            kwargs["pos"][2] = pos[2] - depth / 2
        except:
            kwargs["z"] = z - depth / 2

    try:
        radius_name = kwargs["radius_name"]
        for mode in modes:
            kwargs["shape"] = "cylinder"
            try:
                kwargs.update({"r": ob.gv("hole_radius_"+radius_name, mode)})
            except:
                r = ob.gv(radius_name, mode)
                kwargs.update({"r": r})                
            kwargs.update({"h": depth})
            kwargs.update({"inclusion": mode})
            return_value.append(opsc.opsc_easy(**kwargs))
            #tube innard
            p2 = copy.deepcopy(kwargs)
            if p2["type"] == "p" or p2["type"] == "positive":
                p2["type"] = "negative"
            else:
                p2["type"] = "positive"
            p2["r"] = p2["r"] + p2["wall_thickness"]
            return_value.append(opsc.opsc_easy(**p2))

    except:
        for mode in modes:
            r = kwargs.get("r", kwargs.get("radius", 0))
            kwargs["shape"] = "cylinder"
            kwargs.update({"r": r})
            kwargs.update({"h": depth})
            kwargs.update({"inclusion": mode})
            return_value.append(opsc.opsc_easy(**kwargs))
            #tube innard
            p2 = copy.deepcopy(kwargs)
            if p2["type"] == "p" or p2["type"] == "positive":
                p2["type"] = "negative"
            else:
                p2["type"] = "positive"
            p2["r"] = p2["r"] + p2["wall_thickness"] 
            return_value.append(opsc.opsc_easy(**p2))
    
    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2["m"] = m_original
    return_value_2 = [return_value_2]


    return return_value_2

def get_oobb_tube_new(**kwargs):
    
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
    
    m_original = kwargs.get("m", "")
    kwargs.pop("m", None)

    r = kwargs.get("r", kwargs.get("r", ""))
    if r == "":
        r = kwargs.get("radius", "")
        #update r
        kwargs["r"] = r
        # pop radius
        kwargs.pop("radius", "")


    if kwargs["type"] == "p" or kwargs["type"] == "positive":
        kwargs["type"] = "negative"
    else:
        kwargs["type"] = "positive"
    kwargs["wall_thickness"] = kwargs.get("wall_thickness", 0.5)
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]

    z = kwargs.get("z", 0)
    if z == 0:
        pos = kwargs.get("pos", [0, 0, 0])
        pos = copy.deepcopy(pos)
    return_value = []
    try:
        depth = kwargs["depth"]
    except:
        depth = 250
        try:
            kwargs["pos"][2] = pos[2] - depth / 2
        except:
            kwargs["z"] = z - depth / 2

    try:
        radius_name = kwargs["radius_name"]
        for mode in modes:
            kwargs["shape"] = "cylinder"
            try:
                kwargs.update({"r": ob.gv("hole_radius_"+radius_name, mode)})
            except:
                r = ob.gv(radius_name, mode)
                kwargs.update({"r": r})                
            kwargs.update({"h": depth})
            kwargs.update({"inclusion": mode})
            #tube innard
            p2 = copy.deepcopy(kwargs)
            p2["r"] = p2["r"] - p2["wall_thickness"] 
            if p2["type"] == "p" or p2["type"] == "positive":
                p2["type"] = "negative"
            else:
                p2["type"] = "positive"
            return_value.append(opsc.opsc_easy(**p2))
            
            #tube outard
            p2 = copy.deepcopy(kwargs)
            p2['r'] = r
            if p2["type"] == "p" or p2["type"] == "positive":
                p2["type"] = "positive"
            else:
                p2["type"] = "negative"
            #p2["r"] = p2["r"] - p2["wall_thickness"] 
            return_value.append(opsc.opsc_easy(**p2))

    except:
        for mode in modes:
            r = kwargs.get("r", kwargs.get("radius", 0))
            kwargs["shape"] = "cylinder"
            kwargs.update({"r": r})
            kwargs.update({"h": depth})
            kwargs.update({"inclusion": mode})
            
            #tube innard
            p2 = copy.deepcopy(kwargs)
            p2["r"] = p2["r"] - p2["wall_thickness"] 
            if p2["type"] == "p" or p2["type"] == "positive":
                p2["type"] = "positive"
            else:
                p2["type"] = "negative"
            return_value.append(opsc.opsc_easy(**p2))
            
            #tube outard
            p2 = copy.deepcopy(kwargs)
            p2['r'] = r
            if p2["type"] == "p" or p2["type"] == "positive":
                p2["type"] = "negative"
            else:
                p2["type"] = "positive"
            #p2["r"] = p2["r"] - p2["wall_thickness"] 
            return_value.append(opsc.opsc_easy(**p2))
    
    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2["m"] = m_original
    return_value_2 = [return_value_2]


    return return_value_2


# wire
def get_oobb_wire_basic(**kwargs):
    kwargs["num_pins"] = 3
    kwargs.update({"polarized": True})
    return get_oobb_wire_cutout(**kwargs)

def get_oobb_wire_higher_voltage(**kwargs):
    kwargs["num_pins"] = 2
    kwargs.update({"polarized": True})
    return get_oobb_wire_cutout(**kwargs)

def get_oobb_wire_i2c(**kwargs):
    kwargs["num_pins"] = 4
    kwargs.update({"polarized": True})
    return get_oobb_wire_cutout(**kwargs)

def get_oobb_wire_motor(**kwargs):
    kwargs["num_pins"] = 2
    kwargs.update({"polarized": False})
    return get_oobb_wire_cutout(**kwargs)

def get_oobb_wire_motor_stepper(**kwargs):
    kwargs["num_pins"] = 4
    kwargs.update({"polarized": False})
    return get_oobb_wire_cutout(**kwargs)

def get_oobb_wire_spacer(**kwargs):
    kwargs["length_spacer"] = 23
    kwargs["pos_spacer"] = [-1.5,0,0]
    return get_oobb_wire_spacer_base(**kwargs)

def get_oobb_wire_spacer_long(**kwargs):
    kwargs["length_spacer"] = 29
    kwargs["pos_spacer"] = [-4.5,0,0]
    return get_oobb_wire_spacer_base(**kwargs)

def get_oobb_wire_spacer_u(**kwargs):
    kwargs["length_spacer"] = 40
    kwargs["pos_spacer"] = [-10,0,0]
    return get_oobb_wire_spacer_base(**kwargs)


def get_oobb_wire_spacer_base(**kwargs):
    # setting up for rotation object
    typ = kwargs.get("type", "negative")
    kwargs["type"] = "positive" #needs to be positive for the difference to work
    rot_original = get_rot(**kwargs)  
    kwargs.pop("rot","") 
   
    length_spacer = kwargs.get("length_spacer", 23)
    pos_spacer = kwargs.get("pos_spacer", [-1.5,0,0])

    # storing pos and popping it out to add it in rotation element     
    pos_original = copy.deepcopy(copy.deepcopy(kwargs.get("pos", [0, 0, 0])))
    kwargs.pop("pos", None)
    pos = [0,0,0]
    kwargs["pos"] = pos
    return_value = []

    p3 = copy.deepcopy(kwargs)
    pos_plate = p3.get("pos", [0, 0, 0])
    thickness = p3.get("thickness", 1)
    
    pos1 = copy.deepcopy(pos_plate)
    pos1[0] = pos1[0] + pos_spacer[0]
    pos1[2] = pos1[2] - thickness + 3
    p3 = copy.deepcopy(kwargs)    
    p3["shape"] = f"rounded_rectangle"      
    p3["size"] = [length_spacer,22,thickness]
    p3["pos"] = pos1
    return_value.append( oobb.oe(**p3))

    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]


    return return_value_2 


def get_oobb_wire_cutout(**kwargs):
    # setting up for rotation object
    typ = kwargs.get("type", "negative")
    kwargs["type"] = "positive" #needs to be positive for the difference to work
    rot_original = get_rot(**kwargs)  
    kwargs.pop("rot","") 
   

    # storing pos and popping it out to add it in rotation element     
    pos_original = copy.deepcopy(copy.deepcopy(kwargs.get("pos", [0, 0, 0])))
    kwargs.pop("pos", None)
    pos = [0,0,0]
    kwargs["pos"] = pos


    width = kwargs.get("width", 2)
    height = kwargs.get("height", 2)    
    polarized = kwargs.get("polarized", False)
    through = kwargs.get("through", False)
    num_pins = kwargs.get("num_pins", 2)


    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]

    pole_extra = 0
    if polarized:
        pole_extra = 1
    shift = 2 - num_pins

    return_value = []
    depth_universal = 2.6
    for mode in modes:
        #depth = oobb.gv("wi_depth", mode) 
        depth = depth_universal
        extra = oobb.gv("wi_extra", mode)
        i01 = oobb.gv("wi_i01", mode)        
        p3 = copy.deepcopy(kwargs)
        length = oobb.gv("wi_length", mode)
        
        ##wire back piece
        wbp = copy.deepcopy(kwargs)
        wid = 5
        hei = i01 * num_pins - 2
        depth = depth_universal
        #depth = 8
        size = [wid, hei, depth]
        x = 25.567
        y = 2.54 + (shift) * 2.54/2
        z = 0 
        pos1 = copy.deepcopy(pos)
        pos1[0] = kwargs["pos"][0] + x
        pos1[1] = kwargs["pos"][1] + y
        pos1[2] = kwargs["pos"][2] + z
        wbp["pos"] = pos1
        wbp["shape"] = "oobb_cube_center"
        wbp["size"] = size    
        wbp["inclusion"] = mode    
        return_value.append(oobb.oe(**wbp))
        
        ##big piece front       
        extra_bpf = 1 
        bpf = copy.deepcopy(wbp)
        wid = length - 8 + extra_bpf
        hei = i01 * (num_pins+polarized) + extra
        size = [wid, hei, depth]
        x = 3.354 - extra_bpf / 2
        y = wbp["pos"][1] - 2.54 / 2 * polarized
        z = 0
        pos1 = copy.deepcopy(pos)
        pos1[0] = pos1[0] + x
        pos1[1] = pos1[1] + y
        pos1[2] = pos1[2] + z
        bpf["shape"] = "oobb_cube_center"
        bpf["pos"] = pos1
        bpf["size"] = size    
        #bpf["m"] = "#"
        bpf["inclusion"] = mode    
        return_value.append(oobb.oe(**bpf))
        
        ##big piece back
        bpb = copy.deepcopy(wbp)        
        wid = length
        hei = i01 * num_pins + extra
        size = [wid, hei, depth]        
        x = 16.038
        y = wbp["pos"][1]
        z = 0
        pos1 = copy.deepcopy(pos)
        pos1[0] = pos1[0] + x
        pos1[1] = pos1[1] + y
        pos1[2] = pos1[2] + z        
        bpb["pos"] = pos1
        bpb["size"] = size
        return_value.append(oobb.oe(**bpb))
        
        ##key piece
        kp = copy.deepcopy(bpf)
        wid = i01 + extra
        hei = i01 * (num_pins + 2 + polarized) + extra
        size = [wid, hei, depth]
        x = 7.77
        y = bpf["pos"][1]
        z = 0
        pos1 = copy.deepcopy(pos)
        pos1[0] = pos1[0] + x
        pos1[1] = pos1[1] + y
        pos1[2] = pos1[2] + z        
        kp["pos"] = pos1
        kp["size"] = size    
        return_value.append(oobb.oe(**kp))
        
        #big escape            
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_cube_center"
        pos1 = copy.deepcopy(pos)
        pos_shift = [22.5+6.044,0,0]
        pos1[0] = pos1[0] + pos_shift[0]
        pos1[1] = pos1[1] + pos_shift[1]
        pos1[2] = pos1[2] + pos_shift[2]
        p3["pos"] = pos1
        depth = depth_universal
        if through:
            depth = 10
        p3["size"] = [7, 10, depth]
        p3["inclusion"] = mode  
        p3["depth"] = depth
        #p3["m"] = "#"
        return_value.append(oobb.oe(**p3))
        

    #polariation dot
    if polarized:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_cylinder"
        x = 0.5
        shape = kwargs.get("shape", "")
        y = -15#default for ba
        z = 3/2
        p3["pos"] = [kwargs["pos"][0] + x, kwargs["pos"][1] + y, kwargs["pos"][2] + z]
        p3["r"] = 1.5
        p3["depth"] = depth_universal
        #p3["m"] = "#"
        return_value.extend(oobb.oobb_easy(**p3))
        
    pos_shift = [height/2*15,0,0]
    pos_original[0] += pos_shift[0]
    pos_original[1] += pos_shift[1]
    pos_original[2] += pos_shift[2]
    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]


    return return_value_2 

# ziptie
def get_oobb_zip_tie_clearance_small(**kwargs):
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


    return_value = []

    wall_thickness = kwargs.get("wall_thickness", 2)

    

    #add holes zip tie
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_hole"    
    
    poss = []
    pos1 = copy.deepcopy(pos)
    pos1[0] += 0
    pos11 = copy.deepcopy(pos1)
    pos11[1] += 3
    pos12 = copy.deepcopy(pos1)
    pos12[1] += -3
    poss.append(pos11)
    poss.append(pos12)
    p3["pos"] = poss
    p3["radius_name"] = "m3"    
    #p3["m"] = "#"
    return_value.append(oobb.oobb_easy(**p3))
    
    #add zip tie clearance square
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_cube"
    width = 3
    height = 8
    depth = 1.5
    p3["size"] = [width,height,depth]
    pos1 = copy.deepcopy(pos1)
    pos1[2] += 0
    p3["pos"] = pos1
    #p3["m"] = "#"
    return_value.append(oobb.oobb_easy(**p3))


    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]

    return return_value_2

    
