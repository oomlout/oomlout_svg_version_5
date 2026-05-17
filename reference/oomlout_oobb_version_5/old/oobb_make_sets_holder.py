def get_holders(size="oobb"):
    hls = []
    
    hls = get_holders_computer(hls)
    hls = get_holders_electronic(hls)
    
    
    # fan

    #      120_mm
    hls.append({"type": "holder", "extra": "fan_120_mm","width": 10, "height": 10, "thickness": 3, "size": size})

    # motor
    #      building_block
    #            large_01
    hls.append({"type": "holder", "extra": "motor_building_block_large_01","width": 5, "height": 3, "thickness": 6, "size": size})
    hls.append({"type": "holder", "extra": "motor_building_block_large_01_bottom","width": 3, "height": 3, "thickness": 42, "size": size})
        #        small_01
    hls.append({"type": "holder", "extra": "motor_building_block_small_01_bottom","width": 3, "height": 3, "thickness": 48, "size": size})


    #       tt_01
    hls.append({"type": "holder", "extra": "motor_tt_01","width": 6, "height": 3, "thickness": 6, "size": size})
    
    #      servo
    #           micro
    hls.append({"type": "holder", "extra": "motor_servo_micro_01","width": 4, "height": 3, "thickness": 3, "size": size})
    
    #           standard
    #                 all
    hls.append({"type": "holder", "extra": "motor_servo_standard_01_all_debug","width": 5, "height": 3, "thickness": 00, "size": size})
    hls.append({"type": "holder", "extra": "motor_servo_standard_01_all_print","width": 5, "height": 3, "thickness": 00, "size": size})
    hls.append({"type": "holder", "extra": "motor_servo_standard_01","width": 5, "height": 3, "thickness": 15, "size": size})
    
    #                 top
    hls.append({"type": "holder", "extra": "motor_servo_standard_01_top","width": 5, "height": 3, "thickness": 9, "size": size})

    #                 bottom    
    hls.append({"type": "holder", "extra": "motor_servo_standard_01_bottom","width": 5, "height": 3, "thickness": 24, "size": size})


    #### stepper nema 17
    thicknesses = [3,6,9]
    for t in thicknesses:
        ##shifted nema 17s    
        hls.append({"type": "holder", "extra": "motor_stepper_nema_17_flat_shifted","width": 5, "height": 3, "thickness": t, "size": size})
        ##shifted nema 17s    
        hls.append({"type": "holder", "extra": "motor_stepper_nema_17_flat_shifted_spacer_10_mm","width": 5, "height": 3, "thickness": t, "size": size})
        ##normal nema 17s
        hls.append({"type": "holder", "extra": "motor_stepper_nema_17_flat","width": 5, "height": 3, "thickness": t, "size": size})

    #      with_encoder
    hls.append({"type": "holder", "extra": "mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible","width": 5, "height": 5, "thickness": 3, "size": size})

    
    # powerbank
    #      anker_323
    hls.append({"type": "holder", "extra": "powerbank_anker_323","width": 7, "height": 13, "thickness": 6, "size": size})


    return hls

def get_holders_computer(hls,size="oobb") :
    hls.append({"type": "holder", "extra": "computer_power_supply_microsoft_surface_docking_station_microsoft_model_1749","width": 11, "height": 6, "thickness": 3, "size": size})
    
    hls.append({"type": "holder", "extra": "computer_power_supply_microsoft_surface_standalone_microsoft_model_1625","width": 9, "height": 6, "thickness": 3, "size": size})

    return hls

def get_holders_electronic(hls,size="oobb"):
    #electronic
        
    #      battery_box_aa_battery_4_cell
    hls.append({"type": "holder", "extra": "electronic_battery_box_aa_battery_4_cell","width": 5, "height": 5, "thickness": 4, "size": size})
    #      button_11
    hls.append({"type": "holder", "extra": "electronic_button_11_mm_panel_mount","width": 3, "height": 3, "thickness": 3, "size": size})
    hls.append({"type": "holder", "extra": "electronic_button_11_mm_panel_mount","width": 3, "height": 3, "thickness": 21, "size": size})
    hls.append({"type": "holder", "extra": "electronic_button_11_mm_panel_mount_x4","width": 3, "height": 3, "thickness": 3, "size": size})
    hls.append({"type": "holder", "extra": "electronic_button_11_mm_panel_mount_x4","width": 3, "height": 3, "thickness": 21, "size": size})
    #      breadboard
    hls.append({"type": "holder", "extra": "electronic_prototyping_breadboard_400_point","width": 6, "height": 8, "thickness": 3, "size": size})

    
    #      mcu
    #hls.append({"type": "holder", "extra": "electronic_mcu_atmega328_shennie","width": 3, "height": 4, "thickness": 6, "size": size})
    #      microswitch_standard
    #hls.append({"type": "holder", "extra": "electronic_microswitch_standard","width": 3, "height": 3, "thickness": 3, "size": size}) 
    #hls.append({"type": "holder", "extra": "electronic_microswitch_standard","width": 3, "height": 3, "thickness": 6, "size": size})            
    #      potentimeter
    #            17_mm
    hls.append({"type": "holder", "extra": "electronic_potentiometer_17_mm","width": 3, "height": 3, "thickness": 12, "size": size})
    hls.append({"type": "holder", "extra": "electronic_potentiometer_17_mm","width": 3, "height": 3, "thickness": 3, "size": size})
    #            stick_single_axis_16_mm
    hls.append({"type": "holder", "extra": "electronic_potentiometer_stick_single_axis_16_mm","width": 3, "height": 3, "thickness": 3, "size": size})
    hls.append({"type": "holder", "extra": "electronic_potentiometer_stick_single_axis_16_mm_arm","width": 3, "height": 1, "thickness": 9, "size": size})
    
    return hls