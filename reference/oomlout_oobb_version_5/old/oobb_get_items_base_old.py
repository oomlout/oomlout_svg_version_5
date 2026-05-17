import copy
import math

#print pythonpathenvironment variable
import os




import opsc
import solid2 as sp

import oobb_base as ob
from oobb_variables import *
from oobb_get_item_common import *

_BASE_LOADED = False

def _ensure_base():
    """Lazy-load oobb_get_items_base to break circular import."""
    global _BASE_LOADED
    if _BASE_LOADED:
        return
    _BASE_LOADED = True
    import oobb_get_items_base
    for name in dir(oobb_get_items_base):
        if not name.startswith('_') and name not in globals():
            globals()[name] = getattr(oobb_get_items_base, name)


def get_oobb_bearing(**kwargs):
    p3 = copy.deepcopy(kwargs)
    objects = []
    bearing_type = p3.get("bearing", p3.get("bearing_type", "608"))
    exclude_clearance = p3.get("exclude_clearance", False)
    zz = p3.get("zz", "center")
    pos = p3.get("pos", [0, 0, 0])

    modes = ["laser", "true", "3dpr"]
    for mode in modes:
        p3["inclusion"] = mode
        id = ob.gv(f"bearing_{bearing_type}_id", mode)
        od = ob.gv(f"bearing_{bearing_type}_od", mode)
        depth = ob.gv(f"bearing_{bearing_type}_depth", mode)
        p3["id"] = id
        p3["od"] = od
        p3["depth"] = depth
        
        p3["shape"] = "bearing"

        pos1 = copy.deepcopy(pos)
        if zz == "center" or zz == "middle":
            pos1[2] +=  0
        elif zz == "top":
            pos1[2] += -depth/2
        elif zz == "bottom":
            pos1[2] += depth/2

        p3["pos"] = pos1
        clearance_bearing = ob.gv(f"bearing_{bearing_type}_clearance", mode)
        p3["clearance_bearing"] = clearance_bearing
        p3.update({"exclude_clearance": exclude_clearance})
        objects.append(opsc.opsc_easy(**p3))

    return objects

    return


def get_oobb_bolt(include_nut=True, **kwargs):
    objects = []
    modes = ["laser", "3dpr", "true"]
    shifts = []

    for mode in modes:
        radius = kwargs["radius_name"]
        # countersink bit
        p2 = copy.deepcopy(kwargs)
        h = ob.gv(f'bolt_depth_{radius}', mode)
        depth = kwargs["depth"]
        rot = kwargs.get("rotY", 0)
        if rot == 180:
            shifts = [0, depth, depth]
        else:
            shifts = [0, -depth, -depth]

        pos = kwargs.get("pos", [0, 0, 0])
        pos1 = kwargs.get("pos", [0, 0, 0])
        p2["pos"] = [pos1[0], pos1[1], pos1[2] + shifts[0]]

        p2["r"] = ob.gv(f"bolt_radius_{radius}", mode)
        p2["h"] = h

        p2["shape"] = "polyg"
        p2["sides"] = 6
        p2["inclusion"] = mode
        objects.append(ob.oobb_easy(**p2))
    # hole
    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_hole"
    p2["inclusion"] = mode

    p2["pos"] = [pos1[0], pos1[1], pos1[2] + shifts[1]]
    objects.extend(ob.oobb_easy(**p2))
    # nut
    if include_nut:
        p2 = copy.deepcopy(kwargs)
        # maybe add a nut level argument later
        p2["shape"] = "oobb_nut"
        p2["inclusion"] = mode
        pos1 = kwargs.get("pos", [0, 0, 0])
        p2["pos"] = [pos[0], pos[1], pos[2] + shifts[2]]
        # p2["rotZ"] = 360/12
        objects.extend(ob.oobb_easy(**p2))

    return objects


def get_oobb_cube_center_old_1(**kwargs):
    kwargs.update({"shape": "cube"})
    all = kwargs.get("all", False)
    if not all:
        new_pos = [kwargs["pos"][0] - kwargs["size"][0]/2,
                kwargs["pos"][1] - kwargs["size"][1]/2, kwargs["pos"][2]]
    else:
        new_pos = [kwargs["pos"][0] - kwargs["size"][0]/2,
                kwargs["pos"][1] - kwargs["size"][1]/2, kwargs["pos"][2] - kwargs["size"][2]/2]
    kwargs.update({"pos": new_pos})
    return ob.oobb_easy(**kwargs)


def get_oobb_circle(**kwargs):
    kwargs.update(
        {"radius": kwargs["diameter"]/2 * ob.gv("osp") - ob.gv("osp_minus")})
    # set the size
    kwargs.update({"shape": "oobb_cylinder"})
    import oobb
    return oobb.oobb_easy(**kwargs)


def get_oobb_plate_old(**kwargs):

    # if 1 x 1 than just cylinder
    if kwargs["width"] == 1 and kwargs["height"] == 1:
        kwargs.update({"r": (kwargs["width"]
                    * ob.gv("osp") - ob.gv("osp_minus"))/2})
        kwargs.update({"h": kwargs["depth_mm"]})
        kwargs.update({"shape": "cylinder"})
        return opsc.opsc_easy(**kwargs)

    else:
        kwargs.update({"width_mm": kwargs["width"]
                    * ob.gv("osp") - ob.gv("osp_minus")})
        kwargs.update(
            {"height_mm": (kwargs["height"] * ob.gv("osp")) - ob.gv("osp_minus")})
        # set the size
        depth_mm = kwargs.get("depth_mm", kwargs.get("depth"))
        kwargs.update(
            {"size": [kwargs["width_mm"], kwargs["height_mm"], depth_mm]})

        kwargs.update({"shape": "rounded_rectangle"})
        return opsc.opsc_easy(**kwargs)


def get_oobb_holes(holes=["all"], **kwargs):
    objects = []
    modes = ["laser", "3dpr", "true"]
    width = kwargs.get("width", 0)
    height = kwargs.get("height", 0)
    pos = kwargs.get("pos", [0, 0, 0])
    depth = kwargs.get("depth", 100)
    pos = copy.deepcopy(pos)
    radius_name = kwargs.get("radius_name", "m6")
    middle = kwargs.get("middle", True)
    size = kwargs.get("size", "oobb")
    both_holes = kwargs.get("both_holes", False)
    circle = kwargs.get("circle", False)
    diameter_full = int(kwargs.get("diameter", 0))
    diameter = diameter_full
    diameter_clearance = kwargs.get("diameter_clearance", 7.5)
    diameter_center_clearance = kwargs.get("diameter_center_clearance", 0)
    if diameter_full % 1 != 0:
        diameter = diameter_full - diameter_full % 1
    if diameter != 0:
        width = diameter
        height = diameter
    
    

    x = pos[0]
    y = pos[1]
    z = pos[2]
    #if holes is not an array make it one
    if not isinstance(holes, list):
        holes = [holes]
    
    if isinstance(holes, bool):
        if holes:
            holes = ["all"]
        else:
            holes = ["none"]

    spacing = ob.gv("osp")
    if size == "oobe":
        spacing = ob.gv("osp") / 2

    m = kwargs.get("m", "")
    xx = x
    yy = y
    if "all" in holes:
        if not circle:
            for mode in modes:
                # find the start point needs to be half the width_mm plus half osp
                pos_start = [xx + -(width*spacing/2) + spacing/2,
                            yy + -(height*spacing/2) + spacing/2, z]
                objects.extend(ob.oobb_easy_array(type="negative", shape="hole", inclusion=mode, repeats=[
                            width, height], pos_start=pos_start, shift_arr=[spacing, spacing], middle=middle, r=ob.gv(f"hole_radius_{radius_name}", mode)))
        else:
            if diameter != 0:
                width = diameter
                height = diameter
            acceptable_holes  = []            
            pos_start = [xx + -(width*spacing/2) + spacing/2,
                        yy + -(height*spacing/2) + spacing/2, z]
            #find the acceptable holes
            for w in range(0, math.floor(width)):
                for h in range(0, math.floor(height)):
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    # only include if inside a circle of radius width * ob,gv("osp")/2
                    r = width*spacing/2 - diameter_clearance
                    if math.sqrt(x**2 + y**2) <= r:
                        # check if middle
                        if w == math.floor(width/2) and h == math.floor(height/2) and not middle:
                            pass
                        else:
                            #make sure diameter_center_clearance is met
                            if math.sqrt(x**2 + y**2) >= diameter_center_clearance:
                                acceptable_holes.append([w,h])
                            else:
                                pass
            #now add the holes
            for mode in modes:
                for hole in acceptable_holes:
                    x = pos_start[0] + hole[0]*spacing
                    y = pos_start[1] + hole[1]*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[x, y, 0], radius_name=radius_name, m=m))
    if "perimeter" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [xx + -(width*spacing/2) + spacing/2,
                     yy + -(height*spacing/2) + spacing/2, 0]
        # pos_start = [0,0,0]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == 0 or w == width-1 or h == 0 or h == height-1:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, 0], radius_name=radius_name, m=m))
    if "perimeter_miss_middle" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [xx + -(width*spacing/2) + spacing/2,
                     yy + -(height*spacing/2) + spacing/2, 0]
        # pos_start = [0,0,0]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == 0 or w == width-1 or h == 0 or h == height-1:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    w_test = math.floor(width/2)
                    h_test = math.floor(height/2)
                    if h != h_test and w != w_test:
                        objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                       x, y, 0], radius_name=radius_name, m=m))
    if "u" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [xx + -(width*spacing/2) + spacing/2,
                     yy + -(height*spacing/2) + spacing/2, 0]
        # pos_start = [0,0,0]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == 0 or w == width-1 or h == 0:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, 0], radius_name=radius_name, m=m))
    if "top" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [xx + -(width*spacing/2) + spacing/2,
                     yy + -(height*spacing/2) + spacing/2, z]
        # pos_start = [0,0,0]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == 0:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, z], radius_name=radius_name, m=m,depth=depth))
    if "bottom" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [xx + -(width*spacing/2) + spacing/2,
                     yy + -(height*spacing/2) + spacing/2, z]
        # pos_start = [0,0,0]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == width-1:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, z], radius_name=radius_name, m=m,depth=depth))
    if "right" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [xx + -(width*spacing/2) + spacing/2,
                     yy + -(height*spacing/2) + spacing/2, z]
        # pos_start = [0,0,0]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if h == height-1:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, z], radius_name=radius_name, m=m,depth=depth))
    if "left" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [xx + -(width*spacing/2) + spacing/2,
                     yy + -(height*spacing/2) + spacing/2, z]
        # pos_start = [0,0,0]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if h == 0:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, z], radius_name=radius_name, m=m,depth=depth))
    if "bottom_bottom" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [xx + -(width*spacing/2) + spacing/2,
                     yy + -(height*spacing/2) + spacing/2, 0]
        # pos_start = [0,0,0]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == width-1:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, 0], radius_name=radius_name, m=m,depth=depth))
    if "circle" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [xx + -(width*spacing/2) + spacing/2,
                     yy + -(height*spacing/2) + spacing/2, 0]
        # pos_start = [0,0,0]
        circle_dif = kwargs.get("circle_dif", 0)
        for w in range(0, math.floor(width)):
            for h in range(0, math.floor(height)):
                x = pos_start[0] + w*spacing
                y = pos_start[1] + h*spacing
                # only include if inside a circle of radius width * ob,gv("osp")/2
                r = ((width*spacing) - circle_dif)/2
                if math.sqrt(x**2 + y**2) <= r:
                    # check if middle
                    if w == math.floor(width/2) and h == math.floor(height/2) and not middle:
                        pass
                    else:
                        objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                       x, y, 0], radius_name=radius_name, m=m))
    if "corners" in holes or  "corner" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [xx + -(width*spacing/2) + spacing/2,
                     yy + -(height*spacing/2) + spacing/2, 0]
        # pos_start = [0,0,0]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == 0 and h == 0:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, 0], radius_name=radius_name, m=m))
                if w == 0 and h == height-1:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, 0], radius_name=radius_name, m=m))
                if w == width-1 and h == 0:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, 0], radius_name=radius_name, m=m))
                if w == width-1 and h == height-1:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, 0], radius_name=radius_name, m=m))
    if "single" in holes:
        # find the start point needs to be half the width_mm plus half osp
        locs = kwargs.get("loc", [0, 0])
        if locs == [0, 0]:
            locs = kwargs.get("location", [0, 0])
            if locs == [0, 0]:
                locs = kwargs.get("locations", [0, 0])
                if locs == [0, 0]:
                    locs = kwargs.get("positions", [0, 0])
        #if loc isn't an array of arrays then make it one
        if not isinstance(locs[0], list):
            locs = [locs]
        for loc in locs:
            pos_start = [xx + -(width*spacing/2) + spacing/2,
                        yy + -(height*spacing/2) + spacing/2, 0]
            x = pos_start[0] + (loc[0]-1)*spacing
            y = pos_start[1] + (loc[1]-1)*spacing
            objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                        x, y, z], radius_name=radius_name, m=m, depth=depth))
    if "missing_middle" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [xx + -(width*spacing/2) + spacing/2,
                     yy + -(height*spacing/2) + spacing/2, 0]
        # pos_start = [0,0,0]
        for w in range(0, int(width)):
            for h in range(0, int(height)):
                if w == math.floor(width/2) and h == math.floor(height/2):
                    pass
                else:
                    x = pos_start[0] + w*spacing
                    y = pos_start[1] + h*spacing
                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                   x, y, 0], radius_name=radius_name, m=m))
    if "just_middle" in holes:
        # find the start point needs to be half the width_mm plus half osp
        pos = [0,0,0]
        objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=pos, radius_name=radius_name, m=m))

    if both_holes:
        p2 = copy.deepcopy(kwargs)
        p2["shape"] = "oobe_hole"
        p2["radius_name"] = "m3"
        #make width two times minus one
        p2["width"] = width*2-1
        p2["height"] = height*2-1
        if diameter != diameter_full:
            p2["diameter"] = (diameter_full+0.5) * 2 - 1        
        else:
            if diameter != 0:
                p2["diameter"] = (diameter_full) * 2 - 1        
        #add holes
        p2["holes"] = holes
        #p2["m"] = "#"
        objects.extend(get_oobe_holes(**p2))

    return objects


