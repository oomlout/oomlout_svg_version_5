from solid2 import *
import copy
import hashlib
import importlib.util
import ntpath
import os
import re
import shlex
import subprocess

from solidpython_compat import apply_modifier

mode = "laser"
#mode = "3d_print"

defined_objects = {}

radius_dict = {}
countersunk_dict = {}
_RAW_SCAD_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_raw_scad_cache")
_COMPONENT_RENDER_LOOKUP = None
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

try:
    from solid2.core.scad_import import extra_scad_includes, module_cache_by_resolved_filename
except Exception:
    extra_scad_includes = None
    module_cache_by_resolved_filename = None


def _skip_existing_images_enabled():
    value = os.environ.get("OOBB_SKIP_EXISTING_IMAGES", "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _file_exists_with_content(path):
    try:
        return os.path.exists(path) and os.path.getsize(path) > 0
    except OSError:
        return False


def _cleanup_raw_scad_artifacts(output_dir):
    if not output_dir or not os.path.isdir(output_dir):
        return

    hex_pattern = re.compile(r"^(?P<stem>.+)_[0-9a-f]{16}\.scad$")
    for entry in os.listdir(output_dir):
        match = hex_pattern.match(entry)
        if not match:
            continue

        friendly_name = f"{match.group('stem')}.scad"
        friendly_path = os.path.join(output_dir, friendly_name)
        hashed_path = os.path.join(output_dir, entry)

        if os.path.exists(friendly_path):
            try:
                os.remove(hashed_path)
            except OSError:
                pass


def _reset_scad_import_state():
    if module_cache_by_resolved_filename is not None:
        module_cache_by_resolved_filename.clear()
    if extra_scad_includes is not None:
        extra_scad_includes.clear()


def _is_scad_absolute_path(path):
    return (
        os.path.isabs(path)
        or ntpath.isabs(path)
        or re.match(r"^[A-Za-z]:[\\/]", path) is not None
    )


def _make_relative_scad_path(target, base_dir):
    try:
        if re.match(r"^[A-Za-z]:[\\/]", target) is not None or "\\" in target:
            relative_path = ntpath.relpath(ntpath.abspath(target), ntpath.abspath(base_dir))
        else:
            relative_path = os.path.relpath(os.path.abspath(target), base_dir)
    except ValueError:
        # Different drive roots on Windows cannot be relativized.
        return target

    return relative_path.replace("\\", "/")


def _normalize_scad_use_lines(filename):
    if not filename or not os.path.isfile(filename):
        return

    try:
        with open(filename, "r", encoding="utf-8") as handle:
            content = handle.read()
    except OSError:
        return

    include_re = re.compile(r"(use|include)\s+<([^>]+)>\s*;?")
    file_dir = os.path.dirname(os.path.abspath(filename))
    include_lines = []
    seen_lines = set()

    for match in include_re.finditer(content):
        directive = match.group(1)
        original_target = match.group(2).strip()
        normalized_target = original_target

        if _is_scad_absolute_path(original_target):
            normalized_target = _make_relative_scad_path(original_target, file_dir)

        replacement = f"{directive} <{normalized_target}>;"
        if replacement not in seen_lines:
            seen_lines.add(replacement)
            include_lines.append(replacement)

    content_without_includes = include_re.sub("", content)
    changed = content_without_includes != content

    header_line = ""
    body = content_without_includes
    first_newline = content_without_includes.find("\n")
    if first_newline != -1:
        header_candidate = content_without_includes[:first_newline].rstrip("\r")
        if header_candidate.strip().startswith("$fn"):
            header_line = header_candidate
            body = content_without_includes[first_newline + 1 :].lstrip("\r\n")
    elif content_without_includes.strip().startswith("$fn"):
        header_line = content_without_includes.strip()
        body = ""

    rebuilt_parts = []
    if header_line:
        rebuilt_parts.append(header_line)
    if include_lines:
        if rebuilt_parts:
            rebuilt_parts.append("")
        rebuilt_parts.extend(include_lines)
    rebuilt_content = "\n".join(rebuilt_parts)
    if rebuilt_content:
        rebuilt_content += "\n\n"
    rebuilt_content += body.lstrip("\r\n")

    if rebuilt_content == content and not changed:
        return

    try:
        with open(filename, "w", encoding="utf-8") as handle:
            handle.write(rebuilt_content)
    except OSError:
        return

def set_mode(m):
    global mode
    mode = m
    radius_dict['m6'] = 6.5/2
    radius_dict['m3'] = 3.3/2
    if mode == "laser":
        radius_dict['m6'] = 6/2
        radius_dict['m3'] = 3/2

    countersunk_dict['m3'] = {}
    countersunk_dict['m3']['little_rad'] = radius_dict['m3']
    countersunk_dict['m3']['big_rad'] = (5.5+0.6)/2
    if mode == "laser":
        countersunk_dict['m3']['big_rad'] = (4.75+0.6)/2
        countersunk_dict['m3']['little_rad'] = (4.75+0.6)/2

    countersunk_dict['m3']['height'] = 1.7


def _load_component_module(file_path, object_name):
    module_name = f"opsc_component_{object_name}_{abs(hash(str(file_path)))}"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load component module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_component_render_lookup():
    lookup = {}
    components_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "components")
    if not os.path.isdir(components_root):
        return lookup

    for entry in sorted(os.listdir(components_root)):
        folder_path = os.path.join(components_root, entry)
        working_file = os.path.join(folder_path, "working.py")
        if not os.path.isdir(folder_path) or not os.path.isfile(working_file):
            continue
        try:
            module = _load_component_module(working_file, entry)
        except Exception:
            continue
        render_fn = getattr(module, "render", None)
        if not callable(render_fn):
            continue

        metadata = {}
        define_fn = getattr(module, "define", None)
        if callable(define_fn):
            try:
                metadata = define_fn()
            except Exception:
                metadata = {}

        if entry not in lookup:
            lookup[entry] = render_fn

        aliases = metadata.get("shape_aliases", [])
        if isinstance(aliases, str):
            aliases = [aliases]
        for alias in aliases:
            alias = alias.strip()
            if alias and alias not in lookup:
                lookup[alias] = render_fn
    return lookup


