import oobb
import oobb_base
import oobb_make_sets
import oomB
import oobb_markdown
import oobb_dxf_laser_copy
import copy


def main(**kwargs):
    
    

    filter = ""


    oobb_make_sets.make_all(filter=filter)

    #dump = False
    dump = True
    if dump:
        oobb_base.dump("json")
        oobb_base.dump("folder")

    #save_type = "none"
    #save_type = "laser"
    #save_type = "3dpr"    
    save_type = "all"

    #overwrite = True
    overwrite = False
    
    
    modes = ["laser", "3dpr", "true"]
    #modes = ["3dpr"]
    #modes = ["laser"]
    oobb_base.build_things(overwrite=overwrite, filter=filter, save_type=save_type, modes=modes)

    #generate_release = False
    generate_release = True
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
