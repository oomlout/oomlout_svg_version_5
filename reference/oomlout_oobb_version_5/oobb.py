##### oobb imports
import os
import sys
import json
import copy

import oobb_variables
from opsc import *

# variable definition
things = {}
variables = {}
osp = 15
osp_minus = 1

# ---------------------------------------------------------------------------
# Component discovery
# ---------------------------------------------------------------------------

# oobb_arch moved to old/ during restructure — ensure it is importable.
_oobb_arch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "old")
if _oobb_arch_path not in sys.path:
    sys.path.insert(0, _oobb_arch_path)

try:
    from oobb_arch.catalog.object_discovery import build_object_lookup, discover_objects
except Exception:
    build_object_lookup = None
    discover_objects = None


_OBJECT_LOOKUP = None
_SHAPE_LOOKUP = None


def _get_oobb():
    """Return this module (self-reference, replaces the old 'import oobb; return oobb')."""
    return sys.modules[__name__]


def _get_object_lookup():
    global _OBJECT_LOOKUP
    if _OBJECT_LOOKUP is None and build_object_lookup is not None:
        try:
            _OBJECT_LOOKUP = build_object_lookup()
        except Exception:
            _OBJECT_LOOKUP = {}
    return _OBJECT_LOOKUP or {}


def _build_shape_lookup():
    """Scan components/*/working.py and build a shape-name -> action() map.

    Two sources of names:
    1. The folder name itself (e.g. folder 'oobb_circle' maps shape 'oobb_circle').
    2. define()["shape_aliases"] — extra aliases declared in the component metadata.

    This is separate from "name_short" which drives part-type dispatch.
    """
    lookup = {}
    if discover_objects is None:
        return lookup
    try:
        _components_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "components")
        objects = discover_objects(objects_root=_components_root)
    except Exception:
        return lookup
    for obj in objects.values():
        # Auto-index by folder name so components/oobb_circle -> shape 'oobb_circle'
        if obj.name and obj.name not in lookup:
            lookup[obj.name] = obj.action_fn
        # Also index every explicit shape_aliases entry
        aliases = obj.metadata.get("shape_aliases", [])
        if isinstance(aliases, str):
            aliases = [aliases]
        for alias in aliases:
            alias = alias.strip()
            if alias and alias not in lookup:
                lookup[alias] = obj.action_fn
    return lookup


def _call_shape_action(shape_fn, kwargs):
    """Call a component action() and normalise the return value.

    Component actions may return:
    - A list of geometry dicts  (geometry-primitive components)
    - A single geometry dict    (wrapped into a list)
    - A thing dict with a 'components' key (part builders — extract components)
    """
    result = shape_fn(**kwargs)
    if isinstance(result, dict):
        if "components" in result:
            result = result["components"]
        else:
            result = [result]
    return result


def _get_shape_lookup():
    """Lazy-init and return the shape-name -> action() lookup."""
    global _SHAPE_LOOKUP
    if _SHAPE_LOOKUP is None:
        _SHAPE_LOOKUP = _build_shape_lookup()
    return _SHAPE_LOOKUP


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

def get_thing_from_dict(thing_dict):
    full_object = thing_dict.get("full_object", False)

    object_lookup = _get_object_lookup()
    discovered_obj = object_lookup.get(thing_dict["type"])
    if discovered_obj is None:
        raise ValueError(f"Unknown part type: {thing_dict['type']}")

    func = discovered_obj.action_fn
    thing = func(**thing_dict)

    return thing


things_folder_absolute = "C:\\gh\\oomlout_oobb_version_4_generated_parts\\parts"

# ---------------------------------------------------------------------------
# Base part-building functions
# ---------------------------------------------------------------------------

