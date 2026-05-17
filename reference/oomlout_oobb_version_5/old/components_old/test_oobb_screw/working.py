d = {}


def describe():
    global d
    d = {}
    d["name"] = 'test_oobb_screw'
    d["name_long"] = 'Tests: Screw Test Fixtures'
    d["description"] = 'Screw test fixtures across orientation, nut, and clearance variants.'
    d["category"] = 'Tests'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'style', "description": 'Screw style: socket_cap, countersunk, self_tapping.', "type": 'string', "default": '"socket_cap"'})
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

    style = kwargs.get("style", "socket_cap")
    kwargs.pop("style", "")
    pos = kwargs.get("pos", [0, 0, 0])
    full_object = kwargs.get("full_object", True)

    kwargs["pos"] = pos

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size", "")
    kwargs.pop("extra", "")
    kwargs.pop("type", "")

    pos_shift = 30

    versions = []
    base = {}
    base["shape"] = f"oobb_screw_{style}"
    base["radius_name"] = "m3"
    base["depth"] = 12
    base["comment_extra"] = ""
    base["comment_display"] = True
    base["extra"] = {}

    versions.append(copy.deepcopy(base))

    b = copy.deepcopy(base)
    b["extra"]["nut"] = True
    b["comment_extra"] = "nut : True"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["nut"] = True
    b["extra"]["overhang"] = True
    b["comment_extra"] = "nut : True overhang : True"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["zz"] = "top"
    b["comment_extra"] = "zz : top"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["zz"] = "bottom"
    b["comment_extra"] = "zz : bottom"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["zz"] = "top"
    b["extra"]["nut"] = True
    b["comment_extra"] = "zz : top nut : True"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["zz"] = "bottom"
    b["extra"]["nut"] = True
    b["comment_extra"] = "zz : bottom nut : True"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["zz"] = "bottom"
    b["extra"]["nut"] = True
    b["extra"]["rot_y"] = 180
    b["comment_extra"] = "zz : top nut : True rot_y : 180"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["clearance"] = "top"
    b["comment_extra"] = "clearance : top"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["clearance"] = "bottom"
    b["comment_extra"] = "clearance : bottom"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["clearance"] = "bottom"
    b["extra"]["nut"] = True
    b["comment_extra"] = "clearance : bottom nut : True"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["clearance"] = ["top", "bottom"]
    b["extra"]["nut"] = True
    b["comment_extra"] = "clearance : [top , bottom] nut : True"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["clearance"] = ["top", "bottom"]
    b["extra"]["nut"] = True
    b["extra"]["zz"] = "top"
    b["comment_extra"] = "clearance : [top , bottom] nut : True zz : top"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["clearance"] = ["top", "bottom"]
    b["extra"]["nut"] = True
    b["extra"]["zz"] = "bottom"
    b["comment_extra"] = "clearance : [top , bottom] nut : True zz : bottom"
    versions.append(b)

    rots = []
    rots.append([[0, 0, 0], {}, ""])
    rots.append([[150, 0, 0], {"rot_y": 180}, "rot_y : 180"])
    rots.append([[300, 0, 0], {"rot_y": 90}, "rot_y : 90"])
    rots.append([[450, 0, 0], {"rot_x": 45, "rot_y": 45}, "rot_x : 90 rot_y : 45"])

    for r in rots:
        pos_current = r[0]
        extra_extra = r[1]
        comment_extra_extra = r[2]

        for v in versions:
            p3 = copy.deepcopy(kwargs)
            comment_extra = v["comment_extra"]
            p3["shape"] = v["shape"]
            p3["type"] = "positive"
            radius_name = v["radius_name"]
            p3["radius_name"] = radius_name
            depth = v["depth"]
            p3["depth"] = depth
            p3["comment"] = f"{v['shape']}_{radius_name}_{depth}\n{comment_extra}{comment_extra_extra}"
            comment_display = v.get("comment_display", False)
            p3["comment_display"] = comment_display
            p3["pos"] = copy.deepcopy(pos_current)
            p3["m"] = ""
            p3.update(v["extra"])
            p3.update(extra_extra)
            oobb_base.append_full(thing, **p3)
            pos_current[1] += pos_shift

    if full_object:
        return thing
    else:
        return thing["components"]


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="test_oobb_screw", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