def get_oobb_oring(**kwargs):
    objects = []
    oring_type = kwargs["oring_type"]
    
    modes = ["laser", "true", "3dpr"]
    for mode in modes:
        kwargs["inclusion"] = mode
        kwargs["id"] = ob.gv(f"oring_{oring_type}_id_tight", mode)
        kwargs["od"] = ob.gv(f"oring_{oring_type}_od", mode)
        kwargs["depth"] = ob.gv(f"oring_{oring_type}_depth", mode)
        kwargs["shape"] = "oring"
        objects.append(opsc.opsc_easy(**kwargs))

    return objects

def get_oobb_tire(**kwargs):
    objects = []
    
    
    kwargs["shape"] = "oring"
    objects.append(opsc.opsc_easy(**kwargs))

    return objects


def get_oobe_plate(**kwargs):
    kwargs.update({"width_mm": kwargs["width"]
                  * ob.gv("ospe") - ob.gv("ospe_minus")})
    kwargs.update(
        {"height_mm": (kwargs["height"] * ob.gv("ospe")) - ob.gv("ospe_minus")})
    # set the size
    kwargs.update(
        {"size": [kwargs["width_mm"], kwargs["height_mm"], kwargs["depth_mm"]]})

    kwargs.update({"shape": "rounded_rectangle"})
    kwargs.update({"r": 2.5})

    return opsc.opsc_easy(**kwargs)


def get_oobb_slot_old(**kwargs):
    objects = []
    modes = ["laser", "3dpr", "true"]
    w = kwargs["w"]
    for mode in modes:
        radius_name = kwargs.get("radius_name")
        radius = ob.gv(f"hole_radius_{radius_name}", mode)
        kwargs.update({"inclusion": mode})
        kwargs.update({"shape": "slot"})
        kwargs.update({"r": radius})
        kwargs["w"] = w + radius*2

        objects.append(opsc.opsc_easy(**kwargs))

    return objects

def get_oobb_fan_120_mm(**kwargs):
    objects = []
    
    off_center = 105
    holes = []
    holes.append([off_center/2, off_center/2])
    holes.append([off_center/2, -off_center/2])
    holes.append([-off_center/2, off_center/2])
    holes.append([-off_center/2, -off_center/2])
    
    #screw holes
    for hole in holes:
        p2 = copy.deepcopy(kwargs)
        p2["shape"] = "oobb_hole"
        p2["radius_name"] = "m3"
        #start with pos then add hole[0]
        p2["pos"] = [p2["pos"][0] + hole[0], p2["pos"][1] + hole[1], p2["pos"][2]]        
        objects.extend(ob.oobb_easy(**p2))

    p2 = copy.deepcopy(kwargs)
    

    p2 = copy.deepcopy(kwargs)
    x = 0
    y = 0
    z = 0
    p2["pos"] = [p2["pos"][0] + x, p2["pos"][1] + y, p2["pos"][2] + z]
    p2["shape"] = "oobb_cylinder"
    p2["r"] = 120/2
    p2["depth"] = 120
    objects.append(ob.oobb_easy(**p2))


    return objects



def get_oobb_holes_old(**kwargs):
    objects = []
    modes = ["laser", "3dpr", "true"]
    width = kwargs["width"]
    height = kwargs["height"]
    x = kwargs["pos"][0]
    y = kwargs["pos"][1]
    z = kwargs["pos"][2]
    for mode in modes:
        # find the start point needs to be half the width_mm plus half osp
        pos_start = [x + -(width*spacing/2) + spacing/2,
                     y + -(height*spacing/2) + spacing/2, z]

        objects.extend(ob.oobb_easy_array(type="negative", shape="hole", inclusion=mode, repeats=[
                       width, height], pos_start=pos_start, shift_arr=[spacing, spacing], r=ob.gv("hole_radius_m6", mode)))
    return objects


def get_oobe_holes(**kwargs):
    objects = []
    modes = ["laser", "3dpr", "true"]
    width = kwargs.get("width", 0)
    height = kwargs.get("height", 0)
    middle = kwargs.get("middle", True)
    kwargs["pos"] = kwargs.get("pos", [0, 0, 0])
    holes = kwargs.get("holes", ["all"])
    radius_name = kwargs.get("radius_name", "m3")
    extra = kwargs.get("extra", "")
    depth = kwargs.get("depth", 100)
    diameter_center_clearance = kwargs.get("diameter_center_clearance", 0)
    m = kwargs.get("m", "")
    x = kwargs["pos"][0]
    y = kwargs["pos"][1]
    z = kwargs["pos"][2]
    spacing = ob.gv("osp") / 2

    circle = kwargs.get("circle", False)
    diameter = kwargs.get("diameter", 0)
    diameter_clearance = kwargs.get("diameter_clearance", 1.5)
    if diameter != 0:
        width = diameter
        height = diameter


    #if holes isn't an array make it one
    if not isinstance(holes, list):
        holes = [holes]
    

    for hole in holes:
        for mode in modes:        
            # find the start point needs to be half the width_mm plus half osp
            xx = x  
            yy = y
            if hole == "all":
                if not circle:
                    pos_start = [x + -(width*ob.gv("ospe")/2) + ob.gv("ospe")/2,
                                y + -(height*ob.gv("ospe")/2) + ob.gv("ospe")/2, z]

                    
                    objects.extend(ob.oobb_easy_array(type="negative", shape="hole", inclusion=mode, repeats=[
                                width, height], pos_start=pos_start, shift_arr=[ob.gv("ospe"), ob.gv("ospe")], r=ob.gv("hole_radius_m3", mode)))
                else:
                    acceptable_holes  = []   
                    spacing = 7.5         
                    pos_start = [xx + -(width*spacing/2) + spacing/2,
                                yy + -(height*spacing/2) + spacing/2, z]
                    #find the acceptable holes
                    for w in range(0, math.floor(width)):
                        for h in range(0, math.floor(height)):
                            x = pos_start[0] + w*spacing
                            y = pos_start[1] + h*spacing
                            # only include if inside a circle of radius width * ob,gv("osp")/2
                            r = width*spacing/2 - (diameter_clearance)
                            distance_to_center = math.sqrt(x**2 + y**2)
                            if distance_to_center <= r:                                
                                #if middle make sure r is greater than 15
                                if middle or distance_to_center > 15:                                    
                                    #make sure diameter_center_clearance is met
                                    if math.sqrt(x**2 + y**2) >= diameter_center_clearance:
                                        acceptable_holes.append([w,h])
                                    else:
                                        pass                                            
                    #now add the holes
                    for mode in modes:
                        for hole in acceptable_holes:
                            x = pos_start[0] + hole[0]*spacing
                            y = pos_start[1] + hole[1]*spacing
                            objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[x, y, 0], radius_name=radius_name, m=m))                    
            if "circle_old" in holes:
                # find the start point needs to be half the width_mm plus half osp
                pos_start = [xx + -(width*spacing/2) + spacing/2,
                            yy + -(height*spacing/2) + spacing/2, 0]
                # pos_start = [0,0,0]
                circle_dif = kwargs.get("circle_dif", 0)
                for w in range(0, math.floor(width)):
                    for h in range(0, math.floor(height)):
                        x = pos_start[0] + w*spacing
                        y = pos_start[1] + h*spacing
                        # only include if inside a circle of radius width * ob,gv("osp")/2
                        r = ((width*spacing) - circle_dif)/2
                        if math.sqrt(x**2 + y**2) <= r:
                            # check if middle
                            if w == math.floor(width/2) and h == math.floor(height/2) and not middle:
                                pass
                            else:
                                trim_test = True
                                #if w and h are both odd thrn trim test = true
                                if w % 2 == 1 and h % 2 == 1:
                                    trim_test = False
                                if extra != "trim_down" or trim_test:
                                    objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                            x, y, 0], radius_name=radius_name, m=m))
            if "corners" in holes:
                # find the start point needs to be half the width_mm plus half osp
                pos_start = [xx + -(width*spacing/2) + spacing/2,
                            yy + -(height*spacing/2) + spacing/2, 0]
                # pos_start = [0,0,0]
                for w in range(0, int(width)):
                    for h in range(0, int(height)):
                        if w == 0 and h == 0:
                            xx = pos_start[0] + w*spacing
                            yy = pos_start[1] + h*spacing
                            objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                        xx, yy, 0], radius_name=radius_name, m=m))
                        if w == 0 and h == height-1:
                            xx = pos_start[0] + w*spacing
                            yy = pos_start[1] + h*spacing
                            objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                        xx, yy, 0], radius_name=radius_name, m=m))
                        if w == width-1 and h == 0:
                            xx = pos_start[0] + w*spacing
                            yy = pos_start[1] + h*spacing
                            objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                        xx, yy, 0], radius_name=radius_name, m=m))
                        if w == width-1 and h == height-1:
                            xx = pos_start[0] + w*spacing
                            yy = pos_start[1] + h*spacing
                            objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                        xx, yy, 0], radius_name=radius_name, m=m,depth=depth))
            if "perimeter" in holes:
                # find the start point needs to be half the width_mm plus half osp
                pos_start = [xx + -(width*spacing/2) + spacing/2,
                            yy + -(height*spacing/2) + spacing/2, 0]
                # pos_start = [0,0,0]
                for w in range(0, int(width)):
                    for h in range(0, int(height)):
                        if w == 0 or w == width-1 or h == 0 or h == height-1:
                            xx = pos_start[0] + w*spacing
                            yy = pos_start[1] + h*spacing
                            objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[xx, yy, 0], radius_name=radius_name, m=m,depth=depth))
            if "top" in holes:
                # find the start point needs to be half the width_mm plus half osp
                pos_start = [xx + -(width*spacing/2) + spacing/2,
                            yy + -(height*spacing/2) + spacing/2, 0]
                # pos_start = [0,0,0]
                for w in range(0, int(width)):
                    for h in range(0, int(height)):
                        if w == 0:
                            xxx = pos_start[0] + w*spacing
                            yyy = pos_start[1] + h*spacing
                            objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                        xxx, yyy, z], radius_name=radius_name, m=m,depth=depth))
            if "bottom" in holes:
                # find the start point needs to be half the width_mm plus half osp
                pos_start = [xx + -(width*spacing/2) + spacing/2,
                            yy + -(height*spacing/2) + spacing/2, 0]
                # pos_start = [0,0,0]
                for w in range(0, int(width)):
                    for h in range(0, int(height)):
                        if w == width-1:
                            xxx = pos_start[0] + w*spacing
                            yyy = pos_start[1] + h*spacing
                            objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                        xxx, yyy, z], radius_name=radius_name, m=m,depth=depth))
            if "right" in holes:
                # find the start point needs to be half the width_mm plus half osp
                pos_start = [xx + -(width*spacing/2) + spacing/2,
                            yy + -(height*spacing/2) + spacing/2, 0]
                # pos_start = [0,0,0]
                for w in range(0, int(width)):
                    for h in range(0, int(height)):
                        if h == height-1:
                            xxx = pos_start[0] + w*spacing
                            yyy = pos_start[1] + h*spacing
                            objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                        xxx, yyy, z], radius_name=radius_name, m=m,depth=depth))
            if "left" in holes:
                # find the start point needs to be half the width_mm plus half osp
                pos_start = [xx + -(width*spacing/2) + spacing/2,
                            yy + -(height*spacing/2) + spacing/2, 0]
                # pos_start = [0,0,0]
                for w in range(0, int(width)):
                    for h in range(0, int(height)):
                        if h == 0:
                            xxx = pos_start[0] + w*spacing
                            yyy = pos_start[1] + h*spacing
                            objects.extend(ob.oobb_easy(type="negative", shape="oobb_hole", pos=[
                                        xxx, yyy, z], radius_name=radius_name, m=m,depth=depth))
        return objects


