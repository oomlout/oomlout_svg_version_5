import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


# ---------- cross-component helper imports ----------
import importlib.util
def _load_component(folder_name):
    path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
    spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_rot_mod = _load_component("oobb_rot")
get_rot = _rot_mod.action

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_screw'
    d["name_long"] = 'OOBB Geometry Primitives: Screw'
    d["description"] = 'Screw cutout (socket_cap, countersunk, or self_tapping) with optional through-hole, nut pocket, overhang, and clearance.'
    d["category"] = 'Fasteners'
    d["shape_aliases"] = ['screw']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'radius_name', "description": 'Named radius key, e.g. m3, m6.', "type": 'string', "default": '"m3"'})
    v.append({"name": 'style', "description": 'Screw head style: socket_cap, countersunk, self_tapping.', "type": 'string', "default": '"socket_cap"'})
    v.append({"name": 'depth', "description": 'Shaft hole depth in mm.', "type": 'number', "default": 250})
    v.append({"name": 'zz', "description": 'Z anchor: none, top, bottom.', "type": 'string', "default": '"none"'})
    v.append({"name": 'hole', "description": 'Include a through shaft hole.', "type": 'bool', "default": True})
    v.append({"name": 'clearance', "description": 'Clearance extension sides: top, bottom.', "type": 'string', "default": '""'})
    v.append({"name": 'nut_include', "description": 'Include a nut pocket.', "type": 'bool', "default": False})
    v.append({"name": 'overhang', "description": 'Add overhang geometry.', "type": 'bool', "default": True})
    v.append({"name": 'slot', "description": 'Slot length in mm between two screw centres. Default 0 creates a single screw with no hull.', "type": 'number', "default": 0})
    v.append({"name": 'mode', "description": 'Render modes: laser, 3dpr, true.', "type": 'list', "default": '["laser","3dpr","true"]'})
    v.append({"name": 'rot', "description": 'Rotation [rx,ry,rz] in degrees.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'rot_x', "description": 'X rotation in degrees.', "type": 'number', "default": 0})
    v.append({"name": 'rot_y', "description": 'Y rotation in degrees.', "type": 'number', "default": 0})
    v.append({"name": 'rot_z', "description": 'Z rotation in degrees.', "type": 'number', "default": 0})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable


def _slot_wrap_objects(objects, slot, typetype="positive", modifier=""):
    if float(slot) == 0:
        return objects

    left = {
        "type": "rotation",
        "typetype": typetype,
        "pos": [-float(slot) / 2, 0, 0],
        "rot": [0, 0, 0],
        "objects": copy.deepcopy(objects),
    }
    right = {
        "type": "rotation",
        "typetype": typetype,
        "pos": [float(slot) / 2, 0, 0],
        "rot": [0, 0, 0],
        "objects": copy.deepcopy(objects),
    }

    return {
        "type": "hull",
        "typetype": typetype,
        "pos": [0, 0, 0],
        "rot": [0, 0, 0],
        "m": modifier,
        "objects": [left, right],
    }


def action(**kwargs):
    import oobb
    import opsc
    """Geometry component."""

    hole = kwargs.get("hole", True)
    style = kwargs.get("style", "socket_cap")
    kwargs.pop("style", None)
    clearance = kwargs.get("clearance", "")
    nut_include = kwargs.get("nut_include", kwargs.get("include_nut",kwargs.get("nut", False)))    
    overhang = kwargs.get("overhang", True)
    radius_name = kwargs.get("radius_name", "m3")
    loose = kwargs.get("loose", "")
    depth = float(kwargs.get("depth", 250))
    zz = kwargs.get("zz", "none")
    slot = float(kwargs.get("slot", 0))

    # setting up for rotation object
    typ = kwargs.get("type", "p")
    kwargs["type"] = "positive" #needs to be positive for the difference to work
    rot_original = get_rot(**kwargs)   
    kwargs.pop("rot", None)
    kwargs.pop("rot_x", None)
    kwargs.pop("rot_y", None)
    kwargs.pop("rot_z", None)

    # storing pos and popping it out to add it in rotation element     
    pos_original = copy.deepcopy(copy.deepcopy(kwargs.get("pos", [0, 0, 0])))
    pos_original_original = copy.deepcopy(pos_original)
    kwargs.pop("pos", None)



    return_value = []
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if type(modes) == str:
        modes = [modes] 


    for mode in modes: 
        depth_clearance_top = 250       
        pos_for_overhang = [0, 0, 0]
        pos_base = [0, 0, 0]
        #socket_cap stuff 
        if style == "socket_cap" or style == "self_tapping":
            depth_head = oobb.gv(f'screw_{style}_height_{radius_name}', mode)

            #sort out zz by adjusting pos
            pos = copy.deepcopy(pos_base)
            if zz == "top":
                pos_for_overhang[2] = pos_for_overhang[2] - depth_head
            elif zz == "bottom":
                pos_for_overhang[2] = pos_for_overhang[2] + depth 

            #needs to happen after zz is sorted
            if "top" in clearance and mode == "3dpr":            
                depth_head = depth_head + depth_clearance_top            

            pos1 = copy.deepcopy(pos_for_overhang)
            # screw top
            p3 = copy.deepcopy(kwargs)        
            p3["shape"] = "cylinder"
            p3["pos"] = [pos1[0], pos1[1], pos1[2]]
            p3["r"] = oobb.gv(f"screw_{style}_radius_{radius_name}", mode)
            p3["h"] = depth_head        
            p3["inclusion"] = mode        
            p3.pop("radius_name", None)
            p3.pop("radius", None)
            #p3["m"] = ""
            if slot == 0:
                return_value.append(oobb.oobb_easy(**p3))
            else:
                return_value.append(_slot_wrap_objects([copy.deepcopy(p3)], slot, typetype=p3.get("type", "positive"), modifier=p3.get("m", "")))
        #countersunk stuff
        if style == "countersunk":
            if zz == "top":
                pass
            elif zz == "bottom":
                pos_original[2] = copy.deepcopy(pos_original_original[2]) + depth
            shifts = [0, -depth, -depth]
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "cylinder"
            p3["inclusion"] = mode
            dep = oobb.gv(f"screw_countersunk_depth_{radius_name}", mode)
            p3["h"] = dep
            pos1 = copy.deepcopy(pos_base)
            #pos1[2] = pos1[2] - dep / 2 #hold over mistake but fixed now maybe in bearing plate works check trays
            pos1[2] = pos1[2] - dep

            p3["pos"] = pos1            
            p3["r2"] = oobb.gv(f"screw_countersunk_radius_{radius_name}", mode)
            p3["r1"] = oobb.gv(f"hole_radius_{radius_name}", mode)
            #p3["m"] = "#"
            if slot == 0:
                return_value.extend(oobb.oobb_easy(**p3))
            else:
                return_value.append(_slot_wrap_objects([copy.deepcopy(p3)], slot, typetype=p3.get("type", "positive"), modifier=p3.get("m", "")))
            #clearance = kwargs.get("clearance", "")
            if "top" in clearance:      

                depth_head = depth_clearance_top  
                # screw top
                p3 = copy.deepcopy(kwargs)        
                p3["shape"] = "cylinder"                
                p3["pos"] = [pos1[0], pos1[1], pos1[2]+dep/2]
                if style == "countersunk":
                    p3["pos"] = [pos1[0], pos1[1], pos1[2]+dep]
                p3["r"] = oobb.gv(f"screw_{style}_radius_{radius_name}", mode)
                p3["h"] = depth_head        
                p3["inclusion"] = mode        
                p3.pop("radius_name", None)
                p3.pop("radius", None)
                #p3["m"] = ""
                if slot == 0:
                    return_value.append(oobb.oobb_easy(**p3))
                else:
                    return_value.append(_slot_wrap_objects([copy.deepcopy(p3)], slot, typetype=p3.get("type", "positive"), modifier=p3.get("m", "")))
        # hole    
        if hole:
            radius = oobb.gv(f"hole_radius_{radius_name}", mode)
            if style == "self_tapping":
                if "screw" in loose:    
                    radius = oobb.gv(f"screw_self_tapping_hole_loose_radius_{radius_name}", mode)
                else:
                    radius = oobb.gv(f"screw_self_tapping_hole_radius_{radius_name}", mode)
            p3 = copy.deepcopy(kwargs)
            p3.pop("radius_name", "")
            p3["radius"] = radius
            p3["shape"] = "oobb_hole"
            pos1 = copy.deepcopy(pos_for_overhang)
            p3["pos"] = [pos1[0], pos1[1], pos1[2] - depth]
            p3["inclusion"] = mode        
            #p3["m"] = "#"
            if slot == 0:
                return_value.extend(oobb.oobb_easy(**p3))
            else:
                return_value.append(_slot_wrap_objects(oobb.oobb_easy(**p3), slot, typetype=p3.get("type", "positive"), modifier=p3.get("m", "")))
        # nut
        if nut_include:
            pos1 = copy.deepcopy(pos_for_overhang)
            p3 = copy.deepcopy(kwargs)
            clearance_copy = copy.deepcopy(clearance)
            if "top" in clearance_copy:
                if clearance_copy == "top":
                    p3.pop("clearance", "")
                elif "top" in clearance_copy:
                    for i in range(len(clearance_copy)):
                        if clearance_copy[i] == "top":
                            clearance_copy.pop(i) 
                            p3["clearance"] = clearance_copy
                            break                           

            p3.pop("zz","")
            # maybe add a nut level argument later
            p3["shape"] = "oobb_nut"
            p3["inclusion"] = mode   
            p3["overhang"] = overhang
            p3["pos"] = [pos1[0], pos1[1], pos1[2] -depth]
            p3.pop("loose", "")
            if "nut" in loose:
                p3["loose"] = True
            p3.pop("extra", "")
            if "bottom" in clearance:
                h_nut = oobb.gv(f'nut_depth_{radius_name}', mode)
                dep = depth_clearance_top
                p3["depth"] = dep
                p3["pos"][2] = p3["pos"][2] + h_nut #- dep
                p3["zz"] = "top"
                p3.pop("clearance", "")
            else:
                p3.pop("depth", None)
            #dealing with rot_Z
            rotation_nut = kwargs.get("rotation_nut", None)
            if rotation_nut != None:
                p3["rot"] = rotation_nut    

            #p3["m"] = "#"
            if slot == 0:
                return_value.extend(oobb.oobb_easy(**p3))
            else:
                return_value.append(_slot_wrap_objects(oobb.oobb_easy(**p3), slot, typetype=p3.get("type", "positive"), modifier=p3.get("m", "")))
        # overhang    
        if overhang and style != "countersunk" and mode == "3dpr":        
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_overhang"
            p3["zz"] = "top"
            p3["inclusion"] = "3dpr"  
            p3.pop("width", "")      
            p3.pop("height", "")
            #p3["m"] = "#"
            pos1 = copy.deepcopy(pos_for_overhang)
            p3["pos"] = [pos1[0],pos1[1],pos1[2]]


            #if rot_y == 180:
            #    p3["zz"] = "bottom"     
            #    p3["pos"] = [pos[0], pos[1], pos[2]-0.3]         
            if slot == 0:
                return_value.extend(oobb.oobb_easy(**p3))
            else:
                return_value.append(_slot_wrap_objects(oobb.oobb_easy(**p3), slot, typetype=p3.get("type", "positive"), modifier=p3.get("m", "")))

    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]


    return return_value_2


    # slot


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [70, 0, 20],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'radius_name': 'm3',
                 'style': 'socket_cap',
                 'depth': 16,
                 'zz': 'none',
                 'hole': True,
                 'clearance': '',
                 'nut_include': False,
                 'overhang': False,
                 'slot': 0,
                 'mode': 'true',
                 'rot': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [70, 0, 20],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'radius_name': 'm3',
                 'style': 'countersunk',
                 'depth': 16,
                 'zz': 'none',
                 'hole': True,
                 'clearance': '',
                 'nut_include': False,
                 'overhang': False,
                 'slot': 0,
                 'mode': 'true',
                 'rot': [0, 0, 0]}},
     {'filename': 'test_3',
      'preview_rot': [70, 0, 20],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'radius_name': 'm3',
                 'style': 'self_tapping',
                 'depth': 16,
                 'zz': 'none',
                 'hole': True,
                 'clearance': '',
                 'nut_include': False,
                 'overhang': False,
                 'slot': 0,
                 'mode': 'true',
                 'rot': [0, 0, 0]}},
     {'filename': 'test_4',
      'preview_rot': [70, 0, 20],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'radius_name': 'm3',
                 'style': 'socket_cap',
                 'depth': 16,
                 'zz': 'none',
                 'hole': True,
                 'clearance': '',
                 'nut_include': False,
                 'overhang': False,
                 'slot': 10,
                 'mode': 'true',
                 'rot': [0, 0, 0]}}]

    generated_files = []

    for sample in samples:
        kwargs = copy.deepcopy(sample["kwargs"])
        result = action(**kwargs)
        if isinstance(result, dict) and "components" in result:
            components = copy.deepcopy(result["components"])
        elif isinstance(result, list):
            components = result
        else:
            components = [result]

        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        png_path = os.path.join(sample_dir, "image.png")

        opsc.opsc_make_object(
            scad_path,
            components,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_preview_images(scad_path, sample_dir)
        generated_files.append(png_path)

    return generated_files