def _get_component_render_lookup():
    global _COMPONENT_RENDER_LOOKUP
    if _COMPONENT_RENDER_LOOKUP is None:
        _COMPONENT_RENDER_LOOKUP = _build_component_render_lookup()
    return _COMPONENT_RENDER_LOOKUP

def opsc_make_object(filename, objects, save_type="none",resolution=50, layers = 1, tilediff = 200, mode="laser", overwrite=True, start = 1.5, render=True):
    filename_test = filename.replace(".scad",".png")
    if overwrite or not os.path.exists(filename_test):
        set_mode(mode)
        save_type = save_type.lower()
        path = os.path.dirname(filename)
        if not os.path.exists(path) and path != "":
            os.makedirs(path)
        _reset_scad_import_state()
        output_dir = os.path.dirname(os.path.abspath(filename))
        final_object = opsc_get_object(objects, mode=mode, output_dir=output_dir)
        # Save the final object to the specified filename    
        #file_header = """$fn = %s;
#use <MCAD/involute_gears.scad>
#"""
        file_header = "$fn = %s;\n"
        scad_render_to_file(final_object, filename, file_header=file_header % resolution)
        _normalize_scad_use_lines(filename)
        _cleanup_raw_scad_artifacts(output_dir)
        if save_type == "all":
            saveToAll(filename, render=render)
        elif save_type == "dxf":
            saveToDxf(filename)
        if mode == "laser":
            filename_laser = filename.replace(".scad","_flat.scad")
            scad_render_to_file(getLaser(final_object, layers=layers, tilediff=tilediff, start = start), filename_laser, file_header='$fn = %s;\n' % resolution)
            _normalize_scad_use_lines(filename_laser)
            _cleanup_raw_scad_artifacts(output_dir)
            if save_type == "all":
                saveToAll(filename_laser, render=render)
            elif save_type == "dxf" or save_type == "laser":
                saveToDxf(filename_laser)
        _reset_scad_import_state()
            
    else:
        print("File already exists: " + filename)