# def get_oobb_motor_tt_01(**kwargs):
#     return get_oobb_motor_gearmotor_01(**kwargs)

# def get_oobb_motor_gearmotor_tt_motor_01(**kwargs):
#     return get_oobb_motor_gearmotor_01(**kwargs)




def get_oobb_motor_servo_micro_01(**kwargs):
    #z zero is base of shaft
    part = kwargs.get("part", "all")
    if part == "all" or part == "only_holes":
        objects = []
        pos = kwargs.get("pos", [0, 0, 0])
        xx = pos[0]
        yy = pos[1]
        zz = pos[2]
        thickness = kwargs.get("thickness", 3)
        top_clearance = kwargs.get("top_clearance", False)
        bottom_clearance = kwargs.get("bottom_clearance", False)

        # kwargs["m"] = "#"

        # shaft hole
        p2 = copy.deepcopy(kwargs)
        p2["pos"] = [xx, yy, zz]
        p2["shape"] = "oobb_hole"
        p2["radius_name"] = "m5"
        objects.extend(ob.oobb_easy(**p2))

        
        # mounting holes
        poss = [-20, 0, 0], [8, -0, 0] #, [12, 0, thickness]
        for pos in poss:
            p4 = copy.deepcopy(kwargs)
            p4["pos"] = [xx+pos[0], yy+pos[1], zz+pos[2]]
            p4["shape"] = "oobb_hole"
            p4["radius_name"] = "m2d5"
            objects.extend(ob.oobb_easy(**p4))

        shaft_height = 3

        # main cube cube
        if "only_holes" not in part:
            servo_extra = 0.5 

            p5 = copy.deepcopy(kwargs)
            
            width = 23.75 + servo_extra
            height = 12 + servo_extra
            depth = 26
            x = xx-6
            y = yy-0
            z = zz - depth        
            p5["pos"] = [x,y,z]
            p5["shape"] = "oobb_cube_center"        
            p5["size"] = [width, height, depth]
            #p5["m"] = "#"
            objects.append(ob.oobb_easy(**p5))

            # bigger cube
            
            p5 = copy.deepcopy(kwargs)            
            width = 32 + servo_extra
            height = 12 + servo_extra
            depth = 2.5
            x = xx-6
            y = yy-0
            z = zz - depth - 8.5
            if top_clearance:
                depth = depth + 50
                z = z 
            if bottom_clearance:
                depth = depth + 50
                z = z - 50
            p5["size"] = [width, height, depth]
            p5["pos"] = [x,y,z]
            p5["shape"] = "oobb_cube_center"        
            
            #p5["m"] = ""
            objects.append(ob.oobb_easy(**p5))

        return objects
    elif part == "shaft":
        """ waiting to be able to do intersects and multi level things
        objects = []    
        pos = kwargs.get("pos", [0,0,0])
        x = pos[0]
        y = pos[1]
        z = pos[2]
        
        shaft_dia = 5.5
        p2 = copy.deepcopy(kwargs)
        p2["shape"] = "oobb_hole"
        p2["radius"] = shaft_dia /2
        objects.extend(ob.oobb_easy(**p2))

        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_cube_center"
        p3["size"] = [shaft_dia,0.875,100]
        p3["pos"] = [x,y+2.313,-50]
        objects.append(ob.oobb_easy(**p3))

        p4 = copy.deepcopy(p3)
        p4["pos"] = [x,y-2.313,-50]
        objects.append(ob.oobb_easy(**p4))
        """
        objects = []
        pos = kwargs.get("pos", [0, 0, 0])
        x = pos[0]
        y = pos[1]
        z = pos[2]

        horn_dia_bottom = 5
        horn_dia_top = horn_dia_bottom - 0.2
        
        horn_height = 3
        screw_radius_name = "m2"

        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_cylinder"
        p3["r2"] = horn_dia_top / 2
        p3["r1"] = horn_dia_bottom / 2
        p3["depth"] = horn_height
        p3["pos"] = [x, y,-6+horn_height/2]
        #p3["m"] = "#"
        objects.extend(ob.oobb_easy(**p3))
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = screw_radius_name
        objects.extend(ob.oobb_easy(**p3))
        return objects

def get_oobb_overhang_old_1(**kwargs):
    return_value = []
    height_layer = 0.3
    width = kwargs.get("width", 3.5)
    height = kwargs.get("height", 6.5)
    orientation = kwargs.get("orientation", "bottom")
    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_cube_center" 
    p2["rotX"] = 0           
    p2["rotY"] = 0           
    p2["rotZ"] = 0           
    p2["inclusion"] = "3dpr"
    
    p2["size"] = [width, height, height_layer] 
    if orientation == "bottom":
        p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2]-height_layer]            
    else:
        p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2]]
    
    #p2["m"] = "#"
    return_value.append(ob.oe(**p2))
    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_cube_center"  
    p2["rotX"] = 0           
    p2["rotY"] = 0           
    p2["rotZ"] = 0            
    p2["inclusion"] = "3dpr"
    p2["size"] = [width, width, height_layer] 
    if orientation == "bottom":
        p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2]]        
    else:
        p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2]-height_layer]        
    #p2["m"] = "#"
    return_value.append(ob.oe(**p2))

    return return_value

def get_oobb_motor_building_block_large_01(**kwargs):
    include_screws = kwargs.get("include_screws", True)
    top_clearance = kwargs.get("top_clearance", False)
    #z zero is base of shaft
    part = kwargs.get("part", "all")
    thickness = kwargs.get("thickness", 3)   
    if part == "all" or part == "only_holes":
        objects = []
        pos = kwargs.get("pos", [0, 0, 0])
        xx = pos[0]
        yy = pos[1]
        zz = pos[2]
             
        bottom_clearance = kwargs.get("bottom_clearance", False)

        # kwargs["m"] = "#"

        # shaft hole
        p2 = copy.deepcopy(kwargs)
        p2["pos"] = [xx, yy, zz]
        p2["shape"] = "oobb_hole"
        p2["radius_name"] = "m6"
        objects.extend(ob.oobb_easy(**p2))

        
        # mounting holes
        x1 = 14.25
        x2 = -36.25
        y1 = 4.75
        y2 = -y1
        poss = []
        poss.append([x1, y1, 0])
        poss.append([x1, y2, 0])
        poss.append([x2, y1, 0])
        poss.append([x2, y2, 0])
        for pos in poss:
            p4 = copy.deepcopy(kwargs)
            p4["pos"] = [xx+pos[0], yy+pos[1], zz+pos[2]]
            p4["shape"] = "oobb_hole"
            p4["radius_name"] = "m3"
            objects.extend(ob.oobb_easy(**p4))
            if include_screws:
                p4 = copy.deepcopy(kwargs)
                p4["pos"] = [xx+pos[0], yy+pos[1], zz+pos[2]-4] #the thickness of a socket head screw plus a bit
                p4["shape"] = "oobb_screw_socket_cap"
                p4["radius_name"] = "m3"
                p4["include_nut"] = False
                p4["depth"] = 25
                p4["top_clearance"] = True
                #p4["m"] ="#"
                objects.extend(ob.oobb_easy(**p4))

        shaft_height = 3

        # main cube cube
        if "only_holes" not in part:
            servo_extra = 0.5 

            p5 = copy.deepcopy(kwargs)
            
            width = 42 + servo_extra
            height = 21 + servo_extra
            depth = 40            
            x = xx-11
            y = yy-0
            z = zz - depth        
            if top_clearance:
                depth = depth + 50
                z = z 
            p5["pos"] = [x,y,z]
            p5["shape"] = "oobb_cube_center"        
            p5["size"] = [width, height, depth]
            #p5["m"] = "#"
            objects.append(ob.oobb_easy(**p5))

            #extra cutout  cube
            p5 = copy.deepcopy(kwargs)
            
            width = 50 + servo_extra
            height = 3 + servo_extra
            depth = 3
            x = xx-11
            y = yy-0
            z = zz - 8.5 
            p5["pos"] = [x,y,z]
            p5["shape"] = "oobb_cube_center"        
            p5["size"] = [width, height, depth]
            
            #p5["m"] = "#"
            objects.append(ob.oobb_easy(**p5))
            # bigger cube
            
            p5 = copy.deepcopy(kwargs)            
            #width = 57 + servo_extra
            width = 61 + servo_extra #extra width for clearance for a driver on the underside nut better dealt with with cylinders but this is easier for now
            height = 21 + servo_extra
            depth = 2.5
            x = xx-11
            y = yy-0
            z = zz - depth - 8.5
            
            if bottom_clearance:
                depth = depth + 50
                z = z - 50
            p5["size"] = [width, height, depth]
            p5["pos"] = [x,y,z]
            p5["shape"] = "oobb_cube_center"        
            
            #p5["m"] = ""
            objects.append(ob.oobb_easy(**p5))

        return objects
    elif part == "shaft":
        
        objects = []
        pos = kwargs.get("pos", [0, 0, 0])
        x = pos[0]
        y = pos[1]
        z = pos[2]

        #horn_dia_bottom = 6.1
        #horn_dia_top = horn_dia_bottom - 0.2
        horn_dia_bottom = 7.1
        horn_dia_top = horn_dia_bottom - 0

        horn_height = 6.6 #(1mm gap)

         
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_cylinder"
        p3["r2"] = horn_dia_top / 2
        p3["r1"] = horn_dia_bottom / 2
        p3["depth"] = horn_height
        p3["pos"] = [x, y,-6+horn_height/2]
        #p3["m"] = "#"
        objects.extend(ob.oobb_easy(**p3))

        #add a cube 4.25 x 2 x hornheight at the bottom
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_cube_center"
        #type is pp
        #outie
        #wid = 1.5
        #hei = 4.25
        #dep = horn_height
        #typ = "pp"
        #innie
        wid = 3
        hei = 5
        dep = 30
        typ = "n"

        p3["type"] = typ        
        p3["size"] = [hei, wid, dep]
        p3["pos"] = [0, 0,-6]
        p3["m"] = "#"
        objects.append(ob.oobb_easy(**p3))
        #add another but rotZ 90
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_cube_center"
        #type is pp
        p3["type"] = typ
        p3["size"] = [wid, hei, dep]
        p3["pos"] = [0, 0,-6]
        p3["m"] = "#"
        objects.append(ob.oobb_easy(**p3))


        return objects


