d = {}


def describe():
    global d
    d = {}
    d["name"] = 'test_oobb_screw_socket_cap_old_1'
    d["name_long"] = 'Tests: Socket Cap Screw Test (Legacy)'
    d["description"] = 'Legacy inline screw socket-cap test fixture.'
    d["category"] = 'Tests'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
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
    """Build and return the thing dict for this object type."""
    import copy
    import oobb_base

    pos = kwargs.get("pos", [0, 0, 0])
    full_object = kwargs.get("full_object", True)

    kwargs["pos"] = pos

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size", "")
    kwargs.pop("extra", "")

    pos_current = [0, 0, 0]
    pos_shift = 30
    comment_extra = ""

    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom nut : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["clearance"] = "bottom"
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom nut : True clearance : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["rot_y"] = 180
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nzz : bottom nut : True rot_y : 180"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : top"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : bottom nut : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = ["top", "bottom"]
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : [bottom , top] nut : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = ["top", "bottom"]
    p4["zz"] = "top"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : [bottom , top] nut : True zz : top"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "bottom"
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}{comment_extra}\nclearance : bottom nut : True zz : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current = [300, 0, 0]
    pos_shift = 30
    comment_extra = " rot_y : 180"

    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_y"] = 180
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : top"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "bottom"
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True zz : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current = [600, 0, 0]
    pos_shift = 30
    comment_extra = " rot_y : 90"

    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_y"] = 90
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : top"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["clearance"] = "bottom"
    p4["zz"] = "bottom"
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nclearance : bottom nut : True zz : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current = [900, 0, 0]
    pos_shift = 60
    comment_extra = " rot_x : 180"

    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_x"] = 180
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current = [1200, 0, 0]
    pos_shift = 60
    comment_extra = " rot_x : -90"

    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_x"] = -90
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4)

    pos_current = [1500, 0, 0]
    pos_shift = 60
    comment_extra = " rot_x : 90 rot_y : 90 rot_z : 90"

    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}\n{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_x"] = 90
    p3["rot_y"] = 90
    p3["rot_z"] = 90
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["nut"] = True
    p4["overhang"] = True
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nnut : True, overhang : True"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "top"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : top"
    oobb_base.append_full(thing, **p4)

    pos_current[1] += pos_shift
    p4 = copy.deepcopy(p3)
    p4["zz"] = "bottom"
    p4["pos"] = copy.deepcopy(pos_current)
    p4["comment"] = f"{item}\n{comment_extra}\nzz : bottom"
    oobb_base.append_full(thing, **p4)

    if full_object:
        return thing
    else:
        return thing["components"]


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="test_oobb_screw_socket_cap_old_1", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