def get_default_thing(**kwargs):

    thing = {}
    extra = kwargs.get("extra", "")
    typ = kwargs["type"]
    type_string = typ.replace("_"," ")
    width = kwargs.get("width", "0")
    height = kwargs.get("height", "0")
    thickness = kwargs.get("thickness", "0")
    try:        
        thing.update({"description": f"{type_string} {width}x{height}x{thickness}"})
    except:
        thing.update({"description": f"{type_string}"})

    var_names = ["type", "width", "height", "diameter", "thickness", "radius_name", "depth",
                 "radius_hole", "width_mounting", "oobb_name", "bearing_name", "bearing", "oring_type","extra","shaft"]
    zfill_values = ["width", "height", "thickness", "depth", "diameter"]
    acronyms = {"width": "", "height": "", "diameter": "", "thickness": "", "depth": "", "size": "", "type": "", "radius_hole": "rh","radius_name": "", "width_mounting": "mo", "height_mounting": "hm","oobb_name": "nm", "bearing_name": "", "bearing": "","oring_type":"or", "extra":"ex", "shaft": "sh"}

    if type == "test":
        var_names.append("radius_name")
        acronyms.update({"radius_name": "rn"})
        var_names.append("shape")
        acronyms.update({"shape": "sh"})
        var_names.append("style")
        acronyms.update({"style": "st"})

    deets = {}
    for var in var_names:
        deets[var] = {}

        # if zfill
        if var in zfill_values:
            val = kwargs.get(var, "")
            if isinstance(val, list):
                for i in range(0,len(val)):
                    val[i] = str(val[i]).zfill(2)
                val = "_".join(val)
                deets[var].update({"value": val})
            else:
                if val != "":
                    deets[var].update({"value": str(val).zfill(2)})
                else:
                    deets[var].update({"value": kwargs.get(val, "")})
        else:
            deets[var].update({"value": kwargs.get(var, "")})
        deets[var].update({"acronym": acronyms[var]})
        value_string = deets[var]["value"]
        if type(value_string) == list:
            value_string = "_".join(value_string)

        if deets[var]["acronym"] != "":
            deets[var]["str"] = f"_{deets[var]['acronym']}_{value_string}"
        else:
            deets[var]["str"] = f"_{value_string}"

    id = kwargs.get("size", "")
    for var in deets:
        if deets[var]["value"] != "":
            if deets[var]["value"] != "":
                id += deets[var]["str"]
    id = id.replace(".","d")
    extra_test = str(kwargs.get("extra", ""))
    if "servo_standard" in extra_test:
        pass

    thing.update({"id": id})
    thing.update({"type": f"{typ}"})
    try:
        thing.update({"type_oobb": f"{type_dict[typ]}"})
    except:
        pass

    for var in var_names:
        try:
            thing.update({var: kwargs[var]})
        except:
            pass
    try:
        thing.update(
            {"width_mm": kwargs["width"] * gv("osp") - gv("osp_minus")})
    except:
        pass
    try:
        if thickness != "":
            thing.update({"thickness_mm": kwargs["thickness"]})
    except:
        pass
    try:
        thing.update(
            {"height_mm": kwargs["height"] * gv("osp") - gv("osp_minus")})
    except:
        pass
    thing.update({"components": []})
    thing.update({"components_string": []})
    thing.update({"components_objects": []})

    #adding oomp id
    if True:
        part = thing
        size = part["type"] #different in oomp
        
        attributes = ["width","height","diameter","thickness"]
        description_main = ""
        for attribute in attributes:
            test_value = part.get(attribute, "")
            if isinstance(test_value, list):
                attribute_new = ""
                for value in test_value:
                    attribute_new += f"{value}_"
                test_value = attribute_new[:-1]
            if test_value != "":
                if description_main != "":
                    description_main += "_"
                attribute_name = attribute
                if attribute == "thickness":
                    attribute_name = "mm_depth"
                description_main += f"{test_value}_{attribute_name}"
                description_main = description_main.replace(".","_")
        
        string_extra = ""
        tests = ["bearing","shaft","extra","bearing_name","radius_name","depth","oring_type"]
        for test in tests:
            if test in part:
                deet = part.get(test, "")
                if isinstance(deet, list):
                    attribute_new = ""
                    for value in deet:
                        attribute_new += f"{value}_"
                    deet = attribute_new[:-1]
                
                if deet != "":
                    if string_extra != "":
                        string_extra += "_"
                    string_extra += f"{deet}_{test}"        
        description_extra = string_extra

        part_details = {}
        part_details["classification"] = "oobb"
        part_details["type"] = "part"
        part_details["size"] = size
        part_details["color"] = ""
        
        part_details["description_main"] = description_main
        part_details["description_extra"] = description_extra
        part_details["manufacturer"] = ""
        part_details["part_number"] = ""
        part_details["short_name"] = ""

        part_details["link_redirect"] = f"https://github.com/oomlout/oomlout_oobb_version_4_generated_parts/tree/main/parts/{part['id']}"
        navigate_link = f"{part_details['classification']}/{part_details['type']}/{part_details['size']}/{part_details['description_main']}"
        if part_details["description_extra"] != "":
            navigate_link += f"/{part_details['description_extra']}"
        part_details["link_main"] = f"https://github.com/oomlout/oomlout_oobb_version_4_generated_parts/tree/main/navigation_oomp/{navigate_link}/part"

        thing.update(part_details)
        
        id_parts = ["classification","type","size","color","description_main","description_extra","manufacturer","part_number"]
        id = ""
        for id_part in id_parts:
            value = part_details.get(id_part, "")
            if value != "":
                id += f"{part[id_part]}_"
        id = id[:-1]
        id = id.replace(".0_","_")
        id = id.replace(".","d")
        part_details["id"] = id 
        thing.update(part_details)
        
        name = id.replace("_"," ").title()
        name = name.replace("Mm","mm")
        thing.update({"name_text": name})

        short_name = name
        short_name = short_name.replace("Oobb Part ","")
        short_name = short_name.replace(" Width ","x")
        short_name = short_name.replace(" Height ","x")
        short_name = short_name.replace(" Diameter ","x")
        short_name = short_name.replace(" Thickness ","x")
        short_name = short_name.replace("mm Depth "," ")
        short_name = short_name.replace("mm Depth","")
        short_name = short_name.replace("  "," ")
        short_name = short_name.replace("  "," ")
        length_max = 40
        if len(short_name) > length_max: 
            short_name = short_name.split(" ")
            short_name_working = ""
            for word in short_name:
                if len(short_name_working) + len(word) < length_max:
                    short_name_working += word + " "
                else:
                    break
            short_name_working = short_name_working.strip()
            short_name = short_name_working
            
        thing.update({"name_short": short_name})

    
    
    return thing


