import oobb
import oobb_base
import yaml
import os
from solid2 import *

import os
import shutil

def main(**kwargs):

    render = kwargs.get("render", False)
    overwrite = kwargs.get("overwrite", False)
    git = kwargs.get("git", False)
    filter = kwargs.get("filter", False)
    #if filter isn't a list make it one
    if not isinstance(filter, list):
        filter = [filter]

    

    pass
    folder_things = "parts"
    details = []    
    #smd
    details.append({    "name":"oomlout_oobb_bundle_smd_magazine", "matches": ["smd"],
                        "shift_x": 12*15,
                        "shift_y": 12*15
                        })
    
    #smd
    details.append({    "name":"oomlout_oobb_bundle_smd_magazine", "matches": ["oobb_tray"],
                        "shift_x": 5*15,
                        "shift_y": 5*15
                        })

    # decorations
    details.append({    "name":"oomlout_oobb_bundle_decorations", "matches": ["oobb_decoration"]})
    details.append({    "name":"oomlout_oobe_bundle_decorations", "matches": ["oobe_decoration"]})
    details.append({    "name":"oomlout_oobb_bundle_bunting_alphabet",
                        "matches": ["oobb_bunting_alphabet"],
                        "shift_x": 13*15,
                        "shift_y": 15*15
                        })
    details.append({    "name":"oomlout_oobb_bundle_oobb_holder_05_03_00_ex_motor_servo_standard_01",
                        "matches": [
                            "oobb_bearing_plate_03_03_12_6705_ex_no_center",
                            "oobb_bearing_plate_03_03_12_6705_ex_horn_adapter_screws_sh_motor_servo_standard_01",
                            "oobb_holder_05_03_09_ex_motor_servo_standard_01_top",
                            "oobb_holder_05_03_15_ex_motor_servo_standard_01",
                            "oobb_holder_05_03_00_ex_motor_servo_standard_01_all_print",
                            "oobb_bearing_plate_03_03_12_6705_ex_no_center"
                            ],
                        "shift_x": 6*15,
                        "shift_y": 5*15
                        })
    
    details.append({    "name":"oomlout_oobb_bundle_oobb_holder_06_03_06_ex_motor_tt_01_servo_control",
                        "matches": [
                            "oobb_holder_06_03_06_ex_motor_tt_01",
                            "oobb_bearing_plate_03_03_12_6705_ex_no_center",
                            "oobb_bearing_plate_03_03_12_6705_ex_sandwich_sh_motor_tt_01",
                            "oobb_wire_03_03_04_ex_basic_extra_mm"
                            ],
                        "shift_x": 6*15,
                        "shift_y": 5*15
                        })

    details.append({    "name":"oomlout_oobb_bundle_oobb_holder_05_03_09_ex_motor_stepper_nema_17_flat",
                        "matches": [
                            "oobb_holder_05_03_09_ex_motor_stepper_nema_17_flat",
                            "oobb_bearing_plate_03_03_12_6705_ex_no_center",
                            "oobb_bearing_plate_03_03_12_6705_sh_coupler_flanged"
                            ],
                        "shift_x": 6*15,
                        "shift_y": 5*15
                        })


    #plates_basic
    sizes = ["oobb", "oobe"]

    for size in sizes:
        plates = {  "name":f"oomlout_{size}_bundle_plates_basic"}        
        plates["shift_x"] = 10*15
        plates["shift_y"] = 10*15
        if size == "oobe":            
            plates["shift_x"] = 10*15/2
            plates["shift_y"] = 10*15/2
        includes = []
        #widths etc
        widths = [1,2,3,5,7,9]
        heights = [1,3,5,7,9]
        thicknesses = [3]
        for width in widths:
            for height in heights:
                for thickness in thicknesses:
                    includes.append([width,height,thickness])
        #squares
        for i in range(1,10):
            includes.append([i,i,3])

        

        

        includes_string = []
        for include in includes:
            width = str(include[0]).zfill(2)
            height = str(include[1]).zfill(2)
            thickness = str(include[2]).zfill(2)
            #oobb_pl_{width}_{height}_{thickness}
            includes_string.append(f"{size}_plate_{width}_{height}_{thickness}")

        plates["matches"] = includes_string
        details.append(plates)



    for detail in details:
        name = detail["name"]
        #if any filter string is in name then do it
        if any(x in name for x in filter):
            matches = detail["matches"]
            #folder_bundle = f"git/{name}"
            folder_bundle = f"C:/GH/oobb_bundle/{name}"
            kwargs["folder_bundle"] = folder_bundle
            #if folder_bundle doesnt exists then make it
            if not os.path.isdir(folder_bundle):
                os.makedirs(folder_bundle)
            
            
            print(f"processing {name}")
            
            
            #go through each folder in things   
            for folder in os.listdir(folder_things):
                for match in matches:
                    if match in folder:
                        copy_folder(folder_things, folder, folder_bundle, name )
            
            

            # copy production files
            copy_folder_production(**kwargs)

            #render
            if render:
                shift_x = detail.get("shift_x", 140)
                shift_y = detail.get("shift_y", 75)
                make_all_3dpr_file(folder_bundle, shift_x, shift_y, overwrite=overwrite)
            
            
            #do resolutions
            import oom_base
            oom_base.image_resolutions_dir(directory=folder_bundle, overwrite=True)

            import oom_git
            directory = folder_bundle
            if git:
                oom_git.push_to_git(directory = directory)
    