def opsc_get_object(objects, mode="laser", output_dir=None):
    # Create the solidpython objects only include the positive objects and if they don't have inclusion or their inclusion is either all or mode
    # Initialize an empty list to store the results
    
    
    # objects is a list of dicts, but might also contain lists please flatten it so its a single dimension list of dicts please check recursively
    
    #do it 4 times
    pass
    for i in range(8):
        objects_2 = []
        for obj in objects:
            # use recursion
            if isinstance(obj, dict):
                objects_2.append(obj)
            elif isinstance(obj, list):
                objects_2.extend(obj)
        objects = objects_2


    ################## rotation
    positive_objects = []
    negative_objects = []
    """
    # Iterate over the "objects" list    
    for objs in objects:
        #if objs is a list put it in a list
        #unpacking in case its a list of lists
        if isinstance(objs, dict):
            objs = [objs]
            if isinstance(objs, dict):
                objs = [objs]
        for obj in objs:
        # Check if the current object has a "type" key with a value of "positive"
            if obj['type'] == 'rotation':
                # rotation tpye            
                type = obj['type']
                typetype = obj.get('typetype',"p")
                rot = obj.get('rot',"")
                if rot == "":
                    rot_x = obj.get('rot_x',0)
                    rot_y = obj.get('rot_y',0)
                    rot_z = obj.get('rot_z',0)
                    rot = [rot_x, rot_y, rot_z]
                    obj["rot"] = rot
                    obj.pop('rot_x', None)
                    obj.pop('rot_y', None)
                    obj.pop('rot_z', None)
                objects = obj.get('objects',[])
                #return_value = opsc_get_object(objects, mode = mode)
                if typetype == "p" or typetype == "positive":
                    pass
                    #positive_objects.append(return_value)
                elif typetype == "n" or typetype == "negative":
                    pass
                    #negative_objects.append(return_value)
    # Initialize an empty list to store the results
    """

    types = {}
    types["rotation"] = []
    types["hull"] = []
    types["positive"] = []
    types["negative"] = []
    types["positive_positive"] = []
    types["negative_negative"] = []


    for typ in types:    
        for obj in objects:
            test_type = obj.get('type',"")
            if test_type == "p":
                obj['type'] = "positive"
            elif test_type == "n":
                obj['type'] = "negative"          
            
            if obj['type'] == typ:
                inclusion = obj.get('inclusion',"all")
                if inclusion == "all" or inclusion == mode:                    
                    if typ != "rotation" and typ != "hull":
                        opsc_item = get_opsc_item(obj, output_dir=output_dir)
                        types[typ].append(opsc_item)
                    else:
                        obj_original = copy.deepcopy(obj)
                        typtyp = obj.get('typetype',"p")
                        objects_2 = obj.get('objects',[])
                        pos = copy.deepcopy(obj.get('pos',[0,0,0]))
                        rot = obj.get('rot',"")
                        m_original = obj.get('m',"")
                        pass
                        # expand object list
                        for i in range(8):
                            objects_3 = []
                            for obj in objects_2:
                                # use recursion
                                if isinstance(obj, dict):
                                    objects_3.append(obj)
                                elif isinstance(obj, list):
                                    objects_3.extend(obj)
                            objects_2 = objects_3

                        #for obj in objects_2:
                        #    obj["type"] = "p"


                        opsc_objects = opsc_get_object(objects_2, mode=mode, output_dir=output_dir)
                        
                        if rot == "":
                            rot_x = obj.get('rot_x',0)
                            rot_y = obj.get('rot_y',0)
                            rot_z = obj.get('rot_z',0)
                            rot = [rot_x, rot_y, rot_z]
                            obj["rot"] = rot
                            obj.pop('rot_x', None)
                            obj.pop('rot_y', None)
                            obj.pop('rot_z', None)
                        
                        
                        if typ == "hull":
                            opsc_objects = hull()(opsc_objects)

                        opsc_objects = apply_modifier(translate(pos)(rotate(a=rot)(opsc_objects)), m_original)

                        # dealing with rot_shift
                        rot_shift = obj_original.get('rot_shift', [])
                        if rot_shift != []:
                            opsc_objects = rotate(rot_shift[1])(translate(rot_shift[0])(opsc_objects))


                        if typtyp == "p" or typtyp == "positive":
                            types["positive"].append(opsc_objects)
                        elif typtyp == "n" or typtyp == "negative":
                            types["negative"].append(opsc_objects)
                        elif typtyp == "pp" or typtyp == "positive_positive":
                            types["positive_positive"].append(opsc_objects)
                        elif typtyp == "nn" or typtyp == "negative_negative":
                            types["negative_negative"].append(opsc_objects)

    for typ in types:
        for obj in types[typ]:
            #remove any None
            if obj == None:
                types[typ].remove(obj)
                print("removed None")
    # remvoe a doubble none
    for typ in types:
        for obj in types[typ]:
            #remove any None
            if obj == None:
                types[typ].remove(obj)
                print("removed None")       
        
    positive_object = union()(*types["positive"])
    # Union the negative objects
    negative_object = union()(*types["negative"])
    # Create the final object by subtracting the negative objects from the positive objects
    return_value = difference()(positive_object, negative_object)

    if (len(types["positive_positive"]) > 0):
        positive_positive_object = union()(*types["positive_positive"])
        return_value = union()(return_value, positive_positive_object)
    if (len(types["negative_negative"]) > 0):
        negative_negative_object = union()(*types["negative_negative"])
        return_value = difference()(return_value, negative_negative_object)
    return return_value