def get_comment(comment, type="p", **kwargs):
    kwargs["comment"] = comment
    kwargs["type"] = type
    m = kwargs.get("m", "*")
    pos = kwargs.get("pos", [0,0,0])
    pos = copy.deepcopy(pos)
    line_length = kwargs.get("line_length", 30)
    comment_shift_line = kwargs.get("comment_shift_line", 0)
    shift_line = 7
    pos[1] = pos[1] + shift_line + comment_shift_line
    return_value = []

    if "\n" not in comment:
        comment = "\n".join([comment[i:i+line_length] for i in range(0, len(comment), line_length)])

    comment_list = comment.split("\n")
    
    pos_line = copy.deepcopy(pos) 
    pos_line[1] = pos_line[1] + ((len(comment_list)-1) * shift_line)
    comment_list[0] = f"COMMENT {comment_list[0]}"
    for comment in comment_list:
        p3 = copy.deepcopy(kwargs)
        p3["s"] = "text"
        p3["text"] = comment
        p3['depth'] = 1
        p3["pos"] = copy.deepcopy(pos_line)
        p3["size"] = 4.5
        p3["center"] = True
        p3["m"] = m
        p3["color"] = "gray"
        p3["font"] = "Arial:style=Bold"
        p3.pop("objects", "")

        if comment != "":
            return_value.extend(oobb_easy(**p3))
            pos_line[1] = pos_line[1] - shift_line
    
    return return_value