def make_all_3dpr_file(folder_bundle, shift_x = 140, shift_y = 75, **kwargs):
    overwrite = kwargs.get("overwrite", False)
    #if folder_bundl doesnt exists then make it
    if not os.path.isdir(folder_bundle):
        os.makedirs(folder_bundle)
    

    #get a list of all the files in scad/ that end with _3dpr.scad
    files = []
    for file in os.listdir(os.path.join(folder_bundle, "3dpr")):
        if file.endswith(".stl"):
            files.append(file)
    #go through each file


    

    # List of SCAD files
    stl_files = files  # replace these with your actual file names

    # Initialize an empty OpenSCAD object
    assembly = []

    
    #fill shift values to make a square grid of the number of files in scad_files
    shift_values = []
    sqr = int(sqrt(len(stl_files)))
    for i in range(len(stl_files)):
        shift_values.append([shift_x * (i % sqr), shift_y * (i // sqr), 0])


    

    file_out = os.path.join(folder_bundle, "3dpr/3dpr_all.scad")
    file_out_base = os.path.join(folder_bundle, "3dpr_all")
    with open(file_out, "w") as f:
        for shift, filename in zip(shift_values, stl_files):
            f.write(f'translate([{shift[0]}, {shift[1]}, {shift[2]}]) ' + '{' + '\n')
            f.write(f'import("{filename}");\n')
            f.write('}\n')
    #use the command line openscad.exe to create an stl and png of this file

    #only if.stl of it doesnt exist
    if not os.path.isfile(f"{file_out_base}.stl")  or overwrite:
        #print what's haapening
        print(f"    processing {file_out}")
        os.system(f"openscad -o {file_out_base}.stl -o {file_out_base}.png {file_out}")


    
def copy_folder(folder_things, folder, folder_bundle, name):
    print(f"    processing {folder}")
    #copy the folder to folder_bundle/src
    folder_bundle_src = f"C:/GH/oobb_bundle/{name}/src"
    folder_bundle_src_folder = os.path.join(folder_bundle_src, folder)
    if not os.path.isdir(folder_bundle_src_folder):
        shutil.copytree(os.path.join(folder_things, folder), folder_bundle_src_folder)
    #process the source folder
    #copy 3dpr laser laser_flat and true .scad to scad folder
    

    details = []
    details.append({"folder_bundle" : "scad",
                    "files" : ["3dpr.scad", "laser.scad", "laser_flat.scad", "true.scad"]}
                    )
    details.append({"folder_bundle" : "stl",
                    "files" : ["3dpr.stl", "laser.stl", "laser_flat.stl", "true.stl"]}
                    )    
    details.append({"folder_bundle" : "3dpr",
                    "files" : ["3dpr.stl"]}
                    )    
    details.append({"folder_bundle" : "png",
                    "files" : ["3dpr.png", "laser.png", "laser_flat.png", "true.png"]}
                    )  
    details.append({"folder_bundle" : "laser",
                    "files" : ["laser_flat.dxf", "laser_flat.svg", "laser_flat.pdf"]}
                    )
    
    folder_bundle_start = folder_bundle
    for detail in details:

        ###### scad

        folder_bundle = os.path.join(folder_bundle_start, detail["folder_bundle"])
        if not os.path.isdir(folder_bundle):
            os.makedirs(folder_bundle)
        files = detail["files"]
        for file in files:
            #make the new filename the folder things name plus a _ and the file name
            new_file_name = folder + "_" + file
            src = os.path.join(folder_bundle_src_folder, file)
            src = src.replace("/", "\\")
            dst = os.path.join(folder_bundle, new_file_name)
            dst = dst.replace("/", "\\")
            #if src exists copy it to dst
            if os.path.isfile(src):
                #copy the file to the new folder
                shutil.copyfile(src, dst)
                #print a dot with no new line
                print(".", end="")
                print (f"        copied {src} to {dst}")
            else:
                print(f"        {src} does not exist")
                pass
    

def copy_folder_production(**kwargs):
    folder_bundle = kwargs.get("folder_bundle", "")
    folder_oobb_production_folder = f"{folder_bundle}/oobb_production"
    file_oobb_produciont_yaml = f"{folder_bundle}/oobb_production.yaml"
    #load details into yaml
    if os.path.isfile(file_oobb_produciont_yaml):
        with open(file_oobb_produciont_yaml, "r") as f:
            details = yaml.load(f, Loader=yaml.FullLoader)
        
        production_files = details["oobb_production_file"]
        for production_file in production_files:
            file_source = production_file["file_source"]
            file_source = f"{folder_bundle}/{file_source}"
            file_render = production_file["file_render"]
            file_render = f"{folder_bundle}/{file_render}"
            file_type = production_file["file_type"]
            file_render_extension = production_file.get("file_render_extension","png")        
            file_extension = production_file["file_extension"]
            index = production_file["index"]
            file_destination = f"{folder_oobb_production_folder}/{file_type}_{index}.{file_extension}"
            render_destination = f"{folder_oobb_production_folder}/images/{file_type}_{index}.{file_render_extension}"
            try:
                shutil.copyfile(file_source, file_destination)
                #if file_render fodler doesn't exist make it
                if not os.path.isdir(f"{folder_oobb_production_folder}/images"):
                    os.makedirs(f"{folder_oobb_production_folder}/images")
                shutil.copyfile(file_render, render_destination)
            except Exception as e:
                print(f"    {e}")
        import oom_markdown
        p3 = {}
        p3["file_template"] = details.get("template", "templates/oobb_production_readme.md.j2")
        p3["file_output"] = f"{folder_oobb_production_folder}/readme.md"
        p3["dict_data"] = details
        
        oom_markdown.get_jinja2_template(**p3)


        





if __name__ == "__main__":
    kwargs = {}
    #filter = "oomlout_oobb_bundle_oobb_holder_05_03_09_ex_motor_stepper_nema_17_flat"
    #filter = "oomlout_oobb_bundle_oobb_holder_05_03_00_ex_motor_servo_standard_01"
    filter = "oomlout_oobb_bundle_oobb_holder_06_03_06_ex_motor_tt_01_servo_control"
    #filter = "holder"
    #filter = "tt"
    #filter = ""
    kwargs["filter"] = filter
    
    rend = False
    #rend = True
    kwargs["render"] = rend
    
    overwrite = False
    #overwrite = True
    kwargs["overwrite"] = overwrite

    git = False
    git = True
    kwargs["git"] = git

    main(**kwargs)
