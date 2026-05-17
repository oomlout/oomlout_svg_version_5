import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import copy
import oobb
import opsc

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
    d["name"] = 'oobb_wire_cutout'
    d["name_long"] = 'OOBB Wire Cutouts: Wire Cutout (Base)'
    d["description"] = 'Base wire connector cutout geometry for JST-style connectors; configurable pin count and polarization.'
    d["category"] = 'OOBB Wire Cutouts'
    d["shape_aliases"] = ['wire_cutout']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'num_pins', "description": 'Number of connector pins.', "type": 'number', "default": 2})
    v.append({"name": 'polarized', "description": 'Add polarization dot and extra pin slot.', "type": 'bool', "default": False})
    v.append({"name": 'width', "description": 'Connector footprint width in grid units.', "type": 'number', "default": 2})
    v.append({"name": 'height', "description": 'Connector footprint height in grid units.', "type": 'number', "default": 2})
    v.append({"name": 'through', "description": 'Escape cutout depth is full through.', "type": 'bool', "default": False})
    v.append({"name": 'mode', "description": 'Render modes: laser, 3dpr, true.', "type": 'list', "default": '["laser","3dpr","true"]'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable
def action(**kwargs):
    """Geometry component."""
    def get_oobb_wire_cutout(**kwargs):
        # setting up for rotation object
        typ = kwargs.get("type", "negative")
        kwargs["type"] = "positive" #needs to be positive for the difference to work
        rot_original = get_rot(**kwargs)  
        kwargs.pop("rot","") 


        # storing pos and popping it out to add it in rotation element     
        pos_original = copy.deepcopy(copy.deepcopy(kwargs.get("pos", [0, 0, 0])))
        kwargs.pop("pos", None)
        pos = [0,0,0]
        kwargs["pos"] = pos


        width = kwargs.get("width", 2)
        height = kwargs.get("height", 2)    
        polarized = kwargs.get("polarized", False)
        through = kwargs.get("through", False)
        num_pins = kwargs.get("num_pins", 2)


        modes = kwargs.get("mode", ["laser", "3dpr", "true"])
        if modes == "all":
            modes = ["laser", "3dpr", "true"]
        if type(modes) == str:
            modes = [modes]

        pole_extra = 0
        if polarized:
            pole_extra = 1
        shift = 2 - num_pins

        return_value = []
        depth_universal = 2.6
        for mode in modes:
            #depth = oobb.gv("wi_depth", mode) 
            depth = depth_universal
            extra = oobb.gv("wi_extra", mode)
            i01 = oobb.gv("wi_i01", mode)        
            p3 = copy.deepcopy(kwargs)
            length = oobb.gv("wi_length", mode)

            ##wire back piece
            wbp = copy.deepcopy(kwargs)
            wid = 5
            hei = i01 * num_pins - 2
            depth = depth_universal
            #depth = 8
            size = [wid, hei, depth]
            x = 25.567
            y = 2.54 + (shift) * 2.54/2
            z = 0 
            pos1 = copy.deepcopy(pos)
            pos1[0] = kwargs["pos"][0] + x
            pos1[1] = kwargs["pos"][1] + y
            pos1[2] = kwargs["pos"][2] + z
            wbp["pos"] = pos1
            wbp["shape"] = "oobb_cube_center"
            wbp["size"] = size    
            wbp["inclusion"] = mode    
            return_value.append(oobb.oe(**wbp))

            ##big piece front       
            extra_bpf = 1 
            bpf = copy.deepcopy(wbp)
            wid = length - 8 + extra_bpf
            hei = i01 * (num_pins+polarized) + extra
            size = [wid, hei, depth]
            x = 3.354 - extra_bpf / 2
            y = wbp["pos"][1] - 2.54 / 2 * polarized
            z = 0
            pos1 = copy.deepcopy(pos)
            pos1[0] = pos1[0] + x
            pos1[1] = pos1[1] + y
            pos1[2] = pos1[2] + z
            bpf["shape"] = "oobb_cube_center"
            bpf["pos"] = pos1
            bpf["size"] = size    
            #bpf["m"] = "#"
            bpf["inclusion"] = mode    
            return_value.append(oobb.oe(**bpf))

            ##big piece back
            bpb = copy.deepcopy(wbp)        
            wid = length
            hei = i01 * num_pins + extra
            size = [wid, hei, depth]        
            x = 16.038
            y = wbp["pos"][1]
            z = 0
            pos1 = copy.deepcopy(pos)
            pos1[0] = pos1[0] + x
            pos1[1] = pos1[1] + y
            pos1[2] = pos1[2] + z        
            bpb["pos"] = pos1
            bpb["size"] = size
            return_value.append(oobb.oe(**bpb))

            ##key piece
            kp = copy.deepcopy(bpf)
            wid = i01 + extra
            hei = i01 * (num_pins + 2 + polarized) + extra
            size = [wid, hei, depth]
            x = 7.77
            y = bpf["pos"][1]
            z = 0
            pos1 = copy.deepcopy(pos)
            pos1[0] = pos1[0] + x
            pos1[1] = pos1[1] + y
            pos1[2] = pos1[2] + z        
            kp["pos"] = pos1
            kp["size"] = size    
            return_value.append(oobb.oe(**kp))

            #big escape            
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_cube_center"
            pos1 = copy.deepcopy(pos)
            pos_shift = [22.5+6.044,0,0]
            pos1[0] = pos1[0] + pos_shift[0]
            pos1[1] = pos1[1] + pos_shift[1]
            pos1[2] = pos1[2] + pos_shift[2]
            p3["pos"] = pos1
            depth = depth_universal
            if through:
                depth = 10
            p3["size"] = [7, 10, depth]
            p3["inclusion"] = mode  
            p3["depth"] = depth
            #p3["m"] = "#"
            return_value.append(oobb.oe(**p3))


        #polariation dot
        if polarized:
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_cylinder"
            x = 0.5
            shape = kwargs.get("shape", "")
            y = -15#default for ba
            z = 3/2
            p3["pos"] = [kwargs["pos"][0] + x, kwargs["pos"][1] + y, kwargs["pos"][2] + z]
            p3["r"] = 1.5
            p3["depth"] = depth_universal
            #p3["m"] = "#"
            return_value.extend(oobb.oobb_easy(**p3))

        pos_shift = [height/2*15,0,0]
        pos_original[0] += pos_shift[0]
        pos_original[1] += pos_shift[1]
        pos_original[2] += pos_shift[2]
        # packaging as a rotation object
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot_original
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]


        return return_value_2 

    # ziptie