def get_opsc_item(params, output_dir=None):
    # An array of function names for basic shapes
    basic_shapes = ['cube', 'sphere', 'cylinder', 'import_stl']
    # An array of function names for other shapes
    other_shapes = ['hole', 'slot', 'slot_small', 'text_hollow', "tube", "tube_new", 'tray', 'rounded_rectangle', 'rounded_octagon','rounded_rectangle_extra', 'sphere_rectangle', 'countersunk', 'polyg', 'polyg_tube', 'polyg_tube_half', 'bearing', 'oring', 'vpulley', 'd_shaft', 'gear', 'pulley_gt2', "cycloid", "raw_scad"]

    # Convert radius to r if present, and remove radius from the params dictionary
    if 'radius' in params:
        if isinstance(params['radius'], str):
            # Use the radius_dict to map the radius string value to a numerical value
            params['r'] = radius_dict[params['radius']]
        else:
            params['r'] = params['radius']
        del params['radius']
    

    if params['shape'] in basic_shapes:
        shape = params['shape']
        if shape != "import_stl":
            # Remove shape and unexpected dictionary values
            allowed_keys = {'size', 'r', 'r1', 'r2', 'd', 'h', 'rw', 'rh', 'dw', 'dh'}
        if shape == "import_stl":
            allowed_keys = {'file', 'center', 'convexity', 'scale'}
        shape_params = {k: v for k, v in params.items() if k in allowed_keys}

        m = params.get('m', '')
        func = globals()[params['shape']]
        
        return_value = get_opsc_transform(params,func(**shape_params))
        return_value = apply_modifier(return_value, m)
        return return_value
        
    elif params['shape'] == 'polygon':
        # Remove shape and unexpected dictionary values
        h  = params.get('height',"")
        if h == "":
            h  = params.get('depth',"")
        if h == "":
                h = params['h']
        allowed_keys = {'points'}
        shape_params = {k: v for k, v in params.items() if k in allowed_keys}

        m = params.get('m', '')
        func = globals()[params['shape']]
        return_value = get_opsc_transform(params,linear_extrude(h)(globals()[params['shape']](**shape_params)))
        return_value = apply_modifier(return_value, m)
        return return_value
    
    elif params['shape'] == 'text':        
        h  = params.get('height',params.get("h", params.get("depth", 10)))
        center = params.get('center', False)
        if center:
            params['halign'] = 'center'
            params['valign'] = 'center'
        allowed_keys = {'text', 'size', 'font', 'halign', 'valign', 'spacing', 'direction', 'language', 'script', 'file'}
        shape_params = {k: v for k, v in params.items() if k in allowed_keys}
        m = params.get('m', '')
        func = globals()[params['shape']]
        if h != 0:
            return_value = get_opsc_transform(params,linear_extrude(h)(globals()[params['shape']](**shape_params)))
        else:
            return_value = get_opsc_transform(params,globals()[params['shape']](**shape_params))
        return_value = apply_modifier(return_value, m)
        #strip translations away if they are
        return return_value
        
    component_renderers = _get_component_render_lookup()
    renderer = component_renderers.get(params['shape'])
    if renderer is not None:
        p2 = copy.deepcopy(params)
        p2["pos"] = [0,0,0]
        if output_dir is not None and p2.get("shape") == "raw_scad":
            p2["cache_dir"] = output_dir
        m = params.get('m', '')
        return_value = get_opsc_transform(params, renderer(p2))
        return_value = apply_modifier(return_value, m)
        return return_value

    # If the object type is not a basic shape, check if it's a defined object or one of the other shapes
    if params['shape'] in other_shapes:
        p2 = copy.deepcopy(params)
        p2["pos"] = [0,0,0]
        if output_dir is not None and p2.get("shape") == "raw_scad":
            p2["cache_dir"] = output_dir
        m = params.get('m', '')
        return_value = get_opsc_transform(params, globals()[params['shape']](p2))
        return_value = apply_modifier(return_value, m)
        return return_value