def get_default_thing_old_1(**kwargs):
    ######################## old #########################
    thing = {}

    type_dict = {}
    type_dict.update({"bc": "bearing circle"})
    type_dict.update({"bp": "bearing plate"})
    type_dict.update({"bpj": "bearing plate with jack"})
    type_dict.update({"bpjb": "bearing plate with jack basic"})
    type_dict.update({"bw": "bearing wheel"})
    type_dict.update({"ci": "circle"})
    type_dict.update({"hl": "holder"})
    type_dict.update({"jab": "jack basic"})
    type_dict.update({"ja": "jack"})
    type_dict.update({"jg": "jig"})
    type_dict.update({"mps": "mounting plate single sided holes"})
    type_dict.update({"mpt": "mounting plate top and bottom holes"})
    type_dict.update({"mpu": "mounting plate u holes"})
    type_dict.update({"mp": "mounting plate"})
    type_dict.update({"pl": "plate"})
    type_dict.update({"tr": "tray"})
    type_dict.update({"sc": "shaft coupler"})
    type_dict.update({"sh": "shaft"})
    type_dict.update({"sj": "soldering jig"})
    type_dict.update({"th": "tool holder"})
    type_dict.update({"wh": "wheel"})
    type_dict.update({"wi": "wire plate"})
    type_dict.update({"ztj": "zip tie mount jack"})
    type_dict.update({"zt": "zip tie mount"})
    type_dict.update({"bearing": "bearing"})
    type_dict.update({"nut": "nut"})
    type_dict.update({"screw": "screw"})
    type_dict.update({"screw_countersunk": "screw countersunk"})
    type_dict.update({"screw_socket_cap": "screw socket cap"})
    type_dict.update({"standoff": "standoff"})
    type_dict.update({"threaded_insert": "threaded insert"})
    type_dict.update({"test": "test"})
    type_dict.update({"washer": "washer"})
    type_dict.update({"bolt": "bolt"})

    type = kwargs["type"].replace("_", " ")
    width = kwargs.get("width", "0")
    height = kwargs.get("height", "0")
    thickness = kwargs.get("thickness", "0")
    for key in type_dict:
        if type.startswith(key):
            thing.update(
                {"description": f"{type_dict[key]} {width}x{height}x{thickness}"})
    if thing.get("description", "") == "":
        thing.update({"description": f"{type_dict[type]}"})

    var_names = ["type", "width", "height", "diameter", "thickness", "radius_name", "depth",
                 "radius_hole", "width_mounting", "oobb_name", "bearing_name", "bearing", "oring_type","extra","shaft"]
    zfill_values = ["width", "height", "thickness", "depth", "diameter"]
    acronyms = {"width": "", "height": "", "diameter": "", "thickness": "", "depth": "", "size": "", "type": "", "radius_hole": "rh","radius_name": "", "width_mounting": "mo", "height_mounting": "hm","oobb_name": "nm", "bearing_name": "", "bearing": "","oring_type":"or", "extra":"ex", "shaft": "sh"}

    if type == "test":
        var_names.append("radius_name")
        acronyms.update({"radius_name": "rn"})
        var_names.append("shape")
        acronyms.update({"shape": "sh"})
        var_names.append("style")
        acronyms.update({"style": "st"})

    deets = {}
    for var in var_names:
        deets[var] = {}

        if var in zfill_values:
            val = kwargs.get(var, "")
            if val != "":
                deets[var].update({"value": str(kwargs.get(var, "")).zfill(2)})
            else:
                deets[var].update({"value": kwargs.get(var, "")})
        else:
            deets[var].update({"value": kwargs.get(var, "")})
        deets[var].update({"acronym": acronyms[var]})
        if deets[var]["acronym"] != "":
            deets[var]["str"] = f"_{deets[var]['acronym']}_{deets[var]['value']}"
        else:
            deets[var]["str"] = f"_{deets[var]['value']}"

    id = kwargs.get("size", "")
    for var in deets:
        if deets[var]["value"] != "":
            if deets[var]["value"] != "":
                id += deets[var]["str"]
    id = id.replace(".","d")
    print(id)
    thing.update({"id": id})
    thing.update({"type": f"{type}"})
    try:
        thing.update({"type_oobb": f"{type_dict[type]}"})
    except:
        pass

    for var in var_names:
        try:
            thing.update({var: kwargs[var]})
        except:
            pass
    try:
        thing.update(
            {"width_mm": kwargs["width"] * gv("osp") - gv("osp_minus")})
    except:
        pass
    try:
        if thickness != "":
            thing.update({"thickness_mm": kwargs["thickness"]})
    except:
        pass
    try:
        thing.update(
            {"height_mm": kwargs["height"] * gv("osp") - gv("osp_minus")})
    except:
        pass
    thing.update({"components": []})

    return thing