def get_oobb_motor_n20(**kwargs):
    include_screws = kwargs.get("include_screws", True)
    top_clearance = kwargs.get("top_clearance", False)
    radius_extra = kwargs.get("radius_extra", 0.25)
    #z zero is base of shaft
    part = kwargs.get("part", "all")
    thickness = kwargs.get("thickness", 3)   
    if part == "all" or part == "only_holes":
        objects = []
        return objects
    elif part == "shaft":
        
        objects = []
        pos = kwargs.get("pos", [0, 0, 0])
        x = pos[0]
        y = pos[1]
        z = pos[2]

        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "d_shaft"
        r = 3/2 + radius_extra
        r_plus = 0
        id = 2.5 + radius_extra 
        p3["r"] = r + r_plus
        p3["id"] = id + r_plus
        p3["depth"] = 250
        p3["pos"] = [x, y,125]
        p3["comment"] = ["shaft for n20 motor"]
        #p3["m"] = "#"
        objects.extend(ob.oobb_easy(**p3))


        return objects



def get_oobb_motor_servo_standard_01_old_1(**kwargs):
    _ensure_base()
    include_screws = kwargs.get("include_screws", True)
    top_clearance = kwargs.get("top_clearance", False)
    #z zero is base of shaft
    part = kwargs.get("part", "all")
    thickness = kwargs.get("thickness", 3)   
    if part == "all" or part == "only_holes":
        objects = []
        pos = kwargs.get("pos", [0, 0, 0])
        xx = pos[0]
        yy = pos[1]
        zz = pos[2]
             
        bottom_clearance = kwargs.get("bottom_clearance", False)

        # kwargs["m"] = "#"

        # shaft hole
        p2 = copy.deepcopy(kwargs)
        p2["pos"] = [xx, yy, zz]
        p2["shape"] = "oobb_hole"
        p2["radius_name"] = "m6"
        objects.extend(ob.oobb_easy(**p2))

        
        # mounting holes
        x1 = 14.25
        x2 = -36.25
        y1 = 4.75
        y2 = -y1
        poss = []
        poss.append([x1, y1, 0])
        poss.append([x1, y2, 0])
        poss.append([x2, y1, 0])
        poss.append([x2, y2, 0])
        for pos in poss:
            p4 = copy.deepcopy(kwargs)
            p4["pos"] = [xx+pos[0], yy+pos[1], zz+pos[2]]
            p4["shape"] = "oobb_hole"
            p4["radius_name"] = "m3"
            objects.extend(ob.oobb_easy(**p4))
            if include_screws:
                p4 = copy.deepcopy(kwargs)
                p4["pos"] = [xx+pos[0], yy+pos[1], zz+pos[2]-4] #the thickness of a socket head screw plus a bit
                p4["shape"] = "oobb_screw_socket_cap"
                p4["radius_name"] = "m3"
                p4["include_nut"] = False
                p4["depth"] = 25
                p4["top_clearance"] = True
                #p4["m"] ="#"
                objects.extend(ob.oobb_easy(**p4))

        shaft_height = 3

        # main cube cube
        if "only_holes" not in part:
            servo_extra = 0.5 

            p5 = copy.deepcopy(kwargs)
            
            width = 42 + servo_extra
            height = 21 + servo_extra
            depth = 40            
            x = xx-11
            y = yy-0
            z = zz - depth        
            if top_clearance:
                depth = depth + 50
                z = z 
            p5["pos"] = [x,y,z]
            p5["shape"] = "oobb_cube_center"        
            p5["size"] = [width, height, depth]
            #p5["m"] = "#"
            objects.append(ob.oobb_easy(**p5))

            #extra cutout  cube
            p5 = copy.deepcopy(kwargs)
            
            width = 50 + servo_extra
            height = 3 + servo_extra
            depth = 3
            x = xx-11
            y = yy-0
            z = zz - 8.5 
            p5["pos"] = [x,y,z]
            p5["shape"] = "oobb_cube_center"        
            p5["size"] = [width, height, depth]
            
            #p5["m"] = "#"
            objects.append(ob.oobb_easy(**p5))
            # bigger cube
            
            p5 = copy.deepcopy(kwargs)            
            #width = 57 + servo_extra
            width = 61 + servo_extra #extra width for clearance for a driver on the underside nut better dealt with with cylinders but this is easier for now
            height = 21 + servo_extra
            depth = 2.5
            x = xx-11
            y = yy-0
            z = zz - depth - 8.5
            
            if bottom_clearance:
                depth = depth + 50
                z = z - 50
            p5["size"] = [width, height, depth]
            p5["pos"] = [x,y,z]
            p5["shape"] = "oobb_cube_center"        
            
            #p5["m"] = ""
            objects.append(ob.oobb_easy(**p5))

        return objects
    elif part == "shaft":
        
        objects = []
        pos = kwargs.get("pos", [0, 0, 0])
        x = pos[0]
        y = pos[1]
        z = pos[2]

        #horn_dia_bottom = 6.1
        #horn_dia_top = horn_dia_bottom - 0.2
        horn_dia_bottom = 5.8
        horn_dia_top = horn_dia_bottom - 0.2

        horn_height = 4
        screw_radius_name = "m2d5"

         
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = "oobb_cylinder"
        p3["r2"] = horn_dia_top / 2
        p3["r1"] = horn_dia_bottom / 2
        p3["depth"] = horn_height
        p3["pos"] = [x, y,-6+horn_height/2]
        #p3["m"] = "#"
        objects.extend(ob.oobb_easy(**p3))

        p3 = copy.deepcopy(kwargs)
        p3["m"] = "#"
        p3["pos"] = [x, y,-6+horn_height+0.3]
        objects.extend(get_oobb_overhang(**p3))
        
        

        # middle hole
        p4 = copy.deepcopy(kwargs)        
        p4["shape"] = "oobb_hole"
        p4["radius_name"] = screw_radius_name
        objects.extend(ob.oobb_easy(**p4))
        

        # add screw holes
        p4 = copy.deepcopy(kwargs)        
        p4["shape"] = "oobb_screw_self_tapping"
        p4["radius_name"] = "m2"
        p4["overhang"] = True
        #x = -5.215
        #y = -5.215
        #z = 0
        x = -0
        y = -7.375
        z = 0
        
        rot_y = 180
        p4["flush_top"] = True
        p4["rotY"] = rot_y
        #p4["m"] = "#"

        p4["pos"] = [p4["pos"][0] + x, p4["pos"][1] + y, p4["pos"][2]+z]
        objects.extend(ob.oobb_easy(**p4))
        p5 = copy.deepcopy(p4)
        x = -x
        y = -y
        p5["pos"] = [kwargs["pos"][0] + x, kwargs["pos"][1] + y, kwargs["pos"][2]+z]
        objects.extend(ob.oobb_easy(**p5))
        

        return objects

def get_oobb_powerbank_anker_323(**kwargs):
    objects = []
    # shaft hole
    p2 = copy.deepcopy(kwargs)
    
    x = 0
    y = 0
    z = 0
    p2["pos"] = [p2["pos"][0] + x, p2["pos"][1] + y, p2["pos"][2] + z]    
    p2["shape"] = "oobb_cube_center"
    width = 81
    height = 161
    depth = 17
    extra = 1
    
    p2["size"] = [width+extra, height+extra, depth+extra]
    
    objects.append(ob.oobb_easy(**p2))
    
    p2 = copy.deepcopy(kwargs)
    x = 0
    y = 64
    z = 0
    p2["pos"] = [p2["pos"][0] + x, p2["pos"][1] + y, p2["pos"][2] + z]
    p2["shape"] = "oobb_cylinder"
    p2["r"] = 20/2
    p2["depth"] = 120
    objects.append(ob.oobb_easy(**p2))


    return objects



def get_oobb_screw_countersunk_old_1(**kwargs):
    return get_oobb_countersunk(**kwargs)



def get_oobb_countersunk_old_1(**kwargs):
    objects = []
    top_clearance = kwargs.get("top_clearance", False)
    extra = kwargs.get("extra", "")
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if "all" in modes:
        modes = ["laser", "3dpr", "true"]
    if isinstance(modes, str):
        modes = [modes]

    shifts = []
    sandwich = kwargs.get("sandwich", False)
    include_nut_initial = kwargs.get("include_nut", True)

    # kwargs["m"] = "#"
    radius = kwargs.get("radius_name","m3")
    kwargs["radius_name"]   = radius
    pos = kwargs.get("pos", [0, 0, 0])
    kwargs["pos"] = [pos[0], pos[1], pos[2]]
    

    for mode in modes:
        # countersunk bit
        p2 = copy.deepcopy(kwargs)
        # p2["m"] = ""
        p2["inclusion"] = mode
        pos = p2.get("pos", [0, 0, 0])
        p2["pos"] = [pos[0], pos[1], pos[2]]
        depth = kwargs.get("depth", 100)
        rot = kwargs.get("rotY", 0)

        # top always countersunk size
        p2["r2"] = ob.gv(f"screw_countersunk_radius_{radius}", mode)
        if mode != "laser":
            p2["r1"] = ob.gv(f"hole_radius_{radius}", mode)
            h = ob.gv(f'screw_countersunk_height_{radius}', mode)
            include_nut = include_nut_initial
        else:
            # make a cylinder if laser
            p2["r1"] = ob.gv(f"screw_countersunk_radius_{radius}", mode)
            pass
            # remove nut if sandwich
            if sandwich:
                include_nut = False
            h = 3
            p2["pos"][2] = p2["pos"][2]
        p2["h"] = h
        # calculate shifts rather than rotating
        # index 0 shift for countersunk
        # index 1 shift for
        # index 2 shift for
        # index 3 shift for sandwich
        # index 4 shift for standoff
        # index 5 shift for top clearance
        if rot == 180:
            shifts = [-depth+h, 0, -3, depth-3-3, depth/2,2*-ob.gv(f'screw_countersunk_height_{radius}', mode)]
        else:
            shifts = [-h, -depth, -depth, -depth, depth/2,0]

        pos1 = kwargs.get("pos", [0, 0, 0])
        p2["pos"] = [pos1[0], pos1[1], pos1[2] + shifts[0]]
        p2["shape"] = "cylinder"
        p2["inclusion"] = mode
        objects.append(ob.oobb_easy(**p2))
        # if sandwich add second cylinder and internal standoff
        if mode == "laser" and sandwich:
            # add a second cylinder
            p3 = copy.deepcopy(p2)
            p3["inclusion"] = mode
            p3["mode"] = mode
            p3["pos"] = [pos1[0], pos1[1], pos1[2] + shifts[0] + shifts[3] + 3]
            objects.append(ob.oobb_easy(**p3))
            # standoff
            p4 = copy.deepcopy(kwargs)
            p4["shape"] = "oobb_standoff"
            p4["inclusion"] = mode
            p4["mode"] = mode
            pos1 = p4.get("pos", [0, 0, 0])
            p4["depth"] = depth - 6
            p4["pos"] = [pos1[0], pos1[1], pos1[2] + shifts[0] + shifts[3] + shifts[4]]

            p4["hole"] = True
            #p4["m"] = "#"
            objects.extend(ob.oobb_easy(**p4))
        p3 = copy.deepcopy(p2)
        # addinf top clearance not a great implementation only really works with 3dpr
        if top_clearance and mode == "3dpr":
            p3["shape"] = "cylinder"
            p3["r1"] = p2["r2"]
            p3['h'] = 250
            p3["pos"][2] = p3["pos"][2] + p2['h']  + shifts[5] - 0
            #p3['m'] = "#"
            objects.append(ob.oobb_easy(**p3))


    # hole
    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_hole"
    p2["inclusion"] = mode
    pos1 = kwargs.get("pos", [0, 0, 0])
    p2["pos"] = [pos1[0], pos1[1], pos1[2] + shifts[1]]
    objects.extend(ob.oobb_easy(**p2))
    # nut
    if include_nut:
        if mode != "laser":
            p2 = copy.deepcopy(kwargs)
            # maybe add a nut level argument later
            p2["shape"] = "oobb_nut"
            p2["extra"] = extra
            p2["inclusion"] = mode
            p2["pos"] = [kwargs["pos"][0], kwargs["pos"]
                         [1], kwargs["pos"][2] + shifts[2]]
            #p2["m"] = "#"
            p2["mode"] = ["3dpr", "true"]
            # p2["rotZ"] = 360/12
            objects.extend(ob.oobb_easy(**p2))

    return objects