def get_opsc_transform(params, solid_obj):
    # Rotate the object based on the 'rot' field in the params dictionary, or the 'rotX', 'rotY', and 'rotZ' fields if 'rot' is not present
    col = params.get('color', "")
    rot = params.get('rot', [])
    rot_shift = params.get('rot_shift', [])
    if rot:
        rotX, rotY, rotZ = rot
    else:
        rotX = params.get('rotX', 0)
        rotY = params.get('rotY', 0)
        rotZ = params.get('rotZ', 0)
    rotation = [rotX, rotY, rotZ]
    if rotation != [0, 0, 0]:
        solid_obj = rotate(rotation)(solid_obj)

    # Translate the object based on the 'pos' field in the params dictionary, or the 'x', 'y', and 'z' fields if 'pos' is not present
    pos = params.get('pos', [])
    if pos:
        x, y, z = pos
    else:
        x = params.get('x', 0)
        y = params.get('y', 0)
        z = params.get('z', 0)
    translation = [x, y, z]
    if translation != [0, 0, 0]:
        solid_obj = translate(translation)(solid_obj)
    
    # color
    if col != "":
        solid_obj = color(c=col)(solid_obj)
    
    # add a rotation shift
    if rot_shift != []:
        rot_shift_shift = rot_shift[0]
        rot_shift_rot = rot_shift[1]
        solid_obj = rotate(rot_shift_rot)(translate(rot_shift_shift)(solid_obj))
    
    
    return solid_obj


import random

def opsc_easy_array(type, shape, repeats, pos_start, shift_arr, **kwargs):
    for i in range(0,3):
        repeats.append(1)
        pos_start.append(0)
        shift_arr.append(0)
    return_objects = []

    for x in range(0,repeats[0]):
        for y in range(0,repeats[1]):
            for z in range(0,repeats[2]):
                return_objects.append(opsc_easy(type, shape, pos=[pos_start[0]+x*shift_arr[0],pos_start[1]+y*shift_arr[1],pos_start[2]+z*shift_arr[2]], **kwargs))
    return return_objects                

def opsc_easy(type, shape, **kwargs):
    obj = {
        'type': type,
        'shape': shape
    }
    params_allowed = []
    params_base = ['color','center','comment','size', 'r', 'radius', 'r1', 'r2', 'd', 'h', 'rw', 'rh', 'dw', 'dh', 'pos', 'x', 'y', 'z', 'rot', 'rotX', 'rotY', 'rotZ', "w", "inclusion", 'sides', 'height', 'width', "m", "id", "od", "depth", "exclude_clearance", "clearance", "points","text","valign","halign","font","inset","wall_thickness","extra","wall_thickness", "loc", "locs", "location", "locations", "objects","rot_shift","extra_clearance","file","source","module","module_kwargs","omit_corner"]
    params_allowed.extend(params_base)
    params_gear = ['number_of_teeth', 'circular_pitch', 'diametral_pitch', 'pressure_angle', 'clearance', 'gear_thickness', 'rim_thickness', 'rim_width', 'hub_thickness', 'hub_diameter', 'bore_diameter', 'circles', 'backlash', 'twist', 'involute_facets', 'flat', "lobe_number", "radius_offset", "radius_pin", "offset", "clearance_bearing"]
    params_allowed.extend(params_gear)
    for param in params_allowed:
        if param in kwargs:
            obj[param] = kwargs[param]
    return obj