# ---------------------------------------------------------------------------
# Variable access
# ---------------------------------------------------------------------------

def set_variable(name, value, mode=""):
    if mode != "":
        name = name + "_" + mode
    _get_oobb().variables.update({name: value})

def gv(name, mode=""):
    return get_variable(name, mode)

def get_variable(name, mode=""):
    if mode != "":
        name = name + "_" + mode
    rv = _get_oobb().variables[name]
    return rv

def get_hole_pos(x, y, wid, hei, size="oobb"):
    sp = gv("osp")
    if size == "oobe":
        sp = gv("osp")/2

    x_mm = -(wid-1) * sp / 2 + (x - 1) * sp
    y_mm = -(hei-1) * sp / 2 + (y - 1) * sp
    return x_mm, y_mm

def add_thing(thing):
    _get_oobb().things.update({thing["id"]: thing})


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def dump(mode="json"):
    print(f"dumping {mode}")
    if mode == "json":
        with open('things.json', 'w') as outfile:
            json.dump(_get_oobb().things, outfile)
        with open('variables.json', 'w') as outfile:
            json.dump(_get_oobb().variables, outfile)
    elif mode == "pickle":
        import pickle
        if not os.path.exists("temporary"):
            os.makedirs("temporary")
        with open('temporary/things.pickle', 'wb') as outfile:
            pickle.dump(_get_oobb().things, outfile)
        with open('temporary/variables.pickle', 'wb') as outfile:
            pickle.dump(_get_oobb().variables, outfile)
    elif mode == "folder":
        for thing in _get_oobb().things:
            print(".", end="")
            filename = f'{things_folder_absolute}/{thing}/details.json'
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            with open(filename, 'w') as outfile:
                json.dump(_get_oobb().things[thing], outfile, indent=4)
            import yaml
            filename = f'{things_folder_absolute}/{thing}/details.yaml'
            with open(filename, 'w') as outfile:
                yaml.dump(_get_oobb().things[thing], outfile, indent=4)


def load(mode="json"):
    if mode == "json":
        with open('things.json') as json_file:
            _get_oobb().things = json.load(json_file)
        with open('variables.json') as json_file:
            variables = json.load(json_file)
    elif mode == "folder":
        for thing in os.listdir(f"{things_folder_absolute}"):
            try:
                with open(f'{things_folder_absolute}/{thing}/details.json') as json_file:
                    _get_oobb().things.update({thing: json.load(json_file)})
            except FileNotFoundError:
                pass

def build_things(save_type="none", overwrite=True, filter="", modes=["3dpr", "laser", "true"]):
    if type(filter) == str:
        filter = [filter]
    for f in filter:
        for thing in _get_oobb().things:
            if f in thing:
                print(f'building {thing}')
                build_thing(thing, save_type, overwrite, modes=modes)