def get_oobb_screw_self_tapping_old_1(include_nut=False, **kwargs):
    objects = []
    modes = ["laser", "3dpr", "true"]
    shifts = []    
    flush_top = kwargs.get("flush_top", False)
    loose = kwargs.get("loose", True)
    hole = kwargs.get("hole", True)
    top_clearance = kwargs.get("top_clearance", False)
    overhang = kwargs.get("overhang", False)

    for mode in modes:
        radius = kwargs["radius_name"]
        # countersink bit
        p2 = copy.deepcopy(kwargs)
        h = ob.gv(f'screw_self_tapping_height_{radius}', mode)
        depth = kwargs.get("depth", 250)
        kwargs["depth"] = depth
        rot = kwargs.get("rotY", 0)        
        pos = kwargs.get("pos", [0, 0, 0])
        pos = copy.deepcopy(pos)

        if flush_top:
            pass
            shift = ob.gv(f'screw_self_tapping_height_{radius}', mode)
            pos[2] = pos[2] - shift
            if rot == 180:
                pos[2] = pos[2] + shift * 2
            depth = depth - ob.gv(f'screw_self_tapping_height_{radius}', mode)       
        pos1 = copy.deepcopy(pos)

        if rot == 180:
            shifts = [0, depth, depth]
        else:
            shifts = [0, -depth, -depth]
        

        p2.pop("radius_name", None)
        p2.pop("radius", None)

        
        p2["pos"] = [pos1[0], pos1[1], pos1[2] + shifts[0]]

        p2["r"] = ob.gv(f"screw_self_tapping_washer_radius_{radius}", mode)        
        p2["h"] = h

        p2["shape"] = "cylinder"
        p2["inclusion"] = mode
        
        
        if top_clearance and mode == "3dpr":            
            p2["h"] = p2["h"] + 250

        #objects.extend(ob.oobb_easy(**p2))
        objects.append(ob.oobb_easy(**p2))

          
        
        # hole
        if hole:
            p2 = copy.deepcopy(kwargs)
            p2.pop("radius_name", None)
            p2["r"] = ob.gv(f"screw_self_tapping_hole_radius_{radius}", mode)
            if loose:
                p2["r"] = ob.gv(f"screw_self_tapping_hole_loose_radius_{radius}", mode)
            p2["shape"] = "oobb_hole"
            p2["inclusion"] = mode

            p2["pos"] = [pos1[0], pos1[1], pos1[2] + shifts[1]]
            objects.extend(ob.oobb_easy(**p2))
    # nut
    if include_nut:
        p2 = copy.deepcopy(kwargs)
        # maybe add a nut level argument later
        p2["shape"] = "oobb_nut"
        p2["inclusion"] = mode
        pos1 = kwargs.get("pos", [0, 0, 0])
        p2["pos"] = [pos[0], pos[1], pos[2] + shifts[2]]
        # p2["rotZ"] = 360/12
        objects.extend(ob.oobb_easy(**p2))
    # overhang    
    if overhang:
        p2 = copy.deepcopy(kwargs)
        p2["shape"] = "oobb_overhang"
        p2["orientation"] = "top"
        sh = 0.3
        if rot == 180:
            p2["orientation"] = "bottom"
            sh = 0.9
        p2["inclusion"] = "3dpr"        
        p2["pos"] = [pos[0], pos[1], pos[2]+sh]  
        p2["m"]       = "#"
        objects.extend(ob.oobb_easy(**p2))

    return objects


def get_oobb_screw_socket_cap_old_1(include_nut=True, **kwargs):
    objects = []
    modes = ["laser", "3dpr", "true"]
    shifts = []
    flush_top = kwargs.get("flush_top", False)
    hole = kwargs.get("hole", True)
    top_clearance = kwargs.get("top_clearance", False)
    overhang = kwargs.get("overhang", False)

    for mode in modes:
        radius = kwargs["radius_name"]
        # countersink bit
        p2 = copy.deepcopy(kwargs)
        h = ob.gv(f'screw_socket_cap_height_{radius}', mode)
        depth = kwargs.get("depth", 250)
        kwargs["depth"] = depth
        rot = kwargs.get("rotY", 0)        
        pos = kwargs.get("pos", [0, 0, 0])
        pos = copy.deepcopy(pos)

        if flush_top:
            pass
            shift = ob.gv(f'screw_socket_cap_height_{radius}', mode)
            pos[2] = pos[2] - shift
            depth = depth - ob.gv(f'screw_socket_cap_height_{radius}', mode)       
        pos1 = copy.deepcopy(pos)

        if rot == 180:
            shifts = [0, depth, depth]
        else:
            shifts = [0, -depth, -depth]
        

        p2.pop("radius_name", None)
        p2.pop("radius", None)

        
        p2["pos"] = [pos1[0], pos1[1], pos1[2] + shifts[0]]

        p2["r"] = ob.gv(f"screw_socket_cap_radius_{radius}", mode)
        p2["h"] = h

        p2["shape"] = "cylinder"
        p2["inclusion"] = mode
        
        
        if top_clearance and mode == "3dpr":            
            p2["h"] = p2["h"] + 250

        #objects.extend(ob.oobb_easy(**p2))
        objects.append(ob.oobb_easy(**p2))

          
        
    # hole
    if hole:
        p2 = copy.deepcopy(kwargs)
        p2["shape"] = "oobb_hole"
        p2["inclusion"] = mode

        p2["pos"] = [pos1[0], pos1[1], pos1[2] + shifts[1]]
        objects.extend(ob.oobb_easy(**p2))
    # nut
    if include_nut:
        p2 = copy.deepcopy(kwargs)
        # maybe add a nut level argument later
        p2["shape"] = "oobb_nut"
        p2["inclusion"] = mode
        pos1 = kwargs.get("pos", [0, 0, 0])
        p2["pos"] = [pos[0], pos[1], pos[2] + shifts[2]]
        # p2["rotZ"] = 360/12
        objects.extend(ob.oobb_easy(**p2))
    # overhang    
    if overhang:        
        p2 = copy.deepcopy(kwargs)
        p2["shape"] = "oobb_overhang"
        p2["orientation"] = "top"
        p2["inclusion"] = "3dpr"        
        p2["pos"] = [pos[0], pos[1], pos[2]-0.3]  
        #p2["m"] = "#"
        if rot == 180:
            p2["orientation"] = "bottom"     
            p2["pos"] = [pos[0], pos[1], pos[2]+0.3]  
        objects.extend(ob.oobb_easy(**p2))

    return objects


def get_oobb_text(**kwargs):
    return_value = []
    #check for depth then height then h then put the first one found into kwargs height
    depth = kwargs.get("depth", None)
    h = kwargs.get("h", None)
    height = kwargs.get("height", None)
    if depth:
        kwargs["height"] = depth
    elif h:
        kwargs["height"] = h
    elif height:
        kwargs["height"] = height
    else:
        kwargs["height"] = 0.3

    
    #if concate is true take the string include the first letter then every letter after an underscore and put this into kwargs text
    concate = kwargs.get("concate", False)
    if concate:
        text = kwargs.get("text", "")
        text = text[0] + "".join([x[0] for x in text.split("_")[1:]])
        kwargs["text"] = text

    size = kwargs.get("size", 7)
    kwargs["size"] = size
    font = kwargs.get("font", "Candara:Light")
    kwargs["font"] = font
    valign = kwargs.get("valign", "center")
    kwargs["valign"] = valign
    halign = kwargs.get("halign", "center")
    kwargs["halign"] = halign
    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "text"
    return_value.append(opsc.opsc_easy(**p2))


    return return_value


def get_oobb_threaded_insert(**kwargs):
    objects = []
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    hole = kwargs.get("hole", True)
    typ = kwargs.get("type", "hex")
    if "all" in modes:
        modes = ["laser", "3dpr", "true"]
    if isinstance(modes, str):
        modes = [modes]
    style = kwargs.get("style", "01")
    depth = kwargs.get("depth", 0)
    rotY = kwargs.get("rotY", 0)
    insertion_cone = kwargs.get("insertion_cone", False)

    # kwargs["m"] = "#"

    for mode in modes:

        radius = kwargs["radius_name"]
        # countersunk bit
        p2 = copy.deepcopy(kwargs)
        # p2["m"] = ""
        radius_name = f'threaded_insert_{style}_radius_{radius}'
        depth_threaded = ob.gv(f'threaded_insert_{style}_depth_{radius}', mode)
        shifts = []
        if rotY == 180:
            shifts = [0, -depth_threaded/2]
        else:
            shifts = [-depth_threaded, depth_threaded/2]
        p2["radius_name"] = radius_name
        p2["depth"] = depth_threaded
        pos = p2.get("pos", [0, 0, 0])
        p2["pos"] = [pos[0], pos[1], pos[2]+shifts[0]+shifts[1]]
        p2["shape"] = "oobb_cylinder"
        p2["inclusion"] = mode
        # p2["m"] = "#"
        objects.extend(ob.oobb_easy(**p2))

        # hole
        if hole:
            p2 = copy.deepcopy(kwargs)
            p2["shape"] = "oobb_hole"
            p2["inclusion"] = mode
            p2.pop("depth", None)
            p2.pop("rotY", None)
            pos1 = kwargs.get("pos", [0, 0, 0])
            p2["pos"] = [pos1[0], pos1[1], 0]
            objects.extend(ob.oobb_easy(**p2))
        #insertion cone
        if insertion_cone:
            if mode == "3dpr":
                #kwargs["m"] = "#"
                
                insertion_cone_extra = ob.gv(f'threaded_insert_{style}_insertion_cone_{radius}', mode)
                p2 = copy.deepcopy(kwargs)
                p2["shape"] = "cylinder"
                p2["inclusion"] = mode
                p2["pos"][2] = p2["pos"][2] - depth_threaded / 2 - insertion_cone_extra
                p2["h"] = insertion_cone_extra
                p2["r1"] = ob.gv(f'threaded_insert_{style}_radius_{radius}', mode)
                p2["r2"] = ob.gv(f'threaded_insert_{style}_radius_{radius}', mode) + insertion_cone_extra
                objects.append(ob.oobb_easy(**p2))
                p3 = copy.deepcopy(p2)
                p3["pos"][2] = p3["pos"][2] + insertion_cone_extra
                p3["r2"] = ob.gv(f'threaded_insert_{style}_radius_{radius}', mode)
                p3["r1"] = ob.gv(f'threaded_insert_{style}_radius_{radius}', mode) + insertion_cone_extra  
                
                objects.append(ob.oobb_easy(**p3))              
                
    return objects


def get_oobb_hole(**kwargs):
    pos = kwargs.get("pos", [0, 0, 0])
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
        depth = 200
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
    except:
        for mode in modes:
            r = kwargs.get("r", kwargs.get("radius", 0))
            kwargs["shape"] = "cylinder"
            kwargs.update({"r": r})
            kwargs.update({"h": depth})
            kwargs.update({"inclusion": mode})
            return_value.append(opsc.opsc_easy(**kwargs))
    return return_value

def get_oobb_hole_standoff(**kwargs):
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
                new_radius = ob.gv("hole_radius_"+radius_name, mode) + 2.5/2
                kwargs.update({"r": new_radius})
            except:
                r = ob.gv(radius_name, mode)
                kwargs.update({"r": r})
            kwargs.update({"h": depth})
            kwargs.update({"inclusion": mode})
            return_value.append(opsc.opsc_easy(**kwargs))
    except:
        for mode in modes:
            r = kwargs.get("r", kwargs.get("radius", 0))
            kwargs["shape"] = "cylinder"
            kwargs.update({"r": r})
            kwargs.update({"h": depth})
            kwargs.update({"inclusion": mode})
            return_value.append(opsc.opsc_easy(**kwargs))
    return return_value


