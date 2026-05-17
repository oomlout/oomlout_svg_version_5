import os
import shutil
import json

def main(**kwargs):
    print("action_generate_release_laser_cut")
    pass
    folder_things = kwargs.get("folder_things", "C:\\gh\\oomlout_oobb_version_4_generated_parts\\parts")
    folder_release = kwargs.get("folder_release", "C:/gh/oomlout_oobb_release_laser_cut")
    clone_if_missing = kwargs.get("clone_if_missing", True)

    #if folder doesn't exist clone in from github
    if clone_if_missing and not os.path.exists(folder_release):
        #save cwd
        cwd = os.getcwd()
        #change to folder c:\gh
        os.chdir("C:/gh")
        #clone in
        os.system(f"git clone https://github.com/oomlout/oomlout_oobb_release_laser_cut")
        #change back to cwd
        os.chdir(cwd)

    folder_laser = f"{folder_release}/laser_cut"
    #make directory
    os.makedirs(folder_laser, exist_ok=True)
    folder_navigation = f"{folder_release}/navigation"
    #iterate through each folder in things no recursion
    folders = os.listdir(folder_things)
    for folder in folders:
        
        #iterate through each file in folder
        json_file = f"{folder_things}/{folder}/details.json"
        file_laser_flat_source = f"{folder_things}/{folder}/laser_flat"
        file_laser_flat_source_svg = f"{file_laser_flat_source}.svg"
        file_laser_flat_source_dxf = f"{file_laser_flat_source}.dxf"        
        file_laser_flat_source_png = f"{file_laser_flat_source}.png"
        file_working_yaml = f"{folder_things}/{folder}/working.yaml"

        if os.path.isfile(file_laser_flat_source_svg):
            #load json file
            if os.path.isfile(json_file):
                with open(json_file, 'r') as file:
                    data = json.load(file)
                
                #laser svg copy
                file_3dpr_destination = f"{folder_laser}/svg/{folder}/laser.svg"
                #make directory
                os.makedirs(os.path.dirname(file_3dpr_destination), exist_ok=True)
                #if source exists
                
                if os.path.isfile(file_laser_flat_source_svg):
                    print(".", end="", flush=True)
                    os.makedirs(os.path.dirname(file_3dpr_destination), exist_ok=True)
                    shutil.copy(file_laser_flat_source_svg, file_3dpr_destination)
                #laser dxf copy
                file_3dpr_destination = f"{folder_laser}/dxf/{folder}.dxf"
                #if source exists
                if os.path.isfile(file_laser_flat_source_dxf):
                    print(".", end="", flush=True)
                    os.makedirs(os.path.dirname(file_3dpr_destination), exist_ok=True)
                    shutil.copy(file_laser_flat_source_dxf, file_3dpr_destination)
                
                #navigation copy
                type = data.get("type", "none")
                width = data.get("width", "0")
                height = data.get("height", "0")
                file_3dpr_navigation_svg = f"{folder_navigation}/{type}/width_{width}/height_{height}/{folder}/laser.svg"
                file_3dpr_navigation_dxf = f"{folder_navigation}/{type}/width_{width}/height_{height}/{folder}/laser.dxf"
                file_3dpr_navigation_png = f"{folder_navigation}/{type}/width_{width}/height_{height}/{folder}/laser.png"
                file_3dpr_navigation_working_yaml = f"{folder_navigation}/{type}/width_{width}/height_{height}/{folder}/working.yaml"


                if os.path.isfile(file_laser_flat_source_svg):
                    print(f"copying {file_laser_flat_source_svg} to {file_3dpr_navigation_svg}")
                    os.makedirs(os.path.dirname(file_3dpr_navigation_svg), exist_ok=True)
                    shutil.copy(file_laser_flat_source_svg, file_3dpr_navigation_svg)
                    shutil.copy(file_laser_flat_source_dxf, file_3dpr_navigation_dxf)
                    shutil.copy(file_laser_flat_source_png, file_3dpr_navigation_png)
                    shutil.copy(file_working_yaml, file_3dpr_navigation_working_yaml)
            pass    








if __name__ == "__main__":
    kwargs = {}

    main(**kwargs)
    pass