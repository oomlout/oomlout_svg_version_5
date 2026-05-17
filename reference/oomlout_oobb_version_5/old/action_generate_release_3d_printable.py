import os
import shutil
import json

def main(**kwargs):
    print("action_generate_release_3d_printable")
    pass
    folder_things = kwargs.get("folder_things", "C:\\gh\\oomlout_oobb_version_4_generated_parts\\parts")
    folder_release = kwargs.get("folder_release", "C:/gh/oomlout_oobb_release_3d_print")
    clone_if_missing = kwargs.get("clone_if_missing", True)

    #if folder doesn't exist clone in from github
    if clone_if_missing and not os.path.exists(folder_release):
        #save cwd
        cwd = os.getcwd()
        #change to folder c:\gh
        os.chdir("C:/gh")
        #clone in
        os.system(f"git clone https://github.com/oomlout/oomlout_oobb_release_3d_print")
        #change back to cwd
        os.chdir(cwd)

    folder_3dpr = f"{folder_release}/3dpr"
    
    #make directory
    os.makedirs(folder_3dpr, exist_ok=True)
    folder_navigation = f"{folder_release}/navigation"
    #iterate through each folder in things no recursion
    folders = os.listdir(folder_things)
    for folder in folders:
        
        #iterate through each file in folder
        json_file = f"{folder_things}/{folder}/details.json"
        file_3dpr_source = f"{folder_things}/{folder}/3dpr.stl"
        if os.path.isfile(file_3dpr_source):
            #load json file
            if os.path.isfile(json_file):
                with open(json_file, 'r') as file:
                    data = json.load(file)
                
                #3dpr copy
                file_3dpr_destination = f"{folder_3dpr}/{folder}/3dpr.stl"
                file_3dpr_source_png = f"{folder_things}/{folder}/3dpr.png"
                file_working_yaml = f"{folder_things}/{folder}/working.yaml"

                #make directory
                os.makedirs(os.path.dirname(file_3dpr_destination), exist_ok=True)
                #if source exists
                if os.path.isfile(file_3dpr_source):
                    print(".", end="", flush=True)
                    shutil.copy(file_3dpr_source, file_3dpr_destination)
                
                #navigation copy
                type = data.get("type", "none")
                width = data.get("width", "0")
                height = data.get("height", "0")
                file_3dpr_navigation = f"{folder_navigation}/{type}/width_{width}/height_{height}/{folder}/3dpr.stl"
                file_3dpr_navigation_png = f"{folder_navigation}/{type}/width_{width}/height_{height}/{folder}/3dpr.png"
                file_3dpr_navigation_working_yaml = f"{folder_navigation}/{type}/width_{width}/height_{height}/{folder}/working.yaml"
                
                if os.path.isfile(file_3dpr_source):
                    os.makedirs(os.path.dirname(file_3dpr_navigation), exist_ok=True)
                    shutil.copy(file_3dpr_source, file_3dpr_navigation)                    
                    shutil.copy(file_3dpr_source_png, file_3dpr_navigation_png)
                    shutil.copy(file_working_yaml, file_3dpr_navigation_working_yaml)
            pass    








if __name__ == "__main__":
    kwargs = {}

    main(**kwargs)
    pass