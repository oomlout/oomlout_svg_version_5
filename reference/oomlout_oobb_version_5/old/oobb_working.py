import oobb
import oobb_base
import oobb_make_sets
import oomB
import oobb_markdown
import oobb_dxf_laser_copy
import copy


def main(**kwargs):
    #filter = "oobb_plate_03_01_03"
    #filter = "oobb_bearing_plate_03_03_12_6705_ex_horn_adapter_screws_sh_motor_servo_standard_01"
    #filter = "oobb_bearing_plate_03_03_12_6704_ex_horn_adapter_screws_sh_motor_servo_standard_01"
    #filter = "oobb_bearing_plate_03_03_12_6705_ex_no_center"
    #filter = "oobb_test_ex_oobb_motor_servo_standard_01"
    #filter = "oobb_holder_05_03_00_ex_motor_servo_standard_01_all_print"
    
    
    
    # bearing plate
    #filter = "bearing_plate"
    #filter = "oobb_bearing_plate_03_03_12_6705"
    #filter = "oobb_bearing_plate_03_03_12_6705_ex_no_center"
    #filter = "oobb_bearing_plate_03_03_12_6705_ex_sandwich_sh_motor_tt_01"
    #filter = "oobb_bearing_plate_03_03_12_6705_ex_horn_adapter_screws_sh_motor_servo_standard_01"
    #filter = "oobb_bearing_plate_03_04_12_606_ex_shifted"
    #filter = "coupler_flanged"
    #filter = "oobb_bearing_plate_03_03_12_6705"
    #filter = "oobb_bearing_plate_03_03_09_6705_ex_minimal"
    #filter = "oobb_bearing_plate_05_05_12_6810_ex_three_quarter"
    #filter = "oobb_bearing_plate_03_03_12_6705_ex_horn_adapter_screws_sh_motor_servo_standard_01"

    # bunting
    #filter = "bunting"
    #filter = "oobb_bunting_alphabet_13"

    # circle
    #filter = "circle"
    #filter = "doughnut"
    #filter = "oobb_circle_05_03_ex_doughnut_2"
    #filter = "circle_1d5"
    #filter = "circle_03_03"
    #filter = "circle_03_03_sh"


    # electronic
    #filter = "holder_03_03_03_ex_electronic_potentiometer"
    #filter = "holder_03_03_03_ex_electronic_button_11_mm_panel_mount"

    # gear
    #filter = "gear"
    #filter = "gear_01_03_12_ex"
    #filter = "gear_09_06_ex_72_teeth"
    #filter = "gear_02_06_ex_16_teeth_sh_motor_servo_standard_01"
    #filter = "motor_gearmotor_tt_motor_01"
    #filter = "_8_teeth"
    #filter = "oobb_gear_01_06_ex_8_teeth_sh_motor_tt_01"

    # holder    
    #filter = "oobb_holder"
    #filter = "oobb_holder_06_03_06_ex_motor_tt_01"
    #filter = "oobb_holder_05_03_06_ex_motor_stepper_nema_17_flat_shifted"
    #filter = "oobb_holder_05_05_04_ex_electronic_battery_box_aa_battery_4_cell"
    #filter = "nema_17"
    #filter = "oobb_holder_05_03_09_ex_motor_stepper_nema_17_flat"
    #filter = "ex_motor_stepper_nema_17_flat"
    #filter = "computer_power_supply_microsoft_surface_standalone_microsoft_model_1625"

    #
    # filter = "electronic_battery_box_aa_battery_4_cell"

    # mounting_plate
    #filter = "mounting_plate"
    #filter = "netgear_5_port_gigabit_switch_gs105v5"
    #filter = "electrolama_a_lot_of_jacks"
    #filter = "electronic_breakout_board_servo_tester_32_mm_width_28_mm_height_hw_141"

    # other
    #filter = "_other"
    #filter = "bolt_stacker"
    #filter = "oobb_other_01_06_03_ex_bolt_stacker"
    #filter = "oobb_other_02_02_29_ex_corner_cube"
    #filter = "ptfe"

    # plate
    #filter = "ninety_degree"
    # filter = "ex_u"
    #filter = "ex_label"
    #filter = "oobb_plate_05_05_15_ex_u_double"
    #filter = "oobb_plate_07_01_14_ex_ninety_degree"
    #filter = ["ex_l","_u"]
    #filter = "oobb_plate_07_01_14_ex_ninety_degree"
    #filter = "oobb_plate_03_03_44_ex_ninety_degree"
    #filter = "oobb_plate_10_06_03"
    #filter = "oobb_plate_16_01_14_ex_ninety_degree"
    #filter = "kallax"

    # pulley
    #filter = "pulley"
    #filter = "pulley_gt2_01_06_ex_20_teeth_shield_sh_motor_n20"
    #filter = "72_teeth_shield_sh_m6_grub"
    #filter = "20_teeth_shield_sh_motor_n20"
    #filter = "oobb_pulley_gt2"
    #filter = "_6705_ex_72_teeth_shield"
    #filter = "40_teeth_shield"

    # shaft
    #filter = "shaft"

    # tray
    #filter = "tray"
    #filter = "tray_03_05_90"
    #filter = "tray_vertical"
    filter = "tray_vertical_9_width_1_height_30_mm_depth"


    # wheel
    #filter = "twenty_twenty_aluminium_extrusion"
    #filter = "oobb_wheel_24_10d2_696_ex_bearing_twenty_twenty_aluminium_extrusion"
    #filter = "oobb_wheel_01_06_or_314"
    #filter = "oobb_wheel_1d75_7d5_606"
    #filter = "oobb_wheel_05_09_606_ex_no_tire"
    #filter = "oobb_wheel_29_15_606_ex_bearing_twenty_twenty_aluminium_extrusion"

    # wire
    #filter = "wire"
    
    #filter = "oobb_wire_03_03_12_ex_basic"
    #filter = "oobb_wire_03_03_04_ex_basic"
    #filter = "basic_basic_basic_higher_voltage"
    #filter = "oobb_wire_03_03_09_ex_higher_voltage_motor_stepper"

    #oobb_servo_holder
    #filter = []
    #filter.append("oobb_holder_05_03_09_ex_motor_servo_standard_01") 
    #filter.append("oobb_holder_05_03_15_ex_motor_servo_standard_01")
    #filter.append("oobb_bearing_plate_03_03_12_6705_ex_no_center")
    #filter.append("oobb_bearing_plate_03_03_12_6705_ex_horn_adapter_screws_sh_motor_servo_standard_01")
    #filter.append("oobb_servo_holder_05_03_24_ex_motor_servo_standard_01")
    
    # test
    #filter = "oobb_test_ex_oobb_wire"
    #filter = "oobb_test_ex_motor_tt_01"
    #filter = "oobb_test_ex_oobb_nut"
    #filter = "oobb_test_ex_oobb_shape_slot"
    #filter = "test"
    #filter = "oobb_test_0d1_ex_hole_sh_9d5"
    #filter = "oobb_test_0d1_ex_hole_sh_6"
    
    #filter = "tool"
    #filter = "tool_screwdriver_hex_wera_60_mm_x5"
    #filter = "tool_marker_sharpie_x6"
    #filter = "tape_measure"
    #filter = "tool_knife_utility_blade_disposal_can_olfa_dc_3"
    #filter = "tool_timer_80_mm_diameter_30_mm_depth_black"
    #filter = "caliper_digital"

    #filter = ""


    oobb_make_sets.make_all(filter=filter)

    

    
    save_type = "none"
    #save_type = "laser"
    #save_type = "3dpr"    
    #save_type = "all"

    overwrite = True
    #overwrite = False
    
    
    #modes = ["laser", "3dpr", "true"]
    #modes = ["3dpr", "laser", "true"]
    modes = ["3dpr"]
    #modes = ["laser"]
    oobb_base.build_things(overwrite=overwrite, filter=filter, save_type=save_type, modes=modes)

    #dump = False
    dump = True
    if dump:
        oobb_base.dump("json")
        oobb_base.dump("folder")

    generate_release = False
    #generate_release = True
    if generate_release:
        print("generate_release")
        import action_generate_release_3d_printable
        action_generate_release_3d_printable.main()
        import action_generate_release_laser_cut
        action_generate_release_laser_cut.main()


    #copy_files = True
    copy_files = False
    if copy_files:
        oobb_base.dump("pickle")
        copy_files_routine()
        
        
def copy_files_routine(**kwargs):
        oobb_markdown.make_markdown()
        oobb_dxf_laser_copy.folders_to_folder_dxf()
        oobb_dxf_laser_copy.folders_to_folder_stl()
        oobb_dxf_laser_copy.folders_to_folder_svg()
        oobb_dxf_laser_copy.folders_to_folder_png()
        oobb_dxf_laser_copy.folders_to_folder_all()
    

if __name__ == "__main__":
    main()
    pass
