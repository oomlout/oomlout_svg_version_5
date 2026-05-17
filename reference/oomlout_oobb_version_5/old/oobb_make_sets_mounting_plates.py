import copy

def get_mounting_plates(size="oobb"):
    mounting_plates = []
    mounting_plates.extend(get_mounting_plates_aliexpress())
    mounting_plates.extend(get_mounting_plates_bigtreetech())
    mounting_plates.extend(get_mounting_plates_cytron())
    mounting_plates.extend(get_mounting_plates_dangerousprototypes())
    mounting_plates.extend(get_mounting_plates_electrolama())
    mounting_plates.extend(get_mounting_plates_pimoroni())
    mounting_plates.extend(get_mounting_plates_raspberry_pi())
    mounting_plates.extend(get_mounting_plates_other())

    return mounting_plates

def get_mounting_plates_aliexpress(size="oobb"):
    mounting_plates = []
    # company : aliexpress 

    #      dc to dc converter
    #            step up step down xl6009 48 mm width 25 mm height
    #       motor controller
    mounting_holes = []
    mounting_holes.append({"x": 18, "y": -9})
    mounting_holes.append({"x": -18, "y": 9})
    pl = {"type": "mounting_plate", 
          "name": "aliexpress_dc_to_dc_converter_xl6009_48_mm_width_25_mm_height",
          "width": 5, 
          "height": 4, 
          "thickness": 3,           
          "radius_hole": "m3", 
          "size": size,
          "mounting_holes": mounting_holes}    
    mounting_plates.append(pl)
    pl2 = copy.deepcopy(pl)
    pl2["type"] = "mounting_plate_top"    
    pl2["height"] = pl2["height"]-1
    pl2["width"] = pl2["width"]-1
    mounting_plates.append(pl2)


    #       i2c
    #            servo driver pca9685
    pl = {"type": "mounting_plate", 
          "name": "aliexpress_i2c_servo_driver_pca9685", 
          "width": 6, 
          "height": 4, 
          "thickness": 3, 
          "width_mounting": 56,
          "height_mounting": 19, 
          "radius_hole": "m2d5", 
          "size": size}
    mounting_plates.append(pl)
    pl2 = copy.deepcopy(pl)
    pl2["type"] = "mounting_plate_top"    
    pl2["height"] = pl2["height"]-1
    pl2["width"] = pl2["width"]-1
    mounting_plates.append(pl2)
    
    #       motor controller
    pl = {"type": "mounting_plate", 
          "name": "aliexpress_motor_controller_speed", 
          "width": 4, 
          "height": 4, 
          "thickness": 3, 
          "width_mounting": 26,
          "height_mounting": 26, 
          "radius_hole": "m3", 
          "size": size}
    mounting_plates.append(pl)
    pl = copy.deepcopy(pl)
    pl["type"] = "mounting_plate_u"
    mounting_plates.append(pl)
    pl = copy.deepcopy(pl)
    pl["type"] = "mounting_plate_side"
    mounting_plates.append(pl)

    #      usb
    #            usb_micro_breakout
    mounting_holes = []
    mounting_holes.append({"x": 4.25, "y": -2.5})
    mounting_holes.append({"x": -4.25, "y": -2.5})
    pl = {"type": "mounting_plate", 
          "name": "aliexpress_usb_micro_breakout_01",
          "width": 3, 
          "height": 3, 
          "thickness": 3,           
          "radius_hole": "m3", 
          "size": size,
          "mounting_holes": mounting_holes,
          "extra": "clearance_hole_10_mm_10_mm_0_mm_6_mm"}    
    mounting_plates.append(pl)
    
    pl2 = copy.deepcopy(pl)
    pl2["type"] = "mounting_plate_top"    
    pl2["height"] = pl2["height"]-1
    pl2["width"] = pl2["width"]-1
    pl2.pop("extra", "")
    mounting_plates.append(pl2)

    # oomp

    #       breakout_board

    #             servo_tester
    board = "electronic_breakout_board_servo_tester_32_mm_width_28_mm_height_hw_141"
    mounting_holes = []
    mounting_holes.append({"x": -13.5, "y": 11})
    mounting_holes.append({"x": 6.5, "y": -11})
    mounting_plates.append({"type": "mounting_plate", "width": 4, "height": 4, "thickness": 3, "mounting_holes": mounting_holes, "radius_hole": "m2_5", "name": board, "size": size})

    
    return mounting_plates

def get_mounting_plates_bigtreetech(size="oobb"):
    mounting_plates = []
    # company : bigtree 
    #       octopus driver board
    pl = { "type": "mounting_plate",
          "name": "bigtreetech_octopus", 
          "width": 13, 
          "height": 9, 
          "thickness": 3, 
          "width_mounting": 150,
          "height_mounting": 90, 
          "radius_hole": "m3", 
          "size": size}
    mounting_plates.append(pl)
    
    return mounting_plates

