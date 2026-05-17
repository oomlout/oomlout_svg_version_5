import oobb
import oobb_base
import oobb_make_sets
import oomB
import oobb_markdown
import oobb_dxf_laser_copy
import copy


def main(**kwargs):
   
    filter = "oobb_tray"

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

    copy_files = True
    #copy_files = False
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
