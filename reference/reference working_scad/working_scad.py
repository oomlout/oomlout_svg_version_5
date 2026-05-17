import copy
import oobb
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    typ = scad_help.get_typ(**kwargs)
    oomp_mode = "project"
    #oomp_mode = "oobb"
    filt = ""
    build_variables = scad_help.get_build_variables(typ, filter=filt)
    if True:
        kwargs["filter"] = build_variables["filter"]
        kwargs["save_type"] = build_variables["save_type"]
        kwargs["navigation"] = build_variables["navigation"]
        kwargs["overwrite"] = build_variables["overwrite"]
        kwargs["modes"] = build_variables["modes"]
        kwargs["oomp_mode"] = oomp_mode
        kwargs["oomp_run"] = build_variables["oomp_run"]
    parts = get_parts(kwargs, oomp_mode)
    
    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    if kwargs["navigation"]:
        oobb_style = False  
        sort = scad_help.get_navigation_sort(oobb_style=oobb_style)
        scad_help.generate_navigation(sort=sort)

def get_parts(kwargs, oomp_mode):
    parts = []    

    #load parts from parts/folder/working.yaml
    parts_directory = os.path.join(os.path.dirname(__file__), "parts")
    if not os.path.isdir(parts_directory):
        return parts

    for folder in os.listdir(parts_directory):
        folder_path = os.path.join(parts_directory, folder)
        if not os.path.isdir(folder_path):
            continue

        working_yaml_path = os.path.join(folder_path, "working.yaml")
        if not os.path.isfile(working_yaml_path):
            continue

        with open(working_yaml_path, "r", encoding="utf-8") as infile:
            loaded_part = yaml.safe_load(infile)

        if not isinstance(loaded_part, dict):
            continue

        oobb_details = loaded_part.get("oobb_details")
        if not isinstance(oobb_details, dict):
            continue

        part = loaded_part

        part_kwargs = copy.deepcopy(kwargs)
        part_kwargs.update(copy.deepcopy(loaded_part.get("kwargs", {})))
        part_kwargs.update(copy.deepcopy(oobb_details))
        part["kwargs"] = part_kwargs
        part["oobb_name"] = part.get("oobb_name", oobb_details.get("oobb_name", "default"))

        if oomp_mode == "oobb":
            part["kwargs"]["oomp_size"] = part["oobb_name"]

        parts.append(part)


    return parts

def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    


    #add plate
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_plate"    
        p3["depth"] = depth
        #p3["holes"] = True         uncomment to include default holes
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb.append_full(thing,**p3)
    
    #add holes seperate
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"oobb_holes"
        p3["both_holes"] = True  
        p3["depth"] = depth
        p3["holes"] = "perimeter"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb.append_full(thing,**p3)

    #add a test screw_countersunk
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"screw_countersunk"
        p3["depth"] = depth
        p3["radius_name"] = "m3"
        pos1 = copy.deepcopy(pos)         
        pos1[2] += depth
        p3["pos"] = pos1
        p3["m"] = "#"
        oobb.append_full(thing,**p3)

    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)

def get_base_basic(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    


    #add tray
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"gridfinity_base_raw"    
        p3["gridfinity_width"] = 3
        p3["gridfinity_height"] = height+1
        #p3["holes"] = True         uncomment to include default holes
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb.append_full(thing,**p3)

def get_tray_basic_offset(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    


    #add tray
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"gridfinity_tray_raw_offset"    
        p3["gridfinity_width"] = width
        p3["gridfinity_height"] = height
        p3["gridfinity_depth"] = depth/7
        p3["offset_radius"] = 3
        #p3["holes"] = True         uncomment to include default holes
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb.append_full(thing,**p3)
    
    

    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)    

        
def get_tray_basic(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    


    #add tray
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"gridfinity_tray_default_label"    
        p3["gridfinity_width"] = width
        p3["gridfinity_height"] = height
        p3["gridfinity_depth"] = depth/7
        #p3["holes"] = True         uncomment to include default holes
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb.append_full(thing,**p3)
    
    

    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)    

def get_tray_project_bolt(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    

    depth_gridfinity_lip = 4.4
    #add tray
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"gridfinity_tray_raw"    
        p3["gridfinity_width"] = width
        p3["gridfinity_height"] = height
        #p3["gridfinity_depth"] = (depth-depth_gridfinity_lip)/7
        p3["gridfinity_depth"] = (depth)/7
        p3["wall_thickness"] = 1.25
        p3["lip_style"] = "none"
        #label_style disabled
        p3["label_style"] = "disabled"
        #p3["holes"] = True         uncomment to include default holes
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb.append_full(thing,**p3)
    
    

    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)  

def get_tray_project_bolt_fractional_test(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    

    depth_gridfinity_lip = 4.4
    #add tray
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"gridfinity_tray_fractional_test"    
        p3["gridfinity_width"] = width
        p3["gridfinity_height"] = height * 2
        #p3["gridfinity_depth"] = (depth-depth_gridfinity_lip)/7
        p3["gridfinity_depth"] = (depth)/7
        p3["wall_thickness"] = 1.25
        p3["lip_style"] = "none"
        #label_style disabled
        p3["label_style"] = "disabled"
        #p3["holes"] = True         uncomment to include default holes
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb.append_full(thing,**p3)
    
    

    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs) 

if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)
