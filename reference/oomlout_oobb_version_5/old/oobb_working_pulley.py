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
    
    #filter = "tray_03_03"
    
    # circle
    #filter = "circle_1d5"

    # electronic
    #filter = "holder_03_03_03_ex_electronic_potentiometer"
    #filter = "holder_03_03_03_ex_electronic_button_11_mm_panel_mount"

    # gear
    #filter = "gear"
    #filter = "gear_02_03"
    #filter = "test_ex_gear"


    # holder
    #filter = "oobb_wire_03_03_09_ex_motor_basic"

    # mounting_plate
    #filter = "netgear_5_port_gigabit_switch_gs105v5"

    # plate
    #filter = "ninety_degree"
    #filter = "oobb_plate_07_01_14_ex_ninety_degree"
    #filter = ["ex_l","_u"]

    # pulley
    filter = "pulley"
    #filter = "pulley_gt2_03_06_ex_72_teeth_shield"
    #filter = "40_teeth_shield_sh_motor_servo"
    #filter = "12_teeth"

    # wheel
    #filter = "twenty_twenty_aluminium_extrusion"

    # wire
    #filter = "oobb_wire_03_03_12_ex_basic"
    #filter = "oobb_wire"

    #oobb_servo_holder
    #filter = []
    #filter.append("oobb_holder_05_03_09_ex_motor_servo_standard_01") 
    #filter.append("oobb_holder_05_03_15_ex_motor_servo_standard_01")
    #filter.append("oobb_bearing_plate_03_03_12_6705_ex_no_center")
    #filter.append("oobb_bearing_plate_03_03_12_6705_ex_horn_adapter_screws_sh_motor_servo_standard_01")
    #filter.append("oobb_servo_holder_05_03_24_ex_motor_servo_standard_01")
    
    # test
    #filter = "oobb_test_ex_oobb_wire"
    #filter = "test"

    #ilter = ""


    oobb_make_sets.make_all(filter=filter)

    oobb_base.dump("json")
    oobb_base.dump("folder")

    save_type = "none"
    #save_type = "laser"
    #save_type = "3dpr"
    save_type = "all"

    #overwrite = True
    overwrite = False
    
    modes = ["laser", "3dpr", "true"]
    #modes = ["3dpr"]
    oobb_base.build_things(overwrite=overwrite, filter=filter, save_type=save_type, modes=modes)

    #copy_files = True
    copy_files = False
    if copy_files:
        copy_files()
        
def copy_files(**kwargs):
        oobb_markdown.make_markdown()
        oobb_dxf_laser_copy.folders_to_folder_dxf()
        oobb_dxf_laser_copy.folders_to_folder_stl()
        oobb_dxf_laser_copy.folders_to_folder_svg()
        oobb_dxf_laser_copy.folders_to_folder_png()
        oobb_dxf_laser_copy.folders_to_folder_all()
    

if __name__ == "__main__":
    main()
    pass
