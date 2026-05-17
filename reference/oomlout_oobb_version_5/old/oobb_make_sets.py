
#import oobb_get_items_oobb
import oobb_base

try:
    from oobb_arch.catalog.part_set_discovery import build_part_set_lookup
except Exception:
    build_part_set_lookup = None


_DISCOVERED_PART_SET_LOOKUP = None


def _get_discovered_part_set_lookup():
    global _DISCOVERED_PART_SET_LOOKUP
    if _DISCOVERED_PART_SET_LOOKUP is None and build_part_set_lookup is not None:
        try:
            _DISCOVERED_PART_SET_LOOKUP = build_part_set_lookup()
        except Exception:
            _DISCOVERED_PART_SET_LOOKUP = {}
    return _DISCOVERED_PART_SET_LOOKUP or {}


def _get_discovered_set_items(set_name, size="oobb", **kwargs):
    lookup = _get_discovered_part_set_lookup()
    discovered = lookup.get(set_name)
    if discovered is None:
        return None
    try:
        return discovered.items_fn(size=size, **kwargs)
    except Exception:
        return None


def get_set_items_discovered(set_name, size="oobb", **kwargs):
    """Compatibility bridge for legacy getters to consume discovered part sets."""

    return _get_discovered_set_items(set_name=set_name, size=size, **kwargs)


def make_all(filter=""):
    # typs = ["bps","jas","mps","pls","nuts","screws_countersunk","tests","zts"]
    # add orings make a nice summary page maybe tables of details add 2020 maybe
    typs = ["bearing_plates", "bearing_circles", "buntings", "circles", "gears", "holders", "jacks", "jigs", "mounting_plates", "plates", "pulleys", "shaft_couplers","shafts", "soldering_jigs", "smd_magazines", "tool_holders", "trays", "ziptie_holders", "nuts", "wires", "wheels", "screws", "bearings", "nuts", "tests", "others"]
    #typs = ["bearing_plates", "bearing_circles", "mounting_plates", "trays", "tests","plates"]
   
    all_things = []
    discovered_lookup = _get_discovered_part_set_lookup()

    for type in typs:
        discovered = discovered_lookup.get(type)
        if discovered is not None:
            try:
                all_things.extend(discovered.items_fn(size="oobb"))
                continue
            except Exception:
                pass

        func = globals()["get_"+type]
        all_things.extend(func())


    for thing in all_things:
        thing2 = oobb_base.get_default_thing(**thing) # hack to get the id early
        
        if not isinstance(filter, list):
            filter = [filter]
        
        if any(f in thing2["id"] for f in filter):
            print(f"adding {thing2['id']}")
            type = thing
            thing_2 = oobb_base.get_thing_from_dict(thing)
            oobb_base.add_thing(thing_2)


# oobb makes



def get_bearing_plates(size="oobb"):
    bps = []
    bps.append({"type": "bearing_plate", "width": 3, "height": 3, "thickness": 12, "bearing": "606","size": size})
    bps.append({"type": "bearing_plate", "width": 3, "height": 5, "thickness": 12, "bearing": "606","size": size})
    bps.append({"type": "bearing_plate", "width": 3, "height": 4, "thickness": 12, "bearing": "606","extra": "shifted","size": size})
    
    

    # 6704
    bps.append({"type": "bearing_plate", "width": 3, "height": 3, "thickness": 12, "bearing": "6704","size": size})
    bps.append({"type": "bearing_plate_shim", "thickness": 2, "bearing": "6704", "size": size})
    bps.append({"type": "bearing_plate", "width": 3, "height": 3, "thickness": 12, "bearing": "6704", "size": size, "shaft": "motor_gearmotor_01"})
    bps.append({"type": "bearing_plate", "width": 3, "height": 3, "thickness": 12, "bearing": "6704", "size": size, "shaft": "motor_servo_micro_01"})
    bps.append({"type": "bearing_plate", "width": 3, "height": 3, "thickness": 12, "bearing": "6704", "size": size, "shaft": "motor_servo_standard_01", "extra": "horn_adapter_printed"})
    bps.append({"type": "bearing_plate", "width": 3, "height": 3, "thickness": 12, "bearing": "6704", "size": size, "shaft": "motor_servo_standard_01", "extra": "horn_adapter_screws"})
    bps.append({"type": "bearing_plate", "width": 3, "height": 3, "thickness": 12, "bearing": "6704", "size": size, "shaft": "motor_building_block_large_01"})
    bps.append({"type": "bearing_plate", "width": 3, "height": 3, "thickness": 12, "bearing": "6704", "size": size, "shaft": "motor_n20"})

    # 6705
    b = "6705"
    w = 3
    h = 3
    
    t = 9    
    bps.append({"type": "bearing_plate", "width": w, "height": h, "thickness": t, "bearing": b,"size": size})
    bps.append({"type": "bearing_plate", "width": w, "height": h, "thickness": t, "bearing": b,"size": size, "extra":"missing_middle_3_mm"})
    bps.append({"type": "bearing_plate", "width": w, "height": h, "thickness": t, "bearing": b,"size": size, "extra":"minimal_missing_middle_3_mm"})

    t = 12
    bps.append({"type": "bearing_plate", "width": w, "height": h, "thickness": t, "bearing": b,"size": size})
    bps.append({"type": "bearing_plate", "width": w, "height": h, "thickness": t, "bearing": b,"size": size, "extra":"missing_middle_3_mm"})
    
    
    bps.append({"type": "bearing_plate", "width": w, "height": h, "thickness": t, "bearing": b,"extra": "no_center", "size": size})
    bps.append({"type": "bearing_plate", "width": w, "height": h, "thickness": t, "bearing": b, "size": size, "shaft": "motor_servo_standard_01", "extra": "horn_adapter_screws"})
    bps.append({"type": "bearing_plate", "width": w, "height": h, "thickness": t, "bearing": b, "size": size, "shaft": "motor_tt_01", "extra":"sandwich"})
    bps.append({"type": "bearing_plate", "width": w, "height": h, "thickness": t, "bearing": b, "size": size, "shaft": "motor_tt_01", "extra":"removable"})
    bps.append({"type": "bearing_plate", "width": w, "height": h, "thickness": t, "bearing": b, "size": size, "shaft": "coupler_flanged"})
    
    # 6810
    b = "6810"
    bps.append({"type": "bearing_plate", "width": 7, "height": 5, "thickness": 12, "bearing": b,"size": size})
    bps.append({"type": "bearing_plate", "width": 5, "height": 5, "thickness": 12, "bearing": b,"size": size})
    bps.append({"type": "bearing_plate", "width": 5, "height": 5, "thickness": 12, "bearing": b,"size": size, "extra":"three_quarter"})

    return bps