def get_oobb_tube_old(**kwargs):
    
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
    return return_value



def get_oobb_slot_old(**kwargs):
    
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
    elif zz == "bottom":
        pos[2] = pos[2] - depth
    elif zz == "top":
        pass

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
    return return_value

def get_oobb_slice_old_1(**kwargs):
    
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    pos = kwargs.get("pos", [0, 0, 0])
    zz = kwargs.get("zz", "bottom")
    return_value = []
    pos = kwargs.get("pos", [0, 0, 0])
    if pos[0] == 0 and pos[1] == 0:
        pos = [250,250,0]
        kwargs["pos"] = pos
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]

    for mode in modes:        
        kwargs["shape"] = "cube"
        kwargs["size"] = [500,500,500]
        
        #shift 250
        if zz == "bottom":
            kwargs["pos"] = [pos[0]-250, pos[1]-250, pos[2] - 0]#
        elif zz == "top":
            kwargs["pos"] = [pos[0]-250, pos[1]-250, pos[2] - 500]
        kwargs.update({"inclusion": mode})
        return_value.append(opsc.opsc_easy(**kwargs))
    return return_value
    #rv = 
    #th.append(ob.oobb_easy(t="n", s="cube", size=[500, 500, 500], pos=[-500/2, -500/2, 0], inclusion=inclusion, m=""))    

def get_oobb_cylinder_old_1(**kwargs):

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

    for mode in modes:
        kwargs["shape"] = "cylinder"
        if radius_name != "":
            kwargs.update({"r": ob.gv(radius_name, mode)})
        else:
            try:
                kwargs.update({"r": kwargs["radius"]})
            except:
                try:
                    kwargs.update({"r": kwargs["r"]})
                except:
                    #using r1 and r2
                    pass
                
        if isinstance(depth, str):
            kwargs.update({"h": ob.gv(depth, mode)})
        else:
            kwargs.update({"h": depth})
        kwargs.update({"inclusion": mode})
        return_value.append(opsc.opsc_easy(**kwargs))
    return return_value


def get_oobb_nut_loose(**kwargs):
    kwargs["loose"] = True
    import oobb_get_items_base
    return oobb_get_items_base.get_oobb_nut(**kwargs)


def get_oobb_nut_through(**kwargs):
    kwargs["through"] = True
    import oobb_get_items_base
    return oobb_get_items_base.get_oobb_nut(**kwargs)


def get_oobb_nut_old_1(loose=False, through=False, **kwargs):
    l_string = ""
    extra = kwargs.get("extra", "")
    rotX = kwargs.get("rotX", 0)
    overhang = kwargs.get("overhang", True)
    zz = kwargs.get("zz", "")
    hole = kwargs.get("hole", False) #whether or not to include a hole
        
    if loose:
        l_string = "loose_"
    pos = kwargs.get("pos", [0, 0, 0])
    kwargs["pos"] = [pos[0], pos[1], pos[2]]
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]
    return_value = []
    for mode in modes:
        
        if not through:
            p2 = copy.deepcopy(kwargs)
            p2["shape"] = "polyg"
            p2["sides"] = 6
            p2["inclusion"] = mode
            radius_name = p2["radius_name"]
            extra_str = ""
            if extra != "":
                extra_str = f"_{extra}"
            r = ob.gv(f"nut_radius_{l_string}{radius_name}{extra_str}", mode)
            p2.update({"r": r})
            depth = ob.gv(f"nut_depth_{l_string}{radius_name}", mode)
            if zz == "top":
                p2["pos"][2] = p2["pos"][2] - depth
            p2.update(
                {"height": depth})
            return_value.append(opsc.opsc_easy(**p2))
        else:  # if through
            p2 = copy.deepcopy(kwargs)
            radius_name = p2["radius_name"]
            p2["shape"] = "cube"
            p2["inclusion"] = mode
            depth = ob.gv(f"nut_depth_loose_{radius_name}", mode)
            wid = ob.gv(f"nut_radius_loose_{radius_name}", mode) * 2 / 1.154
            hei = 100
            p2.update(
                {"pos": [p2["pos"][0]-wid/2, p2["pos"][1], p2["pos"][2]-25]})
            p2.update({"size": [wid, hei, depth]})
            return_value.append(opsc.opsc_easy(**p2))
        #### add 3d printing overhang pretifier
        if mode == "3dpr" and rotX == 0:
            #kwargs["m"] = "#"
            height_layer = 0.3
            extra_z = 0
            if zz == "top":
                extra_z = -depth
            if zz == "middle":
                extra_z = -depth/2
            adjusters = [[depth+extra_z, depth + height_layer + extra_z]]
            adjusters.append([-height_layer + extra_z, -height_layer*2 + extra_z])
            if overhang:
                for adjuster in adjusters:
                    p2 = copy.deepcopy(kwargs)
                    p2["shape"] = "oobb_cube_center" 
                    p2["rotX"] = 0           
                    p2["rotY"] = 0           
                    p2["rotZ"] = 0           
                    p2["inclusion"] = mode
                    
                    p2["size"] = [3.5, 6.5, height_layer] 
                    p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2] + adjuster[0]]            
                    
                    #p2["m"] = "#"
                    return_value.append(ob.oe(**p2))
                    p2 = copy.deepcopy(kwargs)
                    p2["shape"] = "oobb_cube_center"  
                    p2["rotX"] = 0           
                    p2["rotY"] = 0           
                    p2["rotZ"] = 0            
                    p2["inclusion"] = mode
                    p2["size"] = [3.5, 3.5, height_layer] 
                    p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2] + adjuster[1]]        
                    #p2["m"] = "#"
                    return_value.append(ob.oe(**p2))

        if hole:
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_hole"
            return_value.extend(ob.oobb_easy(**p3))
    return return_value


def get_oobb_standoff(loose=False, hole=False, **kwargs):
    l_string = ""
    extra = kwargs.get("extra", "")
    if loose:
        l_string = "loose_"

    pos = kwargs.get("pos", [0, 0, 0])
    kwargs["pos"] = [pos[0], pos[1], pos[2]]
    
    rot_y = kwargs.get("rotY", 0)
    if rot_y == 90:
        new_pos = [pos[1], pos[0], pos[2]]
        pos = new_pos
        kwargs["pos"] = [pos[0], pos[1], pos[2]]

    modes = kwargs.get("inclusion", ["laser", "3dpr", "true"])
    if not isinstance(modes, list):
        modes = [modes]
    return_value = []
    depth = kwargs.get("depth", 250)

    if hole:
        p2 = copy.deepcopy(kwargs)
        p2["shape"] = "oobb_hole"
        p2["t"] = "n"
        p2["type"] = "n"
        p2["m"] = ""
        return_value.extend(ob.oobb_easy(**p2))
    for mode in modes:
        p2 = copy.deepcopy(kwargs)
        p2["shape"] = "polyg"
        p2["sides"] = 6
        p2["inclusion"] = mode
        radius_name = kwargs["radius_name"]
        p2.update(
            {"r": ob.gv(f"standoff_radius_{l_string}{radius_name}", mode)})
        p2.update({"height": depth})
        #if depth = 250 then shift z down by 125
        if depth == 250:
            p2["pos"][2] = p2["pos"][2] - 125
        return_value.append(opsc.opsc_easy(**p2))
        if "support" in extra:
            height_layer = 0.3
            adjusters = [[depth, depth + height_layer]]
            adjusters.append([-height_layer, -height_layer*2])

            for adjuster in adjusters:
                p2 = copy.deepcopy(kwargs)
                p2["shape"] = "oobb_cube_center"            
                p2["inclusion"] = mode
                
                p2["size"] = [3.5, 6.5, height_layer] 
                p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2] + adjuster[0]]            
                #p2["m"] = "#"
                return_value.append(ob.oe(**p2))
                p2 = copy.deepcopy(kwargs)
                p2["shape"] = "oobb_cube_center"            
                p2["inclusion"] = mode
                p2["size"] = [3.5, 3.5, height_layer] 
                p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2] + adjuster[1]]        
                #p2["m"] = "#"
                return_value.append(ob.oe(**p2))
                
    return return_value



# hv
def get_oobb_wire_higher_voltage_old(**kwargs):
    kwargs["num_pins"] = 2
    kwargs.update({"polarized": True})
    return get_oobb_wire_generic(**kwargs)
# i2c
def get_oobb_wire_i2c_old(**kwargs):
    kwargs["num_pins"] = 4
    kwargs.update({"polarized": True})
    return get_oobb_wire_generic(**kwargs)

def get_oobb_wire_motor_old(**kwargs):
    kwargs["num_pins"] = 2
    kwargs.update({"polarized": False})
    return get_oobb_wire_generic(**kwargs)



# 2 wire unpolarized 

# space
def get_oobb_wire_spacer_old(**kwargs):
    pos = kwargs.get("pos", [0, 0, 0])    
    kwargs.update({"polarized": False})
    depth = kwargs.get("depth", 3)

    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]
    return_value = []



    return_value = get_oobb_wire_base(**kwargs)
    for mode in modes:
        ##wire back piece
        p2 = copy.deepcopy(kwargs)
        wid = 24
        hei = 24
        depth = depth
        size = [wid, hei, depth]
        x = 21.5
        y = 0
        z = 0 
        pos = [kwargs["pos"][0] + x, kwargs["pos"][1] + y, kwargs["pos"][2] + z]
        p2["shape"] = "rounded_rectangle"
        p2["pos"] = pos
        p2["size"] = size    
        p2["inclusion"] = mode    
        ##wire escape =             
        return_value.append(ob.oe(**p2))

    return return_value


def get_oobb_wire_spacer_long_old(**kwargs):
    pos = kwargs.get("pos", [0, 0, 0])    
    kwargs.update({"polarized": False})
    depth = kwargs.get("depth", 3)

    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]
    return_value = []



    return_value = get_oobb_wire_base(**kwargs)
    for mode in modes:
        ##wire back piece
        p2 = copy.deepcopy(kwargs)
        wid = 36
        hei = 22
        depth = depth
        size = [wid, hei, depth]
        x = 22.5
        y = 0
        z = 0 
        pos = [kwargs["pos"][0] + x, kwargs["pos"][1] + y, kwargs["pos"][2] + z]
        p2["shape"] = "rounded_rectangle"
        p2["pos"] = pos
        p2["size"] = size    
        p2["inclusion"] = mode    
        ##wire escape =             
        return_value.append(ob.oe(**p2))

    return return_value

def get_oobb_wire_spacer_u_old(**kwargs):
    pos = kwargs.get("pos", [0, 0, 0])    
    kwargs.update({"polarized": False})
    depth = kwargs.get("depth", 3)

    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]
    return_value = []



    return_value = get_oobb_wire_base(**kwargs)
    for mode in modes:
        ##wire back piece
        p2 = copy.deepcopy(kwargs)
        wid = 51

        hei = 22
        depth = depth
        size = [wid, hei, depth]
        x = 30
        y = 0
        z = 0 
        pos = [kwargs["pos"][0] + x, kwargs["pos"][1] + y, kwargs["pos"][2] + z]
        p2["shape"] = "rounded_rectangle"
        p2["pos"] = pos
        p2["size"] = size    
        p2["inclusion"] = mode    
        ##wire escape =             
        return_value.append(ob.oe(**p2))

    return return_value