import os



import random

def test(num_objects):
    objects = []
    for i in range(num_objects):
        # Choose a random shape
        #shape = random.choice(['cube', 'sphere', 'cylinder', 'hole', 'slot', "rounded_rectangle"])
        shape = random.choice(["rounded_rectangle"])

        # Choose a random type
        type = random.choice(['positive', 'negative'])
        
        # Create an empty object dictionary
        obj = {'shape': shape, 'type': type}
        
        # Set shape-specific parameters
        if obj['shape'] in ['cube']:
            obj['size'] =  [random.uniform(5, 15), random.uniform(5, 15), random.uniform(5, 15)]
        if obj['shape'] in ['rounded_rectangle']:
            obj['size'] =  [random.uniform(5, 15), random.uniform(5, 15), random.uniform(5, 15)]
            obj['r'] = random.uniform(0.5, 5)
        elif obj['shape'] == 'sphere':
            obj['r'] = random.uniform(5, 15)
        elif obj['shape'] in ['cylinder', 'hole']:
            obj['r'] = random.uniform(0.5, 5)
            obj['h'] = random.uniform(5, 15)
        elif obj['shape'] == 'slot':
            obj['r'] = random.uniform(0.5, 5)
            obj['h'] = random.uniform(5, 15)
            obj['w'] = random.uniform(5, 15)
        
        # Set a random position and rotation
        obj['pos'] = [random.uniform(-20, 20), random.uniform(-20, 20), random.uniform(-20, 20)]
        obj['rot'] = [random.uniform(-180, 180), random.uniform(-180, 180), random.uniform(-180, 180)]
        
        # Add the object to the list
        objects.append(obj)
    return objects

def save_to_all(fileIn, render=True):
    saveToAll(fileIn, render=render)
def saveToAll(fileIn, render=True):
    saveToFileAll(fileIn, render=render)

def save_to_dxf(fileIn, fileOut="", copy_to_laser=True):
    saveToDxf(fileIn, fileOut=fileOut, copy_to_laser=copy_to_laser)
def saveToDxf(fileIn, fileOut="", copy_to_laser=True):
    if fileOut == "":
        fileOut = fileIn.replace(".scad",".dxf")
    saveToFile(fileIn, fileOut)

def save_to_png(fileIn, fileOut=""):
    saveToPng(fileIn, fileOut=fileOut)    
def saveToPng(fileIn, fileOut="",extra="--render"):
    if fileOut == "":
        fileOut = fileIn.replace(".scad",".png")
    saveToFile(fileIn, fileOut, extra=extra)
    if os.path.basename(fileOut).lower() == "image.png":
        preview_400_path = os.path.join(os.path.dirname(fileOut), "image_400.png")
        preview_extra = f"{extra} --imgsize 400,400".strip()
        saveToFile(fileIn, preview_400_path, extra=preview_extra)