def get_bearing_circles(size="oobb"):
    discovered = get_set_items_discovered("bearing_circles", size=size)
    if discovered is not None:
        return discovered

    bcs = []
    bcs.append({"type": "bearing_circle", "diameter": 3, "thickness": 12, "bearing": "606","size": size})

    return bcs

def get_buntings(size="oobb"):
    items = []
    
    #letters = "HELEN"
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".lower()
    #letters = "AZO"
    widths = [3,5,7,13]
    #widths = [13]

    for width in widths:
        for letter in letters:
            items.append({"type": "bunting_alphabet", "width": width, "thickness": 1, "extra":letter, "size": size})
  
    return items



def get_circles(size="oobb"):
    circles = []
    circle_size = [1.5,3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
    for s in circle_size:
        circles.append({"type": "circle", "diameter": s, "thickness": 3, "size": size})
    
    #extra thicknesses
    circle_size = [1.5,3, 5]
    thicknesses = [6, 9, 12, 15]
    for s in circle_size:
        for t in thicknesses:
            circles.append({"type": "circle", "diameter": s, "thickness": t, "size": size})

    #extra thin ones
    circle_size = [1.5]
    thicknesses = [0.5, 0.75, 1.5]
    for s in circle_size:
        for t in thicknesses:
            circles.append({"type": "circle", "diameter": s, "thickness": t, "size": size})


    shafts = ["coupler_flanged"]
    circle_size = [3, 5, 7]
    for shaft in shafts:
        for s in circle_size:
            circles.append({"type": "circle", "diameter": s, "thickness": 3, "size": size, "shaft":shaft})


    #circles.append({"type": "circle", "diameter": 1.5, "thickness": 12, "extra":"nut_m6", "size": size})


    #circles.append({"type": "circle_captive", "diameter": 3, "thickness": 9, "shaft":"electronic_potentiometer_17_mm", "size": size})
    #circles.append({"type": "circle_captive", "diameter": 1.5, "thickness": 6, "shaft":"electronic_potentiometer_17_mm", "size": size})
    
    #circles.append({"type": "circle_captive", "diameter": 3, "thickness": 9, "shaft":"motor_gearmotor_01", "size": size})
    #circles.append({"type": "circle_captive", "diameter": 1.5, "thickness": 9, "shaft":"motor_gearmotor_01", "size": size})

    #doughnuts
    circles = []
    circle_size = [5, 7, 9, 11, 13, 15, 17, 19, 21]
    doughnuts = [2.5,3,5]
    for s in circle_size:
        for d in doughnuts:
            if s > d:
                circles.append({"type": "circle", "diameter": s, "thickness": 3, "size": size,"extra":f"doughnut_{d}"})

    return circles

def get_gears(size="oobb"):
    gears = []
    
    #extra thicknesses
    gear_size = [1, 1.5,2,3,4,5,7,9]
    thicknesses = [3,6]
    shafts = ["", "m3", "electronic_potentiometer_17_mm", "motor_n20", "motor_servo_standard_01","motor_tt_01"]
    

    for shaft in shafts:
            for s in gear_size:
                for t in thicknesses:   
                                 
                    teeth = f"{s * 8}_teeth"
                    if isinstance(s, list):
                        teeth = []
                        for s2 in s:
                            teeth.append(f"{s2 * 8}_teeth")                        
                    gears.append({"type": "gear", "diameter": s, "thickness": t, "size": size, "extra":teeth, "shaft": f"{shaft}"})
    
    gear_size = [2,3,4,5,7,9]
    shafts = ["m6_grubscrew_m3"]
    thicknesses = [9]
    for shaft in shafts:
            for s in gear_size:
                for t in thicknesses:                
                    teeth = f"{s * 8}_teeth"
                    gears.append({"type": "gear", "diameter": s, "thickness": t, "size": size, "extra":teeth, "shaft": f"{shaft}"})

    # double stacks
    gears.append({"type": "gear", "diameter": [1,3], "thickness": 12, "size": "oobb", "extra":["8_teeth","24_teeth"], "shaft": "m6"})


    return gears

def get_holders(size="oobb"):
    import oobb_make_sets_holder
    return oobb_make_sets_holder.get_holders()
    


def get_jacks(size="oobb"):
    jas = []

    types = ["jack", "jack_basic"]

    for typ in types:
        for wid in range(3, 10+1):
            #jas.append({"type": typ, "width": wid, "height": 1, "thickness": 12, "size": size})
            pass

    #jas.append({"type": "jack", "width": 3, "height": 2,"thickness": 12, "size": size})
    #jas.append({"type": "jack", "width": 5, "height": 2,"thickness": 12, "size": size})
    #jas.append({"type": "jack", "width": 3, "height": 3,"thickness": 12, "size": size})

    #jas.append({"type": "jack_basic", "width": 2, "height": 1,"thickness": 12, "size": size})
    #jas.append({"type": "jack_basic", "width": 1, "height": 1,"thickness": 12, "size": size})

    return jas

def get_jigs(size="oobb"):
    jgs = []

    jgs.append({"type": "jig", "extra": "tray_03_03","width": 5, "height": 5, "thickness": 6, "size": size})    
    jgs.append({"type": "jig", "extra": "screw_sorter_m3_03_03","width": 3, "height": 3, "thickness": 15, "size": size})
            


    return jgs


def get_mounting_plates(size="oobb"):
    import oobb_make_sets_mounting_plates
    mounting_plates = oobb_make_sets_mounting_plates.get_mounting_plates(size="oobb")

    return mounting_plates

def get_others(size="oobb"):
    ots = []
        
    # timing_belt

    #      clamp_gt2
    ots.append({"type": "other", "extra": "timing_belt_clamp_gt2","width": 2.5, "height": 1.5, "thickness": 14, "size": size})
    ots.append({"type": "other", "extra": "timing_belt_clamp_gt2","width": 2.5, "height": 1.5, "thickness": 6, "size": size})

    #      corner_cube
    ots.append({"type": "other", "extra": "corner_cube","width": 2, "height": 2, "thickness": 29, "size": size})

    #      bolt_stacker
    ots.append({"type": "other", "extra": "bolt_stacker","diameter": 1.5,  "thickness": 24, "size": size})

    ots.append({"type": "other", "extra": "bolt_stacker","width": 1,  "height":6, "thickness": 3, "size": size})

    #      ptfe_tube_holder
    heights = [7,5,3]
    shafts = ["m6", "quarter_inch_pipe_thread"]
    for h in heights:
        for s in shafts:
            ots.append({"type": "other", "extra": "ptfe_tube_holder","width": 1,  "height":h, "thickness": 14, "size": size, "shaft":s})
            ots.append({"type": "other", "extra": "ptfe_tube_holder_ninety_degree","width": 1,  "height":h, "thickness": 14, "size": size, "shaft":s})


    return ots


def get_plates(size="oobb"):
    plates = []
    
    
    #sizes = ["oobb", "oobe"]
    sizes = ["oobb"]
    
    for size in sizes:
        #all 3m thicks 1x1 to 10x10
        for wid in range(1, 11):
            for hei in range(1, 11):
                if wid >= hei:
                    plates.append({"type": "plate", "width": wid,
                                "height": hei, "thickness": 3, "size": size})

        #all thicknesses 1x1
        depths = []
        for i in range(1, 34):
            depths.append(i*3)
        for dep in depths:
            plates.append({"type": "plate", "width": 1, "height": 1,
                    "thickness": dep, "size": size})
        
        #various plates that also have extra thicknesses
        premo_plates = []
        premo_plates.append([2,1])
        premo_plates.append([3,1])
        premo_plates.append([4,1])
        premo_plates.append([5,1])
        premo_plates.append([7,1])
        premo_plates.append([9,1])
        premo_plates.append([10,1])
        premo_plates.append([11,1])
        premo_plates.append([12,1])
        premo_plates.append([13,1])
        premo_plates.append([15,1])
        premo_plates.append([17,1])
        premo_plates.append([19,1])
        premo_plates.append([20,1])
        premo_plates.append([2,1])
        premo_plates.append([3,3])
        premo_plates.append([5,5])
        premo_plates.append([6,3])
        premo_plates.append([5,3])
        premo_thicknesses = [6, 9, 12, 15,21,30]
        for plate in premo_plates:
            for thickness in premo_thicknesses:
                plates.append({"type": "plate", "width": plate[0], "height": plate[1],
                    "thickness": thickness, "size": size})

        #one widers
        thicknesses = [3, 6, 9, 12]
        for thickness in thicknesses:
            for len in range(2, 35):
                plates.append({"type": "plate", "width": len, "height": 1,
                            "thickness": thickness, "size": size})

        #03s, 05s
        widths = [7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
        heights = [3,5]
        for w in widths:
            for h in heights:
                plates.append({"type": "plate", "width": w, "height": h,
                        "thickness": 3, "size": size})
        
        #squares
        widths = range(10,21)
        for w in widths:
            plates.append({"type": "plate", "width": w, "height": w,
                    "thickness": 3, "size": size})
        
        # larger plates of desire
        plates.append({"type": "plate", "width": 15, "height": 9,
                    "thickness": 3, "size": size})

        
        # extra fifteens
        widths = range(1,21)        
        for w in widths:
                if w < 15:
                    plates.append({"type": "plate", "width": 15, "height": w,
                        "thickness": 3, "size": size})
                else:
                    plates.append({"type": "plate", "width": w, "height": 15,
                        "thickness": 3, "size": size})
        
        plates.append({"type": "plate", "width": 15, "height": 14,
                    "thickness": 3, "size": size})
        plates.append({"type": "plate", "width": 15, "height": 13,
                    "thickness": 3, "size": size})
        plates.append({"type": "plate", "width": 15, "height": 12,
                    "thickness": 3, "size": size})
        plates.append({"type": "plate", "width": 15, "height": 11,
                    "thickness": 3, "size": size})

    size = "oobb"
    plates.append({"type": "plate", "width": 28, "height": 20,
                "thickness": 3, "size": size, "extra": "paper_sheet_a3"})
    plates.append({"type": "plate", "width": 20, "height": 14,
                "thickness": 3, "size": size, "extra": "paper_sheet_a4"})
    plates.append({"type": "plate", "width": 14, "height": 10,
                "thickness": 3, "size": size, "extra": "paper_sheet_a5"})
    plates.append({"type": "plate", "width": 10, "height": 7,
                "thickness": 3, "size": size, "extra": "paper_sheet_a6"})
    plates.append({"type": "plate", "width": 25, "height": 20,
                "thickness": 3, "size": size, "extra": "furniture_shelf_ikea_kallax"})

    """
    size = "oobe"
    thicknesses = [3]
    for thickness in thicknesses:
        plates.append({"type": "plate", "width": 28, "height": 20, "thickness": thickness, "size": size, "name": "oobe_warehouse_box"})
        plates.append({"type": "plate", "width": 21, "height": 21, "thickness": thickness, "size": size, "name": "oobe_shelf_tray"})
    """

    #add oobe holes to all oobb plates
    for plate in plates:
        #add "both_holes" True to all plates
        if plate["size"] == "oobb":
            plate["both_holes"] = True

    

    size = "oobb"

    #non both_holes ones
    #gorm plates
    #plates.append({"type": "plate", "width": 7, "height": 4, "thickness": 3, "extra":"gorm", "size": size})
    #plates.append({"type": "plate", "width": 5, "height": 2, "thickness": 3, "extra":"gorm", "size": size})

    #ninety_degree plates    
    max = 20
    for i in range(2,max):
        plates.append({"type": "plate", "width": i, "height": 1, "thickness": 14, "extra":"ninety_degree", "size": size})
    
    cubes = []
    cubes.append([2,2,14])
    cubes.append([3,3,14])
    cubes.append([4,4,14])
    cubes.append([5,5,14])
    cubes.append([2,2,29])
    cubes.append([3,3,29])
    cubes.append([3,3,44])
    
    for cube in cubes:
        width = cube[0]
        height = cube[1]
        thickness = cube[2]
        plates.append({"type": "plate", "width": width, "height": height, "thickness": thickness, "extra":"ninety_degree", "size": size})


    # l
    thicknesses = [3,6,9,12,15]
    sizes = []
    sizes.append([3,3])
    sizes.append([5,2])
    for thick in thicknesses:
        for siz in sizes:
            plates.append({"type": "plate", "width": siz[0], "height": siz[1], "thickness": thick, "extra":"l", "size": size})
    
    # t
    thicknesses = [3,6,9,12,15]
    thicknesses = [3]
    sizes = []
    sizes.append([3,2])    
    sizes.append([3,3])  
    sizes.append([5,2])  
    sizes.append([5,5])  
    for thick in thicknesses:
        for siz in sizes:
            plates.append({"type": "plate", "width": siz[0], "height": siz[1], "thickness": thick, "extra":"t", "size": size})

    # u
    thicknesses = [3,6,9,12,15]
    sizes = []
    sizes.append([3,3])
    sizes.append([5,3])
    sizes.append([5,5])
    typs = ["u","u_double"]
    for thick in thicknesses:
        for siz in sizes:
            for typ in typs:
                plates.append({"type": "plate", "width": siz[0], "height": siz[1], "thickness": thick, "extra":typ, "size": size})


    
    # slip_center and slip_end
    widths = [3,5, 7]
    thicknesses = [8.5]
    extras = ["slip_center", "slip_end"]
    for width in widths:
        for thickness in thicknesses:
            for extra in extras:
                pass
                #plates.append({"type": "plate", "width": width, "height": 1, "thickness": thickness, "extra":extra, "size": size})

    #plates.append({"type": "plate", "width": 3, "height": 3, "thickness": thickness, "extra":"slip_corner", "size": size})

    # labels only the top row of holes
    # t
    thicknesses = [3]
    sizes = []
    sizes.append([3,2])    
    sizes.append([3,3])  
    sizes.append([5,2])  
    sizes.append([5,3]) 
    sizes.append([7,3]) 
    sizes.append([5,5])  
    sizes.append([7,5])
    sizes.append([9,5])
    for thick in thicknesses:
        for siz in sizes:
            plates.append({"type": "plate", "width": siz[0], "height": siz[1], "thickness": thick, "extra":"label", "size": size})

    return plates

def get_pulleys(size="oobb"):
    pulleys = []
    
    #extra thicknesses
    pulley_size = [16,20,24,30,36,40,48,60,72,144]    
    thicknesses = [6,9]
    shafts = ["", "m3", "electronic_potentiometer_17_mm", "motor_n20", "motor_servo_standard_01","motor_tt_01"]
    shields = ["_shield", ""]

    for shaft in shafts:
        for shield in shields:
            for s in pulley_size:
                for t in thicknesses:                
                    pulleys.append({"type": "pulley_gt2", "thickness": t, "size": size, "extra":f"{s}_teeth{shield}", "shaft":shaft})

    pulley_size = [60,72,144]    
    thicknesses = [6,9]
    shafts = ["m6_grubscrew_m3"]
    shields = ["_shield"]

    for shaft in shafts:
        for shield in shields:
            for s in pulley_size:
                for t in thicknesses:                
                    pulleys.append({"type": "pulley_gt2", "thickness": t, "size": size, "extra":f"{s}_teeth{shield}", "shaft":shaft})

    #bearing cores
    pulley_size = [72]    
    bearings = ["6705"]
    shields = ["_shield", "_shield_double"]
    t = 6
    for bearing in bearings:
        for s in pulley_size:
            for shield in shields:
                pulleys.append({"type": "pulley_gt2", "thickness": t, "size": size, "extra":f"{s}_teeth{shield}", "bearing":bearing})


    return pulleys


def get_shafts(size="oobb"):
    shafts = []
    thinesses = [0, 0.5, 1, 3, 3.5, 4, 6, 9, 12, 15]
    extras = ["","small", "countersunk", "countersunk_small", "nut", "nut_small", "washer"]
    for extra in extras:
        for dep in thinesses:
            shafts.append({"type": "shaft", "thickness": dep, "size": size, "extra": extra})
    

    return shafts

def get_smd_magazines(size="oobb"):
    magazines = []
    
    sizes = [2,3,4,5,7,9]
    #sizes = [3]
    
    thicknesses = []
    wids = [8,12,16]
    this = [1.5,2,3,4]
    #this = [1.5]
    for wid in wids:        
        for thi in this:
            thicknesses.append({"thickness": wid + 2, "extra": thi, "name":f"{wid}_mm_tape_width_{str(thi).replace('.','_')}_mm_tape_thickness"})
    
    
    

    for size in sizes:
        magazines.append({"type": "smd_magazine_lid", 
                        "width": size, 
                        "height": size,                        
                        "size": "oobb"})
        for thickness in thicknesses:
            magazines.append({"type": "smd_magazine", 
                          "width": size, 
                          "height": size,
                          "thickness": thickness["thickness"], 
                          "name" : thickness["name"], 
                          "extra": thickness["extra"],
                          "size": "oobb"})
    
    #5 x 5 16 width 8mm thickness
    size = 5
    wid = 16
    thi = 8
    thickness = {"thickness": wid + 2, "extra": thi, "name":f"{wid}_mm_tape_width_{str(thi).replace('.','_')}_mm_tape_thickness"}
    magazines.append({"type": "smd_magazine", 
                          "width": size, 
                          "height": size,
                          "thickness": thickness["thickness"], 
                          "name" : thickness["name"], 
                          "extra": thickness["extra"],
                          "size": "oobb"})

    #full reel        
    magazines.append({"type": "smd_magazine", 
                          "width": 13, 
                          "height": 13,
                          "thickness": 14, 
                          "name" : "8_mm_tape_width_on_10_mm_reel_1_5_mm_tape_thickness", 
                          "extra": 1.5,
                          "size": "oobb"})

    magazines.append({"type": "smd_magazine_refiller", 
                          "width": 3,                           
                          "size": "oobb"})
    magazines.append({"type": "smd_magazine_refiller", 
                          "width": 3,
                          "extra": "big",                           
                          "size": "oobb"})

    widths = [3,5]
    thicknesses = [8,12]
    for width in widths:
        for thickness in thicknesses:
            label_length = 26
            if width == 5:
                label_length = 36
            magazines.append({"type": "smd_magazine_label_holder", 
                          "width": width,
                          "thickness": thickness +2,
                          "name": f"{thickness}_mm_tape_width_{thickness}_mm_x_{label_length}_mm_label",                           
                          "size": "oobb"})
    
    widths = [4,5,7,9,13]
    for width in widths:
        magazines.append({"type": "smd_magazine_joiner", 
                    "width": width,
                    "thickness": 9,                    
                    "size": "oobb"})
    
    return magazines


def get_shaft_couplers(size="oobb"):
    couplers = []
    size = "oobb"
    couplers.append({"type": "shaft_coupler", "diameter": 2, "thickness": 9,  "size": size})
    
    return couplers

def get_soldering_jigs(size="oobb"):
    sjs = []
    
    #sjs.append({"type": "soldering_jig", "extra": "electronic_mcu_pi_pico_socket", "width": 3, "height": 5, "thickness": 9, "size": size})
    
    return sjs


def get_tool_holders(size="oobb"):
    tool_holders = []
    size = "oobb"
    tool_holders.append({"type": "tool_holder", "width": 7, "height": 10,  "thickness": 66, "extra": "tool_holder_basic", "size": size})


    #C:\DB\Dropbox\bbbb_product_working\tool\tool_holder

    tools = []

    extra_thick = 2

    tools.append(["tool_pliers_needlenose_generic_130_mm_blue",5,5,10+extra_thick])
    
    ## screwdriver
    tools.append(["tool_screwdriver_hex_wera_60_mm_x4",7,5,18+extra_thick])  
    tools.append(["tool_screwdriver_hex_wera_60_mm_x5",9,5,18+extra_thick])  
    tools.append(["tool_screwdriver_hex_wera_60_mm_x2",5,5,18+extra_thick])  
    tools.append(["tool_screwdriver_hex_m1d5_wera_60_mm",3,5,18+extra_thick])  
    tools.append(["tool_screwdriver_hex_m2_wera_60_mm",3,5,18+extra_thick])  
    tools.append(["tool_screwdriver_hex_m2d5_wera_60_mm",3,5,18+extra_thick])
    tools.append(["tool_screwdriver_multi_quikpik_200_mm_knife",5,5,36+extra_thick]) 
    tools.append(["tool_screwdriver_driver_bit",3,3,8+extra_thick])
    tools.append(["tool_screwdriver_driver_bit_x4",5,3,8+extra_thick])
    tools.append(["tool_screwdriver_driver_bit_x6",7,3,8+extra_thick])
    tools.append(["tool_screwdriver_driver_bit_x8",9,3,8+extra_thick])
    tools.append(["tool_screwdriver_hex_key_set_small",5,5,6+extra_thick])
    tools.append(["tool_screwdriver_hex_key_set_small_reverse",5,5,6+extra_thick])

    tools.append(["tool_marker_sharpie",3,5,13+extra_thick])
    tools.append(["tool_marker_sharpie_x2",5,5,13+extra_thick])
    tools.append(["tool_marker_sharpie_x5",8,5,13+extra_thick])
    tools.append(["tool_marker_sharpie_x6",9,5,13+extra_thick])

    tools.append(["tool_marker_bic_clear_lid",3,5,9+extra_thick])
    tools.append(["tool_marker_bic_clear_lid_x6",8,5,9+extra_thick])

    tools.append(["tool_marker_german_big",3,5,20+extra_thick])
    tools.append(["tool_marker_german_big_x4",8,5,20+extra_thick])

    tools.append(["tool_marker_ikea_mala",3,5,14+extra_thick])
    tools.append(["tool_marker_ikea_mala_x5",8,5,14+extra_thick])

    tools.append(["tool_marker_patterned_thicker",3,5,12+extra_thick])
    tools.append(["tool_marker_patterned_thicker_x6",8,5,12+extra_thick])


    #tools.append(["tool_knife_exacto_17mm_black",3,5,12]) # too thick
    tools.append(["tool_side_cutters_generic_110_mm_red",5,5,11+extra_thick])
    tools.append(["tool_wire_strippers_generic_120_red",5,5,11+extra_thick])
    tools.append(["tool_wrench_m7",3,5,4.5+extra_thick])
    tools.append(["tool_wrench_m8",3,5,5.5+extra_thick])
    tools.append(["tool_wrench_m10",3,5,7+extra_thick])
    tools.append(["tool_wrench_m10_x2",5,5,7+extra_thick])
    tools.append(["tool_wrench_m10_x3",7,5,7+extra_thick])
    tools.append(["tool_wrench_m10_x4",9,5,7+extra_thick])
    tools.append(["tool_wrench_m13",3,5,8+extra_thick])
    tools.append(["tool_wrench_m21",5,5,10+extra_thick])
    
    tools.append(["tool_knife_exacto_17mm_black",3,5,27.5+extra_thick])
    tools.append(["tool_knife_utility_17_mm_blade",3,5,27.5+extra_thick])
    tools.append(["tool_knife_utility_blade_disposal_can_olfa_dc_3",5,3,27.5+extra_thick])
    

    tools.append(["tool_measure_tape_measure_5000_mm_length_stanley_1_30_696",7,3,42+extra_thick])
    tools.append(["tool_measure_caliper_digital_150_mm_length_mitutoyo_mit500_196_30",7,6,16+extra_thick])

    tools.append(["tool_timer_80_mm_diameter_30_mm_depth_black",7,3,32+extra_thick])

    #tdpb tools
    tools.append(["tool_tdpb_nozzle_changer",3,5,12+extra_thick])
    tools.append(["tool_tdpb_drill_cleaner_m3",3,5,15+extra_thick])
    tools.append(["tool_tdpb_drill_cleaner_m6",3,5,15+extra_thick])
    tools.append(["tool_tdpb_glue_stick_prit_medium_knife",5,5,28+extra_thick])
    tools.append(["tool_tdpb_glue_stick_prit_medium",4,5,28+extra_thick])

    #specialty tools
    #tools.append(["tool_electronic_crimp_jst_wc_260",5,5,24+extra_thick])
    #tools.append(["tool_electronic_crimp_molex_11010185",7,5,18+extra_thick])

    for tool in tools:
        tool_holders.append({"type": "tool_holder_vertical", "width": tool[1], "height": tool[2],  "thickness": tool[3], "extra": tool[0], "size": size})
    return tool_holders

def get_trays(size="oobb"):
    trays = []

    ts = []    
    trays_all = []

    wids = 15 + 1
    heis = 15 + 1
    wids = list(range(1,wids))
    wids.append(1.5)
    for wid in wids:
        for hei in range(1,heis):
            #don't add duplicates
            if [hei,wid] not in ts:
                ts.append([wid,hei])
                trays_all.append([wid,hei])
            else:
                trays_all.append([wid,hei])
    ts.append([3,1.5])    
    ts.append([2,2.5])
    ts.append([3,2.5])
    ts.append([4,2.5])
    ts.append([5,2.5])
    ts.append([6,2.5])
    ts.append([7,2.5])
    ts.append([8,2.5])
    """
    ts.append([3,3])
    """
    thicknesses = [9, 12, 15, 18, 21,24,27,30,60,90]
    for tray in ts:
        #trays.append({"type": "tray_lid", "width": tray[0], "height": tray[1], "thickness": 2, "size": size})
        #trays.append({"type": "tray_lid_thin", "width": tray[0], "height": tray[1], "thickness": 4, "size": size})
        #trays.append({"type": "tray_lid_thin_spin", "width": tray[0], "height": tray[1], "thickness": 4, "size": size})
        for thickness in thicknesses:
            trays.append({"type": "tray", "width": tray[0], "height": tray[1], "thickness": thickness, "size": size})            
            #trt thin trays for faster printing
            trays.append({"type": "tray_thin", "width": tray[1], "height": tray[0], "thickness": thickness, "size": size})
            #trts thin trays for faster printing with a screw holder
            #trays.append({"type": "tray_thin_spin", "width": tray[1], "height": tray[0], "thickness": thickness, "size": size})

    for tray in trays_all:
        for thickness in thicknesses:
            #trv vertical ones with oobb added for mounting on a wall
            trays.append({"type": "tray_vertical", "width": tray[1], "height": tray[0], "thickness": thickness, "size": size})

    return trays

def get_wheels(size="oobb"):
    wheels = []
    types = [["wheel",6],["wheel",9],["wheel",15]]
    types = [["wheel",6]]
    for t in types:
        type, thickness = t
        wheels.append({"type": type, "thickness": thickness, "oring_type":"314", "size": size})                
        #wheels.append({"type": type, "thickness": thickness, "oring_type":"319", "size": size})
        #wheels.append({"type": type, "thickness": thickness, "oring_type":"323", "size": size})
        #wheels.append({"type": type, "thickness": thickness, "oring_type":"327", "size": size})
        #wheels.append({"type": type, "thickness": thickness, "oring_type":"333", "size": size})
        #wheels.append({"type": type, "thickness": thickness, "oring_type":"339", "size": size})
    

    wheels.append({"type": "wheel", "diameter":3, "thickness": 9, "bearing":"606", "size": size})
    wheels.append({"type": "wheel", "diameter":3, "thickness": 9, "bearing":"606", "size": size, "extra":"no_tire"})    
    wheels.append({"type": "wheel", "diameter":5, "thickness": 9, "bearing":"606", "size": size})
    wheels.append({"type": "wheel", "diameter":5, "thickness": 9, "bearing":"606", "size": size, "extra":"no_tire"})
    wheels.append({"type": "wheel", "diameter":1.75, "thickness": 7.5, "bearing":"606", "size": size})

    wheels.append({"type": "wheel", "thickness": 10.2, "diameter":24, "extra": "bearing_twenty_twenty_aluminium_extrusion" ,"bearing" : "696", "size": size})
    wheels.append({"type": "wheel", "thickness": 15, "diameter":29, "extra": "bearing_twenty_twenty_aluminium_extrusion" ,"bearing" : "606", "size": size})

    
    wheels.append({"type": "wheel", "thickness": 12+3, "diameter":24, "extra": "bearing_twenty_twenty_aluminium_extrusion" ,"bearing" : "606", "size": size})

    #make both_holes true for all
    for wheel in wheels:
        wheel["both_holes"] = True


    return wheels


def get_wires(size="oobb"):
    wis = []
    
    extra_mms = ["", "_extra_mm"]
    
    for extra_mm in extra_mms:
        thicknesses = [2.54,4]
        widths = [3]
        extras = ["motor","basic","higher_voltage","i2c","motor_stepper"]
        #extras = ["basic"]
        for thickness in thicknesses:        
            for width in widths:
                for extra in extras:
                    wis.append({"type": "wire", "extra": f"{extra}{extra_mm}", "thickness": thickness, "width": width, "height": 3, "size": size})
        
        #spacer    
        thicknesses = [3,6,9,12]
        heights = [3]
        for height in heights:
            for thickness in thicknesses:
                wis.append({"type": "wire", "extra": f"spacer{extra_mm}", "thickness": thickness, "width": 3, "height": 2, "size": size})  
                wis.append({"type": "wire", "extra": f"spacer_long{extra_mm}", "thickness": thickness, "width": 3, "height": 2, "size": size}) 
                wis.append({"type": "wire", "extra": f"spacer_u{extra_mm}", "thickness": thickness, "width": 3, "height": 2, "size": size})                    
        
        
        
    extra = ["motor", "basic"]
    wis.append({"type": "wire", "extra": extra, "thickness": 6, "width": 3, "height": 3, "size": size})
    
    extra = ["higher_voltage", "motor_stepper"]
    wis.append({"type": "wire", "extra": extra, "thickness": 6, "width": 3, "height": 3, "size": size}) 
    
    extra = ["higher_voltage", "higher_voltage"]
    wis.append({"type": "wire", "extra": extra, "thickness": 6, "width": 3, "height": 3, "size": size}) 

    extra = ["basic", "basic", "motor"]    
    wis.append({"type": "wire", "extra": extra, "thickness": 9, "width": 3, "height": 3, "size": size})  
    
    extra = ["basic","basic","basic","basic"]
    wis.append({"type": "wire", "extra": extra, "thickness": 12, "width": 3, "height": 3, "size": size})          
    
    extra = ["basic","basic","basic","higher_voltage"]
    wis.append({"type": "wire", "extra": extra, "thickness": 12, "width": 3, "height": 3, "size": size})  

    #stepper motor driver
    extra = ["higher_voltage", "basic", "basic", "motor_stepper"]
    wis.append({"type": "wire", "extra": extra, "thickness": 12, "width": 3, "height": 3, "size": size})
            


        

    return wis

def get_ziptie_holders(size="oobb"):

    zts = []

    zts.append({"type": "ziptie_holder_jack", "width": 1, "thickness": 12, "size": size})
    zts.append({"type": "ziptie_holder_jack", "width": 1, "height": 2,
               "thickness": 12, "size": size})
    zts.append({"type": "ziptie_holder_jack", "width": 2, "thickness": 12, "size": size})
    zts.append({"type": "ziptie_holder_jack", "width": 2, "height": 2,
               "thickness": 12, "size": size})
    zts.append({"type": "ziptie_holder_jack", "width": 2, "height": 3,
               "thickness": 12, "size": size})
    zts.append({"type": "ziptie_holder_jack", "width": 3, "thickness": 12, "size": size})

    zts.append({"type": "ziptie_holder", "width": 2, "height": 3,
               "thickness": 6, "size": size})
    zts.append({"type": "ziptie_holder", "width": 2, "height": 4,
               "thickness": 6, "size": size})
    zts.append({"type": "ziptie_holder", "width": 2, "height": 5,
               "thickness": 6, "size": size})

    return zts

# other makes


def get_bearings():
    bearings = []
    bearing_names = ['6701', '6702', '6703', '6704', '6705', '6706', '6707', '6800', '6801', '6802', '6803', '6804', '6805', '6806', '6807', '6808',
                     '6809', '6810', '6811', '6812', '6813', '6814', '6815', '6816', '6817', '6818', '6819', '6820', '6821', '6822', '6824', '6826', '6828', '6830']

    for bearing in bearing_names:
        bearings.append(
            {"type": "bearing", "bearing_name": bearing, "size": "hardware"})

    return bearings


def get_nuts():
    nuts = []
    nut_sizes = ["m1d5", "m2", "m3", "m4", "m5", "m6", "m8", "m10", "m12"]
    # nut_sizes = ["m10", "m12"]
    for nut_size in nut_sizes:
        nuts.append(
            {"type": "nut", "radius_name": nut_size, "size": "hardware"})

    standoff_lengths = [6, 8, 10, 12, 15, 20, 25, 30]
    standoff_radiuses = ["m3"]
    for standoff_radius in standoff_radiuses:
        for standoff_length in standoff_lengths:
            nuts.append({"type": "standoff", "radius_name": standoff_radius,
                        "depth": standoff_length, "size": "hardware"})

    threaded_insert_radiuses = ["m3"]
    for threaded_insert_radius in threaded_insert_radiuses:
        nuts.append({"type": "threaded_insert",
                    "radius_name": threaded_insert_radius, "size": "hardware"})

    return nuts


def get_screws():
    screws = []
    sizes = {}
    sizes["m3"] = [8, 10, 12, 16, 18, 20, 25, 30, 35, 40]
    for size in sizes:
        for depth in sizes[size]:
            screws.append({"type": "screw_countersunk",
                          "radius_name": size, "depth": depth, "size": "hardware"})
            screws.append({"type": "screw_socket_cap",
                          "radius_name": size, "depth": depth, "size": "hardware"})

    sizes = {}
    lengths = [6, 12, 16, 18, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    sizes["m5"] = lengths
    sizes["m6"] = lengths
    for size in sizes:
        for depth in sizes[size]:
            screws.append({"type": "bolt", "radius_name": size,
                          "depth": depth, "size": "hardware"})

    sizes = {}
    sizes["m2"] = [6, 8, 10, 12]
    for size in sizes:
        for depth in sizes[size]:
            screws.append({"type": "screw_self_tapping",
                          "radius_name": size, "depth": depth, "size": "hardware"})
            

    

    return screws


def get_tests():
    tests = []

    # gear test
    tests.append({"type": "test", "size": "oobb", "extra": "gear"})

    # hole test
    shafts = [9.5, 6]
    for s in shafts:
        tests.append({"type": "test", "size": "oobb", "extra": "hole", "shaft":s, "bearing":0.1 })

    # motor test#
    
    #     motor_gearmotor_tt_motor_01
    tests.append({"type": "test", "size": "oobb", "extra": "motor_tt_01_shaft"})
    
    #     motor_gearmotor_tt_motor_01
    tests.append({"type": "test", "size": "oobb", "extra": "motor_tt_01"})
    
    #      motor_n20
    tests.append({"type": "test", "size": "oobb", "extra": "motor_n20_shaft"})

    #       servo test
    tests.append({"type": "test", "size": "oobb", "extra": "oobb_motor_servo_standard_01"})
    
    # nut test
    tests.append({"type": "test", "size": "oobb", "extra": "oobb_nut"})
    

    # rotation test
    tests.append({"type": "test", "size": "oobb", "extra": "rotation"})
    
    
    # screw test
    tests.append({"type": "test", "size": "oobb", "extra": "oobb_screw_countersunk"})
    tests.append({"type": "test", "size": "oobb", "extra": "oobb_screw_socket_cap"})
    tests.append({"type": "test", "size": "oobb", "extra": "oobb_screw_self_tapping"})
    
    # shape tests
    tests.append({"type": "test", "size": "oobb", "extra": "oobb_shape_slot"})

    # wire test
    tests.append({"type": "test", "size": "oobb", "extra": "oobb_wire"})

    return tests

    for thing in things:
        oobb_base.add_thing(thing)
