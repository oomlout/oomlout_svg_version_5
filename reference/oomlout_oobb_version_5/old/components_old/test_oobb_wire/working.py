d = {}


def describe():
    global d
    d = {}
    d["name"] = 'test_oobb_wire'
    d["name_long"] = 'Tests: Wire Shape Test'
    d["description"] = 'Wire shape test fixtures across all wire styles and rotation variants.'
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

    kwargs.pop("style", "")
    pos = kwargs.get("pos", [0, 0, 0])
    full_object = kwargs.get("full_object", True)

    kwargs["pos"] = pos

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size", "")
    kwargs.pop("extra", "")
    kwargs.pop("type", "")

    pos_shift = 60

    versions = []
    styles = ["motor", "motor_stepper", "basic", "higher_voltage", "i2c", "spacer"]

    for style in styles:
        base = {}
        base["shape"] = f"oobb_wire_{style}"
        base["comment_extra"] = ""
        base["comment_display"] = True
        base["extra"] = {}
        versions.append(copy.deepcopy(base))

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

            p3["comment"] = f"{v['shape']}_\n{comment_extra}{comment_extra_extra}"
            p3["comment_display"] = v.get("comment_display", False)
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
        result = action(type="test_oobb_wire", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