def build_thing(thing, save_type="all", overwrite=True, modes=["3dpr", "laser", "true"]):    
    if type(modes) != list:
        modes = [modes]
    if "all" in modes:
        modes = ["3dpr", "laser", "true"]
    for mode in modes:
        depth = _get_oobb().things[thing].get(
            "depth_mm", _get_oobb().things[thing].get("thickness_mm", 3))
        height = _get_oobb().things[thing].get("height_mm", 100)
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2)*3
        if "bunting" in thing:
            start = 0.5
        filename = f'{things_folder_absolute}/{thing}/{mode}.scad'    
        _get_oobb().opsc_make_object(filename, _get_oobb().things[thing]["components"], mode=mode, save_type=save_type, overwrite=overwrite, layers=layers, tilediff=tilediff, start=start)
        with open(f'{things_folder_absolute}/{thing}/{mode}.txt', 'w') as outfile:
            component_strings = _get_oobb().things[thing]["components_string"]
            for component in component_strings:
                outfile.write(f'{component}\n')
        with open(f'{things_folder_absolute}/{thing}/{mode}.json', 'w') as outfile:
            json.dump(_get_oobb().things[thing]["components_objects"], outfile, indent=4)
        import yaml
        with open(f'{things_folder_absolute}/{thing}/{mode}.yaml', 'w') as outfile:
            yaml.dump(_get_oobb().things[thing]["components_objects"], outfile, indent=4)


def build_thing_filename(thing, save_type="all", overwrite=True, filename="", depth=3, height=200, render=True):
    modes = ["3dpr", "laser", "true"]
    for mode in modes:
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2)*3
        _get_oobb().opsc_make_object(f'{filename}{mode}.scad', thing, mode=mode, save_type=save_type, overwrite=overwrite, layers=layers, tilediff=tilediff, start=start, render=render)


# ---------------------------------------------------------------------------
# Component string helpers
# ---------------------------------------------------------------------------

def oobb_easy_get_string(**kwargs):
    return_value = ""
    p3 = copy.deepcopy(kwargs)
    
    if p3["pos"] == [0,0,0]:
        p3.pop("pos","")    
    p3.pop("m","")
    p3.pop("inclusion","")

    order = ["shape", "type","radius_name", "depth", "pos"]
    value_pairs = []
    for key in order:
        if key in p3:
            value_pairs.append([key, p3[key]])        
    for key in p3:
        if key not in order:
            value_pairs.append([key, p3[key]])

    for pair in value_pairs:
        key = pair[0]
        value = pair[1]
        value = str(p3[key])
        value = value.replace("[", "")
        value = value.replace("]", "")
        value = value.replace(",", "_")
        value = value.replace(" ", "")
        if value != "":
            return_value += f'{value}_{key}_'
        
    return return_value[:-1].lower()

def oobb_easy_string(**kwargs):
    return oobb_easy(**oobb_easy_string_params(**kwargs))

def oobb_easy_string_params(**kwargs):
    item = kwargs.get("item", "")
    input_string = item

    variable_names = [ "_radius_name", "_depth", "_pos","_width", "_height", "_extra", "_nut", "_clearance", "_bearing", "_type","_holes", "_slots", "_inserts", "_insertion_cone", "_overhang", "_inclusion", "_rot","_thickness"]

    result_dict = {}

    shape = input_string.split("_shape")[0]
    result_dict["_shape"] = {}
    result_dict["_shape"]["value"] = shape
    input_string = input_string.replace(shape + "_shape", "")

    i = 0
    while i < len(input_string):
        for variable in variable_names:
            if input_string.startswith(variable, i):
                start = i
                end = i + len(variable)
                before = input_string[:start]
                after = input_string[end:]
                result_dict[variable] = {"before": before, "after": after}
                i = end
            
        i += 1
    variable_indexes = {'' : 0}
    for variable in variable_names:
        variable_index = input_string.find(variable)
        if variable_index != -1:
            variable_indexes[variable] = input_string.find(variable)

    for current_variable in variable_names:
        index = input_string.find(current_variable)        
        closest_variable = ""
        for variable in variable_names:
            try:
                if variable_indexes[variable] < index and variable_indexes[variable] > variable_indexes[closest_variable]:
                    closest_variable = variable
            except KeyError:
                pass

        try:
            value = input_string[variable_indexes[closest_variable]:index]
            value = value.replace(closest_variable, "")
            value = value.strip("_")
            result_dict[current_variable]["value"] = value
        except KeyError:
            pass
        
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = result_dict["_shape"]["value"]
    for variable in variable_names:        
        if variable in result_dict:
            value = result_dict[variable]["value"]
            value = value.replace("_mm", "")
            p3[variable] = value
        
    p3["_type"] = p3.get("_type", "p")

    convert_to_floats = ["_depth", "_width", "_height"]
    for key in convert_to_floats:
        if key in p3:
            p3[key] = float(p3[key])
    if "_pos" in p3:
        pos_split = p3["_pos"].split("_")
        p3["_pos"] = [float(pos_split[0]), float(pos_split[1]), float(pos_split[2])]
    if "_rot" in p3:
        pos_split = p3["_rot"].split("_")
        p3["_rot"] = [float(pos_split[0]), float(pos_split[1]), float(pos_split[2])]

    for key in list(p3.keys()):
        if key.startswith("_"):
            p3[key[1:]] = p3[key]
            del p3[key]

    return p3


