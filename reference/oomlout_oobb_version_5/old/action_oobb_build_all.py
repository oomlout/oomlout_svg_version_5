import oobb
import oobb_base
import oobb_make_sets



just_yaml_files = False
#just_yaml_files = True


oobb_make_sets.make_all()
oobb_base.dump("pickle")
oobb_base.dump("folder")
#oobb_base.dump("json")

#make readmes
if True:
    command = f"python C:\gh\oomlout_oomp_utility_readme_generation\\working.py"
    import os
    os.system(command)

if not just_yaml_files:    
    oobb_base.build_things(overwrite=False, save_type="all")
    import action_generate_release_3d_printable
    action_generate_release_3d_printable.main()
    import action_generate_release_laser_cut
    action_generate_release_laser_cut.main()
    #input = input("Press Enter to continue...")