def get_oobb_ziptie(**kwargs):
    modes = ["laser", "3dpr", "true"]
    return_value = []
    clearance = kwargs.get("clearance", False)
    for mode in modes:
        kwargs["shape"] = "oobb_cube_center"
        kwargs["center"] = True
        kwargs["inclusion"] = mode
        kwargs.update(
            {"size": [ob.gv("ziptie_width", mode), ob.gv("ziptie_height", mode), 100]})
        spacing_zt = 7

        p3 = copy.deepcopy(kwargs)
        p3.update({"pos": [kwargs["pos"][0], kwargs["pos"]
                  [1]-spacing_zt/2, kwargs["pos"][2] - 50]})
        return_value.append(ob.oobb_easy(**p3))
        p2 = copy.deepcopy(kwargs)
        p2.update({"pos": [kwargs["pos"][0], kwargs["pos"]
                  [1]+spacing_zt/2, kwargs["pos"][2]-50]})
        return_value.append(ob.oobb_easy(**p2))
        if clearance:
            p4 = copy.deepcopy(kwargs)
            p4.update(
                {"pos": [kwargs["pos"][0], kwargs["pos"][1], kwargs["pos"][2]]})
            p4.update({"size": [ob.gv("ziptie_width", mode), ob.gv(
                "ziptie_height", mode)+spacing_zt, 3], "m": ""})
            return_value.append(ob.oobb_easy(**p4))

    return return_value

###### electronics


def get_oobb_electronics_header_i2d54_20(**kwargs):
    return_value = []

    return return_value

def get_oobb_electronics_socket_i2d54_20(**kwargs):
    return_value = []
    kwargs["pins"] = 20
    return_value = get_oobb_electronics_socket_i2d54(**kwargs)
    return return_value

def get_oobb_electronics_socket_i2d54(**kwargs):
    return_value = []
    pins = kwargs.get("pins", 20)
    clearance = kwargs.get("clearance", True)
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    pos = kwargs.get("pos", [0, 0, 0])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes]
    for mode in modes:
        i2 = ob.gv("i2d54", mode)        
        i2_true = ob.gv("i2d54", "true")        
        width = i2
        ex = 0.5
        if mode == "3dpr":
            ex = 1.2
        height  = ob.gv(f"i2d54x{pins}", mode) + ex #datasheet says 0.5mm extra added more for corners etc
        depth = ob.gv("electronics_socket_i2d54_depth", mode)
        x = pos[0]
        y = pos[1]-pins/2*i2_true + i2_true/2
        z = pos[2]
        zz = kwargs.get("zz", "")
        if zz == "bottom":
            z = z + 0            
        elif zz == "top":
            z = z - depth            
        m = kwargs.get("m", "")
        typ = kwargs.get("type", "p")
        return_value.append(ob.oobb_easy(s="oobb_cube_center", type=typ, inclusion = mode, size = [width, height, depth], pos = [x, y, z], m = m))
    return return_value

        
        
def get_oobb_electronics_mcu_atmega328_shennie(**kwargs):
    _ensure_base()
    part = kwargs.get("part", "all")    

    if part == "all":
        clearance = kwargs.get("clearance", False)
        extra_clearance = 0
        if clearance:
            extra_clearance = 20
        return_value = []
        #add a keying cube 1.2 x 2.8 x 2.5 plus 0.5 at 0,8
        rects = []
                        #extra  height  width  depth    x shift y shift  z shift
        #main middle pieces
            #tall
        rects.append([   -0.2,   38.1,   12.7,    3,       0,       -2.54,       0])
            #wide
        rects.append([   -0.2,   35.56,   17.78,    3,       0,       -1.27,       0])    
        #side pieces
        rects.append([   -0.2,   38.1,   2.54,    3,       -7.62,       0,       0])
        rects.append([   -0.2,   38.1,   2.54,    3,       7.62,       0,       0])
        #top pin well
        rects.append([   0.1,    2.54,   17.78,   3,       0,       20.32,       -3])
        #programming pins well
        rects.append([   0.1,    5.08,   7.62,   3,       0,       19.05,       -3])
        #bottom bin wells
        rects.append([   0.1,    2.54,   5.08,   3,       -8.89,       -20.32,       -3])
        rects.append([   0.1,    2.54,   5.08,   3,       8.89,       -20.32,       -3])
        #wire pass through
        #rects.append([   0,      5,      12,     6,       0,          15.5+6,         0])
        for rect in rects:
            p2 = copy.deepcopy(kwargs)
            extra = rect[0]
            height = rect[1]
            width = rect[2]
            depth = rect[3]
            p2["size"] = [width+extra, height+extra, depth]
            #offset pos for center postion
            p2["pos"] = [p2["pos"][0]+rect[4], p2["pos"][1]+rect[5], p2["pos"][2]+rect[6]]
            return_value.append((get_oobb_cube_center(**p2)))

        holes = []
        pin_size = "m1"
                        #x      y      radius
        holes.append([   -7.62, 20.32, pin_size])
        holes.append([   7.62, 20.32, pin_size])
        holes.append([   -7.62, -20.32, pin_size])
        holes.append([   7.62, -20.32, pin_size])
        holes.append([   0, 7.5, "m10"])
        start_x = -2.54
        start_y = 17.78
        for w in range(0, 3):
            for h in range(0, 2):
                holes.append([start_x+w*2.54, start_y+h*2.54, pin_size])
        
        for hole in holes:
            p2 = copy.deepcopy(kwargs)
            p2["shape"] = "oobb_hole"
            p2["radius_name"] = hole[2]
            p2["pos"] = [p2["pos"][0]+hole[0], p2["pos"][1]+hole[1], p2["pos"][2]]
            return_value.extend(ob.oobb_easy(**p2))



        

    return return_value

def get_oobb_electronics_microswitch_standard(**kwargs):
    _ensure_base()
    return_value = []
    clearance = kwargs.get("clearance", False)
    rot_z = kwargs.get("rotZ", 0)
    kwargs["rotZ"] = 0
    m = kwargs.get("m", "")
    nut_offset = kwargs.get("nut_offset", -3)
    pos = kwargs.get("pos", [0, 0, 0])
    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_cube_center"
    extra = 0
    if rot_z == 0:
        p2["size"] = [28+extra, 16+extra, 10+extra]
    if rot_z == 90:
        p2["size"] = [16+extra, 28+extra, 10+extra]
    p2["pos"] = [p2["pos"][0], p2["pos"][1], p2["pos"][2]]
    return_value.append((get_oobb_cube_center(**p2)))        
    holes = []
    if rot_z == 0:
        shift_x = 11.1
        shift_y = 5.15
    elif rot_z == 90:
        shift_x = 5.15
        shift_y = 11.1
    holes.append([shift_x, shift_y])
    holes.append([-shift_x, -shift_y])
    holes.append([-shift_x, shift_y])
    holes.append([shift_x, -shift_y])
    for hole in holes:
        x,y = hole
        return_value.extend(ob.oobb_easy(t="n", s="oobb_hole", radius_name="m3", pos=[pos[0]+x,pos[1]+y,0], m=m))
        return_value.extend(ob.oobb_easy(t="n", s="oobb_nut", radius_name="m3", pos=[pos[0]+x,pos[1]+y,nut_offset], m=m))


    return return_value

def get_oobb_electronics_potentiometer_17(**kwargs):
    _ensure_base()
    return get_oobb_electronic_potentiometer_17_mm(**kwargs)



def get_oobb_electronics_pushbutton_11(**kwargs):

    clearance = kwargs.get("clearance", False)
    extra_clearance = 0
    return_value = []
    p2 = copy.deepcopy(kwargs)        
    depth_bottom = 18.5
    p2["r"] = [11/2, 7.5/2, 6/2]
    p2["h"] = [depth_bottom, 6, 6]
    return_value.extend((get_cylinders(**p2)))
    return_value = ob.shift(return_value, [0, 0, -depth_bottom])

    return return_value



###### tools

    
def get_oobb_tool_allen_key_set_small_generic(**kwargs):
    return_value = []
    spacing = 5
    start_offset = -spacing * 5/2 + spacing/2
    
    p2 = copy.deepcopy(kwargs)
    p2["pos"] = [p2["pos"][0]+start_offset+spacing*0, p2["pos"][1], p2["pos"][2]]    
    return_value.extend(get_oobb_tool_allen_key_hex_m1d5_small_generic(**p2))

    p2 = copy.deepcopy(kwargs)
    p2["pos"] = [p2["pos"][0]+start_offset+spacing*1, p2["pos"][1], p2["pos"][2]- 5*1]
    return_value.extend(get_oobb_tool_allen_key_hex_m2_small_generic(**p2))
    
    p2 = copy.deepcopy(kwargs)
    p2["pos"] = [p2["pos"][0]+start_offset+spacing*2, p2["pos"][1], p2["pos"][2]- 5*2]
    return_value.extend(get_oobb_tool_allen_key_hex_m2d5_small_generic(**p2))
    
    p2 = copy.deepcopy(kwargs)
    p2["pos"] = [p2["pos"][0]+start_offset+spacing*3, p2["pos"][1], p2["pos"][2]- 5*3]
    return_value.extend(get_oobb_tool_allen_key_hex_m3_small_generic(**p2))

    p2 = copy.deepcopy(kwargs)
    p2["pos"] = [p2["pos"][0]+start_offset+spacing*4, p2["pos"][1], p2["pos"][2]- 5*4]
    return_value.extend(get_oobb_tool_allen_key_hex_m4_small_generic(**p2))

    return return_value

def get_oobb_tool_allen_key_hex_m1d5_small_generic(**kwargs):
    return_value = []
    p2 = copy.deepcopy(kwargs)
    p2["hex_r"] = "m2d5"
    return_value.extend(get_oobb_tool_allen_key_generic(**p2))
    return return_value

def get_oobb_tool_allen_key_hex_m2_small_generic(**kwargs):
    return_value = []
    p2 = copy.deepcopy(kwargs)
    p2["hex_r"] = "m3"
    return_value.extend(get_oobb_tool_allen_key_generic(**p2))
    return return_value

def get_oobb_tool_allen_key_hex_m2d5_small_generic(**kwargs):
    return_value = []
    p2 = copy.deepcopy(kwargs)
    p2["hex_r"] = "m3d5"
    return_value.extend(get_oobb_tool_allen_key_generic(**p2))
    return return_value

def get_oobb_tool_allen_key_hex_m3_small_generic(**kwargs):
    return_value = []
    p2 = copy.deepcopy(kwargs)
    p2["hex_r"] = "m4"
    return_value.extend(get_oobb_tool_allen_key_generic(**p2))
    return return_value

def get_oobb_tool_allen_key_hex_m4_small_generic(**kwargs):
    return_value = []
    p2 = copy.deepcopy(kwargs)
    p2["hex_r"] = "m5"
    return_value.extend(get_oobb_tool_allen_key_generic(**p2))
    return return_value

def get_oobb_tool_allen_key_hex_m5_small_generic(**kwargs):
    return_value = []
    p2 = copy.deepcopy(kwargs)
    p2["hex_r"] = "m6"
    return_value.extend(get_oobb_tool_allen_key_generic(**p2))
    return return_value

def get_oobb_tool_allen_key_generic(**kwargs):
    hex_r = kwargs.get("hex_r", 1.5)
    extra = kwargs.get("extra", "cutout")
    hex_dic = {}
    
    
    if extra == "cutout":
        clearance_up = 10
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [ob.gv(f"hole_radius_{hex_r}", "3dpr")]
        p2["h"] = [100]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value

def get_oobb_tool_electronics_crimp_jst_wc_260(**kwargs):
    ##### rotation doesn't work
    ##too thin needs resizing
    return_value = []

    kwargs["rotX"] = 0

    pos = kwargs.get("pos", [0, 0, 0])
    kwargs["pos"] = [pos[0], pos[1], pos[2]]  

    total_depth = 17

    #add wide cube
    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_cube_center"
    width = 39
    height = 75
    depth = 14
    p2["size"] = [width, height, depth]    
    p2["pos"] = [pos[0], pos[1]+height/2, pos[2]]
    return_value.append(ob.oe(**p2))
     #add narrow cube
    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_cube_center"
    width = 18
    height = 60
    depth = 21
    p2["size"] = [width, height, depth]    
    p2["pos"] = [pos[0], pos[1]+height/2+15, pos[2]]
    return_value.append(ob.oe(**p2))

    return return_value