def get_mounting_plates_cytron(size="oobb"):
    mounting_plates = []
    # company : cytron
    #      maker_pi_rp2040
    pl = { "type": "mounting_plate",
            "name": "cytron_maker_pi_rp2040",
            "width": 8,
            "height": 6,
            "thickness": 3,
            "width_mounting": 82,
            "height_mounting": 58,
            "radius_hole": "m3",
            "size": size}
    mounting_plates.append(pl)
    pl3 = copy.deepcopy(pl)
    pl3["type"] = "mounting_plate_top"
    pl3["width"] = pl3["width"]-1
    mounting_plates.append(pl3)

    return mounting_plates

def get_mounting_plates_dangerousprototypes(size="oobb"):
    mounting_plates = []
    # company : dangerousprototypes
    #      bus pirate 5
    pl = { "type": "mounting_plate",
            "name": "dangerousprototypes_bus_pirate_version_5",
            "width": 6,
            "height": 6,
            "thickness": 3,
            "width_mounting": 52,
            "height_mounting": 52,
            "radius_hole": "m3",
            "size": size}
    mounting_plates.append(pl)
    pl3 = copy.deepcopy(pl)
    pl3["type"] = "mounting_plate_top"
    pl3["width"] = pl3["width"]-1
    mounting_plates.append(pl3)

    return mounting_plates

def get_mounting_plates_electrolama(size="oobb"):
    mounting_plates = []
    # electrolama
    #      hub
    mounting_holes = []
    mounting_holes.append({"x": -32.5, "y": 10})
    mounting_holes.append({"x": 31.5, "y": 10})
    mounting_holes.append({"x": -24.5, "y": -10})
    mounting_holes.append({"x": 31.5, "y": -10})
    mounting_plates.append({"type": "mounting_plate", "width": 7, "height": 4, "thickness": 3, "mounting_holes": mounting_holes, "radius_hole": "m3", "name": "electrolama_basic_hub", "size": size})
    
    pl = { "type": "mounting_plate",
            "name": "electrolama_a_lot_of_jacks",
            "width": 6,
            "height": 6,
            "thickness": 3,
            "width_mounting": 30,
            "height_mounting": 30,
            "radius_hole": "m2",
            "size": size}
    mounting_holes = []
    mounting_holes.append({"x": 0, "y": 21.5})
    mounting_holes.append({"x": 0, "y": -21.5})
    mounting_holes.append({"x": 23, "y": 0})
    mounting_holes.append({"x": -23, "y": 0})
    mounting_plates.append({"type": "mounting_plate", 
                            "width": 6, 
                            "height": 6, 
                            "thickness": 3, 
                            "mounting_holes": mounting_holes, "radius_hole": "m2", 
                            "name": "electrolama_a_lot_of_jacks", 
                            "size": size})
    mounting_plates.append(pl)

    return mounting_plates

def get_mounting_plates_other(size="oobb"):
    mounting_plates = []
    # netgear
    #      hub
    mounting_holes = []
    mounting_holes.append({"x": -17.5, "y": 0})
    mounting_holes.append({"x": 27.5, "y": 0})
    mounting_plates.append({"type": "mounting_plate", "width": 9, "height": 9, "thickness": 3, "mounting_holes": mounting_holes, "standoff": False, "radius_hole": "m3", "name": "netgear_5_port_gigabit_switch_gs105v5", "size": size})

    return mounting_plates

def get_mounting_plates_pimoroni(size="oobb"):
    mounting_plates = []
    # company : dangerousprototypes
    #      bus pirate 5
    pl = { "type": "mounting_plate",
            "name": "pimoroni_pim613_servo_2040",
            "width": 6,
            "height": 5,
            "thickness": 3,
            "width_mounting": 56.5,
            "height_mounting": 36.5,
            "radius_hole": "m2d5",
            "size": size}
    mounting_plates.append(pl)
    pl3 = copy.deepcopy(pl)
    pl3["type"] = "mounting_plate_top"
    pl3["width"] = pl3["width"]-1
    mounting_plates.append(pl3)

    return mounting_plates

def get_mounting_plates_raspberry_pi(size="oobb"):
    mounting_plates = []
    # company : dangerousprototypes
    #      bus pirate 5
    pl = { "type": "mounting_plate",
            "name": "raspberry_pi_pico",
            "width": 5,
            "height": 3,
            "thickness": 3,
            "width_mounting": 47,
            "height_mounting": 11.5,
            "radius_hole": "m2",
            "size": size}
    mounting_plates.append(pl)
    pl3 = copy.deepcopy(pl)
    pl3["type"] = "mounting_plate_top"
    pl3["width"] = pl3["width"]-1
    mounting_plates.append(pl3)

    return mounting_plates