# ---------------------------------------------------------------------------
# Component assembly
# ---------------------------------------------------------------------------

def append_full(thing, **kwargs):
    objects_raw = kwargs.get("objects", [])

    objects = []
    for object in objects_raw:
        if type(object) == list:
            for object_2 in object:
                if type(object_2) == list:
                    for object_3 in object_2:
                        if type(object_3) == list:
                            for object_4 in object_3:
                                if type(object_4) == list:
                                    for object_5 in object_4:
                                        if type(object_5) == list:
                                            for object_6 in object_5:
                                                objects.append(object_6)
                                        else:
                                            objects.append(object_5)
                                else:
                                    objects.append(object_4)
                        else:
                            objects.append(object_3)
                else:
                    objects.append(object_2)        
        else:
            objects.append(object)
    
    m = kwargs.get("m", "")
    if objects != []:
        for object in objects:            
            object["m"] = m
            append_full(thing, **object)
        return    

    kwargs_original = copy.deepcopy(kwargs)
    poss = kwargs.get("pos", [0,0,0])
    if poss == []:
        poss = [0,0,0]        
    if type(poss[0]) != list:
        poss = [poss]

    shapes = kwargs.get("shape", "")
    if type(shapes) != list:
        shapes = [shapes]

    rot_shifts = kwargs.get("rot_shift", None)
    if type(rot_shifts) == list:
        if type(rot_shifts[0]) == list:
            rot_shifts = rot_shifts
        else:
            rot_shifts = [rot_shifts]
    else:
        rot_shifts = [rot_shifts]

    for shape in shapes:
        for pos in poss:
            for rot_shift in rot_shifts:
                kwargs = copy.deepcopy(kwargs_original)
                kwargs["pos"] = pos
                kwargs["shape"] = shape
                if rot_shift is not None:
                    kwargs["rot_shift"] = rot_shift
                else:
                    kwargs.pop("rot_shift", None)

                comment = kwargs.get("comment", "")
                comment_display = kwargs.get("comment_display", False)
                m = kwargs.get("m", "")
                item = kwargs.get("item", "")
                
                p3 = copy.deepcopy(kwargs)
                if item != "":
                    string_params = oobb_easy_string_params(item=item)
                    p3.update(string_params)

                ths = thing["components_objects"]
                p4 = copy.deepcopy(p3)
                p4.pop("comment", None)
                p4.pop("thing", None)
                p4.pop("item", None)
                ths.append(p4)

                ths = thing["components_string"]
                p4 = copy.deepcopy(p3)
                p4.pop("comment", None)
                p4.pop("thing", None)
                p4.pop("item", None)
                p4.pop("objects", "")
                string_to_add = oobb_easy_get_string(**p4)
                ths.append(string_to_add)

                th = thing["components"]

                if comment != "":        
                    p4 = copy.deepcopy(p3)
                    p4.pop("rot","")
                    p4.pop("type", None)
                    p4["m"] = "*"
                    if comment_display:
                        p4["m"] = m
                    pass 

                p4 = copy.deepcopy(p3)
                p4["comment"] = f"description {string_to_add}\n"
                p4["m"] = "*"

                p4 = copy.deepcopy(p3)
                th.extend(oobb_easy(**p4))