def get_oobb_tool_electronics_crimp_molex_11010185(**kwargs):
    ##### rotation doesn't work
    ##too thin needs resizing
    return_value = []

    kwargs["rotX"] = 0

    pos = kwargs.get("pos", [0, 0, 0])
    kwargs["pos"] = [pos[0], pos[1], pos[2]]  

    total_depth = 17

    #add wide cube
    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_cube_center"
    width = 65
    height = 200
    depth = 18
    p2["size"] = [width, height, depth]    
    p2["pos"] = [pos[0], pos[1]+height/2, pos[2]]
    return_value.append(ob.oe(**p2))
   

    return return_value


def get_oobb_tool_marker_black_sharpie(**kwargs):
    return get_oobb_tool_marker_sharpie(**kwargs)

def get_oobb_tool_marker_bic_clear_lid(**kwargs):
    extra = kwargs.get("extra", "cutout")
    if extra == "cutout":
        clearance_up = 10
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [10/2,12/2]
        p2["h"] = [112, 35]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value

def get_oobb_tool_marker_german_big(**kwargs):
    extra = kwargs.get("extra", "cutout")
    if extra == "cutout":
        clearance_up = 10
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [20/2]
        p2["h"] = [115]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value

def get_oobb_tool_marker_ikea_mala(**kwargs):
    extra = kwargs.get("extra", "cutout")
    if extra == "cutout":
        clearance_up = 10
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [14/2]
        p2["h"] = [136.5]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value

def get_oobb_tool_marker_patterned_thicker(**kwargs):
    extra = kwargs.get("extra", "cutout")
    if extra == "cutout":
        clearance_up = 10
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [12/2]
        p2["h"] = [140]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value

def get_oobb_tool_marker_sharpie(**kwargs):
    extra = kwargs.get("extra", "cutout")
    if extra == "cutout":
        clearance_up = 10
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [13/2]
        p2["h"] = [137]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value

def get_oobb_tool_measure_caliper_digital_150_mm_length_mitutoyo_mit500_196_30(**kwargs):
    kwargs["w"] = 78
    kwargs["h"] = 78
    kwargs["depth"] = 16
    pos = kwargs.get("pos", [0, 0, 0])
    pos[0] += 0
    pos[1] += -10
    pos[2] += 0
    return get_oobb_tool_wrench(**kwargs)

def get_oobb_tool_measure_tape_measure_5000_mm_length_stanley_1_30_696(**kwargs):
    kwargs["w"] = 78
    kwargs["h"] = 74
    kwargs["depth"] = 42
    pos = kwargs.get("pos", [0, 0, 0])
    pos[0] += 0
    pos[1] += 0
    pos[2] += 0
    return get_oobb_tool_wrench(**kwargs)


def get_oobb_tool_knife_utility_17_mm_blade(**kwargs):
    return get_oobb_tool_knife_exacto_17mm_black(**kwargs)

def get_oobb_tool_knife_exacto_17mm_black(**kwargs):    
    kwargs["w"] = 17
    kwargs["h"] = 160
    kwargs["depth"] = 27.5        
    return get_oobb_tool_wrench(**kwargs)


def get_oobb_tool_knife_utility_blade_disposal_can_olfa_dc_3(**kwargs):
    
    pos = kwargs.get("pos", [0, 0, 0])

    pos1 = copy.deepcopy(pos)

    kwargs["pos"] = pos1
    kwargs["depth"] = 27.5
    kwargs["radius"] = 69 / 2

    return get_tool_cylinder_horizontal(**kwargs)

def get_oobb_tool_pliers_needlenose_generic_130_mm_blue(**kwargs):
    extra = kwargs.get("extra", "cutout")
    return_value = []
    if extra == "cutout":
        
        p2 = copy.deepcopy(kwargs)
        p2["depth"] = 10
        p2["w"] = [17, 17, 46, 50]
        p2["h"] = [0, 54, 93, 125]
        return_value.append(get_tool_generic(**p2))
        
    return return_value

def get_oobb_tool_screwdriver_driver_bit(**kwargs):
    extra = kwargs.get("extra", "cutout")
    
    if extra == "cutout":
        
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [8/2]
        p2["h"] = [60]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value


def get_oobb_tool_screwdriver_hex_m1d5_wera_60_mm(**kwargs):
    kwargs["wera_r"] = 3.5/2
    return get_oobb_tool_screwdriver_hex_wera_60_mm(**kwargs)

def get_oobb_tool_screwdriver_hex_m2_wera_60_mm(**kwargs):
    kwargs["wera_r"] = 3.5/2
    return get_oobb_tool_screwdriver_hex_wera_60_mm(**kwargs)

def get_oobb_tool_screwdriver_hex_m2d5_wera_60_mm(**kwargs):
    kwargs["wera_r"] = 5/2
    return get_oobb_tool_screwdriver_hex_wera_60_mm(**kwargs)
    

def get_oobb_tool_screwdriver_hex_wera_60_mm(**kwargs):
    wera_r = kwargs.get("wera_r", 1.5)
    extra = kwargs.get("extra", "cutout")
    
    if extra == "cutout":
        
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [wera_r, 9]
        p2["h"] = [60, 98]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value

def get_oobb_tool_screwdriver_multi_quikpik_200_mm(**kwargs):
    extra = kwargs.get("extra", "cutout")
    
    if extra == "cutout":
        
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [7.7/2, 11/2,13/2,36/2]
        p2["h"] = [57, 30, 17, 100]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value


def get_oobb_tool_side_cutters_generic_110_mm_red(**kwargs):
    extra = kwargs.get("extra", "cutout")
    return_value = []
    if extra == "cutout":
        
        p2 = copy.deepcopy(kwargs)
        p2["depth"] = 11
        p2["w"] = [11.5, 11.5, 33, 42]
        p2["h"] = [0, 35, 60, 110]
        return_value.append(get_tool_generic(**p2))
        
    return return_value

def get_oobb_tool_timer_80_mm_diameter_30_mm_depth_black(**kwargs):
    
    pos = kwargs.get("pos", [0, 0, 0])

    pos1 = copy.deepcopy(pos)

    kwargs["pos"] = pos1
    kwargs["depth"] = 32
    kwargs["radius"] = 82 / 2

    return get_tool_cylinder_horizontal(**kwargs)

def get_oobb_tool_wire_strippers_generic_120_red(**kwargs):
    extra = kwargs.get("extra", "cutout")
    return_value = []
    if extra == "cutout":
        
        p2 = copy.deepcopy(kwargs)
        p2["depth"] = 11
        p2["w"] = [17, 17, 45, 55]
        p2["h"] = [0, 35, 80, 120]
        return_value.append(get_tool_generic(**p2))
        
    return return_value

def get_oobb_tool_wrench_m7(**kwargs):
    kwargs["w"] = 16
    kwargs["h"] = 110
    kwargs["depth"] = 4.5        
    return get_oobb_tool_wrench(**kwargs)

def get_oobb_tool_wrench_m8(**kwargs):
    kwargs["w"] = 18
    kwargs["h"] = 120
    kwargs["depth"] = 5.5        
    return get_oobb_tool_wrench(**kwargs)

def get_oobb_tool_wrench_m10(**kwargs):
    kwargs["w"] = 23
    kwargs["h"] = 140
    kwargs["depth"] = 7        
    return get_oobb_tool_wrench(**kwargs)

def get_oobb_tool_wrench_m13(**kwargs):
    kwargs["w"] = 28
    kwargs["h"] = 160
    kwargs["depth"] = 8        
    return get_oobb_tool_wrench(**kwargs)

def get_oobb_tool_wrench_m21(**kwargs):
    kwargs["w"] = 44
    kwargs["h"] = 140
    kwargs["depth"] = 10 #7.25 real        
    return get_oobb_tool_wrench(**kwargs)

def get_oobb_tool_wrench(**kwargs):
    extra = kwargs.get("extra", "cutout")
    return_value = []
    depth = kwargs.get("depth", 3)
    w = kwargs.get("w", 11.5)
    w = w/2
    h = kwargs.get("h", 140)
    if extra == "cutout":
        
        p2 = copy.deepcopy(kwargs)
        p2["depth"] = depth
        p2["w"] = [w, w]
        p2["h"] = [0, h]
        return_value.append(get_tool_generic(**p2))
        
    return return_value

#tdpb tools
def get_oobb_tool_tdpb_nozzle_changer(**kwargs):
    extra = kwargs.get("extra", "cutout")
    if extra == "cutout":
        clearance_up = 10
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [12/2]
        p2["h"] = [100]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value

def get_oobb_tool_tdpb_drill_cleaner_m3(**kwargs):
    extra = kwargs.get("extra", "cutout")
    if extra == "cutout":
        clearance_up = 10
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [3.6/2]
        p2["h"] = [100]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value
def get_oobb_tool_tdpb_drill_cleaner_m6(**kwargs):
    extra = kwargs.get("extra", "cutout")
    if extra == "cutout":
        clearance_up = 10
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [6.6/2]
        p2["h"] = [100]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value

def get_oobb_tool_tdpb_glue_stick_prit_medium(**kwargs):
    extra = kwargs.get("extra", "cutout")
    if extra == "cutout":
        clearance_up = 10
        p2 = copy.deepcopy(kwargs)        
        p2["r"] = [28/2]
        p2["h"] = [96]
        return_value = (get_tool_cylinders(**p2))
        
    return return_value


def get_tool_generic(**kwargs):
    depth = kwargs.get("depth", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    w = kwargs.get("w", [0, 0, 0, 0])
    h = kwargs.get("h", [0, 0, 0, 0])
    rotX = kwargs.get("rotX", 0)
    
    p2 = copy.deepcopy(kwargs)
    points = []
    points = get_points_tool_poly(w,h,pos)
    p2["points"] = points
    p2["h"] = depth
    p2["shape"] = "polygon"
    p2["rotX"]  = rotX + 90
    p2["pos"] = [0, depth/2+pos[1], 0]
    return_value = opsc.opsc_easy(**p2)

    return return_value

def get_tool_cylinders(**kwargs):
    return get_cylinders(**kwargs)    



def get_cylinders(**kwargs):
    
    depth = kwargs.get("depth", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    rs = kwargs.get("r", [0, 0, 0, 0])
    hs = kwargs.get("h", [0, 0, 0, 0])
    return_value = []
    zz = 0
    for i in range(len(rs)):
        r = rs[i]
        h = hs[i]    
        p2 = copy.deepcopy(kwargs)
        rotX = kwargs.get("rotX", 0) 
        p2["r"] = r
        #p2["depth"] = h
        p2["h"] = h

        #p2["shape"] = "oobb_cylinder"        
        p2["shape"] = "cylinder"  
        if rotX == 0:      
            p2["pos"][2] = p2["pos"][2] + zz
        elif rotX == -90:
            p2["pos"][1] = p2["pos"][1] + zz
    
        
        #return_value.extend(ob.oe(**p2))
        return_value.append(ob.oe(**p2))
        zz+=h

    return return_value

def get_tool_cylinder_horizontal(**kwargs):
    
    depth = kwargs.get("depth", 3)
    radius = kwargs.get("radius", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    rot = kwargs.get("rot", [0,0,0])

    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "cylinder"
    p3["r"] = radius
    p3["h"] = depth
    pos1 = [pos[0], pos[1], pos[2]]
    p3["pos"] = pos1
    rot1 = copy.deepcopy(rot)
    p3["rot"] = rot1
    p3["m"] = "#"





    return_value = ob.oe(**p3)
    return return_value


def get_points_tool_poly(w,h,pos):
    points = []
    #do a mirrored image of points
    for i in range(len(w)):
        points.append([-w[i]+pos[0], h[i]+pos[2]])
    #go through points in reverse
    for i in range(len(w)-1, -1, -1):
        points.append([w[i]+pos[0], h[i]+pos[2]])
    return points
    


######### oomp items
def get_oobb_oomp_l5(**kwargs):
    return get_oobb_oomp_electronic_led_5_mm(**kwargs)

def get_oobb_oomp_electronic_led_5_mm(**kwargs):        
    p2 = copy.deepcopy(kwargs)        
    p2["r"] = [6/2,5/2]
    p2["h"] = [1, 8]
    return_value = (get_tool_cylinders(**p2))
    return return_value