def save_preview_images(fileIn, output_dir):
    iso_path = os.path.join(output_dir, "image.png")
    iso_400_path = os.path.join(output_dir, "image_400.png")
    iso_120_path = os.path.join(output_dir, "image_120.png")
    top_path = os.path.join(output_dir, "image_top.png")
    top_400_path = os.path.join(output_dir, "image_top_400.png")
    top_120_path = os.path.join(output_dir, "image_top_120.png")
    side_path = os.path.join(output_dir, "image_side.png")
    side_400_path = os.path.join(output_dir, "image_side_400.png")
    side_120_path = os.path.join(output_dir, "image_side_120.png")

    preview_targets = [
        iso_path,
        iso_400_path,
        iso_120_path,
        top_path,
        top_400_path,
        top_120_path,
        side_path,
        side_400_path,
        side_120_path,
    ]

    if _skip_existing_images_enabled() and all(_file_exists_with_content(path) for path in preview_targets):
        return {
            "iso": iso_path,
            "iso_400": iso_400_path,
            "iso_120": iso_120_path,
            "top": top_path,
            "top_400": top_400_path,
            "top_120": top_120_path,
            "side": side_path,
            "side_400": side_400_path,
            "side_120": side_120_path,
        }

    view_common = "--autocenter --viewall --projection o"
    iso_extra = f"{view_common} --camera=0,0,0,55,0,25,500"
    top_extra = f"{view_common} --camera=0,0,0,90,0,0,500"
    side_extra = f"{view_common} --camera=0,0,0,0,90,0,500"
    iso_120_extra = f"{iso_extra} --imgsize 120,120"
    top_400_extra = f"{top_extra} --imgsize 400,400"
    top_120_extra = f"{top_extra} --imgsize 120,120"
    side_400_extra = f"{side_extra} --imgsize 400,400"
    side_120_extra = f"{side_extra} --imgsize 120,120"

    saveToPng(fileIn, fileOut=iso_path, extra=iso_extra)
    saveToFile(fileIn, iso_120_path, extra=iso_120_extra)
    saveToPng(fileIn, fileOut=top_path, extra=top_extra)
    saveToFile(fileIn, top_400_path, extra=top_400_extra)
    saveToFile(fileIn, top_120_path, extra=top_120_extra)
    saveToPng(fileIn, fileOut=side_path, extra=side_extra)
    saveToFile(fileIn, side_400_path, extra=side_400_extra)
    saveToFile(fileIn, side_120_path, extra=side_120_extra)

    return {
        "iso": iso_path,
        "iso_400": iso_400_path,
        "iso_120": iso_120_path,
        "top": top_path,
        "top_400": top_400_path,
        "top_120": top_120_path,
        "side": side_path,
        "side_400": side_400_path,
        "side_120": side_120_path,
    }

def save_to_stl(fileIn, fileOut=""):
    saveToStl(fileIn, fileOut=fileOut)
def saveToStl(fileIn, fileOut=""):
    if fileOut == "":
        fileOut = fileIn.replace(".scad",".stl")
    saveToFile(fileIn, fileOut)
    
def save_to_svg(fileIn, fileOut=""):
    saveToSvg(fileIn, fileOut=fileOut)
def saveToSvg(fileIn, fileOut=""):
    if fileOut == "":
        fileOut = fileIn.replace(".scad",".svg")
    saveToFile(fileIn, fileOut)

def save_to_file(fileIn, fileOut,extra=""):
    saveToFile(fileIn, fileOut,extra=extra)
def saveToFile(fileIn, fileOut,extra=""):
    if (
        _skip_existing_images_enabled()
        and fileOut.lower().endswith(".png")
        and _file_exists_with_content(fileOut)
    ):
        print(f"skipping existing image: {fileOut}")
        return
    launch_args = ["openscad", "-o", fileOut]
    if extra:
        launch_args.extend(shlex.split(extra, posix=False))
    launch_args.append(fileIn)
    if fileOut.lower().endswith(".png") and "--render" not in launch_args:
        launch_args.append("--render")
    print(f"saving to file: {' '.join(launch_args)}")
    subprocess.run(launch_args, check=False)

def save_to_file_all(fileIn, extra="", render=True):
    saveToFileAll(fileIn, extra=extra, render=render)
def saveToFileAll(fileIn, extra="", render=True):
    #extra = extra + " --colorscheme Tomorrow"
    
    launch_strings = []
    #add openscad
    launch_strings.append("openscad")
    if render:
        launch_strings.append(f'--render')
    formats = ["dxf","png","svg","stl"]
    
    format_string = ""
    for f in formats:
        file_out = fileIn.replace(".scad","."+f)
        format_string = f'{format_string} -o "{file_out}"'
        #add format string to launch string
        launch_strings.append(f"-o")
        launch_strings.append(f'{file_out}')
                          
    launch_strings.append(f'{fileIn}')
                          
    launchStr = " ".join(launch_strings)
    print(f"saving to file all: {launchStr}")
    #if fileout folder doesn't exist, create it
    path = os.path.dirname(file_out)
    if not os.path.exists(path) and path != "":
        os.makedirs(path)
    os.system(launchStr)

def getLaser(final_object,start=1.5,layers=1,thickness=3,tilediff=200):
        rv= []
        layers = max(1,layers)
        for x in range(int(layers)):
            rv.append(translate([0,x*tilediff,0])(
                    projection()(
                        intersection()(translate([-500,-500,start+x*thickness])(cube(size=[1000,1000,0.1])),
                            final_object
                        )
                    )
                )
            )            
        return union()(rv)

set_mode("laser")