def oe(**kwargs):
    return oobb_easy(**kwargs)

def oobb_easy(**kwargs):
    kwargs_original = copy.deepcopy(kwargs)
    poss = kwargs.get("pos", [0,0,0])
    shapes = kwargs.get("shape", "")
    if type(poss[0]) != list:
        poss = [poss]
    if type(shapes) != list:
        shapes = [shapes]

    return_value_2 = []
    for shape in shapes:
        for pos in poss:
            kwargs = copy.deepcopy(kwargs_original)
            kwargs["pos"] = pos
            kwargs["shape"] = shape
            key_mappings = {"type": "t", "shape": "s", "radius_name": "rn"}

            for new_key, old_key in key_mappings.items():
                value = kwargs.get(old_key)
                if value is not None:
                    kwargs[new_key] = value
                    del kwargs[old_key]

            shape = kwargs.get('shape',"")

            if "oobb" in shape or "oobe" in shape:
                shape = kwargs["shape"]
                shape = shape.replace("_extra_mm", "")
                shape = shape.replace("_spacer_10_mm", "")
                shape_lookup = _get_shape_lookup()
                if shape in shape_lookup:
                    return_value_2.append(_call_shape_action(shape_lookup[shape], kwargs))
                else:
                    raise ValueError(f"Unknown shape: {shape}")
            else:
                shape_lookup = _get_shape_lookup()
                if shape in shape_lookup:
                    return_value_2.append(_call_shape_action(shape_lookup[shape], kwargs))
                else:
                    raise ValueError(f"Unknown shape: {shape}")
    return return_value_2

def oobb_easy_array(**kwargs):
    for i in range(0, 3):
        kwargs["repeats"].append(1)
        kwargs["pos_start"].append(0)
        kwargs["shift_arr"].append(0)
    return_objects = []

    repeats = kwargs["repeats"]
    for x in range(0, int(repeats[0])):
        for y in range(0, int(repeats[1])):
            for z in range(0, int(repeats[2])):
                pos = [0, 0, 0]
                pos[0] = kwargs["pos_start"][0]+x*kwargs["shift_arr"][0]
                pos[1] = kwargs["pos_start"][1]+y*kwargs["shift_arr"][1]
                pos[2] = kwargs["pos_start"][2]+z*kwargs["shift_arr"][2]
                kwargs.update({"pos": pos})
                return_objects.append(oobb_easy(**kwargs))
    return return_objects


# ---------------------------------------------------------------------------
# Geometry manipulation helpers
# ---------------------------------------------------------------------------

def shift(thing, shift):
    mode = "components"

    if "components" in thing:
        return_thing = thing
        thing = thing["components"]        
        mode = "thing"
    for i in range(0,8):
        thing_2 = []
        for th in thing:
            if type(th) == list:
                thing_2.extend(th)
            else:
                thing_2.append(th)
        thing = thing_2

    for component in thing:  
        component["pos"] = copy.deepcopy(component["pos"])     
        component["pos"][0] += shift[0]
        component["pos"][1] += shift[1]
        component["pos"][2] += shift[2]
    if mode == "components":
        return thing
    else:
        return return_thing

def highlight(thing):
    add_all(thing,"m","#")
    return thing

def color_set(thing, color):
    th = thing
    if "components" in thing:
        th = thing["components"]
    add_all(th, "color", color)
    return thing

def remove_if(thing, name, value):
    return thing

def add_all(thing, name, value):
    if type(thing) == list:
        if "type" not in thing:          
            for component in thing:
                add_all(component, name, value)
    else:
        thing.update({name: value})
    return thing

def inclusion(thing, include):    
    thing2 = []
    for component in thing:
        inclusion = component.get("inclusion", "all")
        if include in inclusion or inclusion == "all":
            component["inclusion"] = include
            thing2.append(component)
            pass
        else:
            pass
    return thing


# ---------------------------------------------------------------------------
# Initialise variables (must be last — set_variable is defined above)
# ---------------------------------------------------------------------------

oobb_variables.initialize_variables()


