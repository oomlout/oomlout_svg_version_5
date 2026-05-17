d = {}


def describe():
    global d
    d = {}
    d["name"] = 'test_motor_tt_01'
    d["name_long"] = 'Tests: TT Motor Fit Test'
    d["description"] = 'TT motor fit-test fixtures for body clearances.'
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

    pos_current = [0, 0, 0]
    pos_shift = 15

    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "oobb_plate"
    p3["type"] = "p"
    p3["width"] = 1.5
    p3["height"] = 5
    p3["depth"] = 7
    pos1 = copy.deepcopy(p3["pos"])
    pos1[2] += -6
    p3["pos"] = pos1

    versions = []
    base = {}
    base["type"] = "p"
    base["shape"] = "oobb_motor_tt_01"
    base.pop("clearance", "")
    base["pos"] = pos_current
    base["comment_extra"] = ""
    base["comment_shift_line"] = 30
    base["extra"] = {}

    versions.append(copy.deepcopy(base))

    tests = {}
    tests["radius_extra"] = [0]
    a_extra = "radius_extra"

    for a in tests[a_extra]:
        for v in versions:
            p3 = copy.deepcopy(v)
            comment_extra = v["comment_extra"]
            comment_extra += f" {a_extra} : {a}\n"

            extra_detail_a = a
            p3["comment"] = f"{v['shape']}_{a}_{extra_detail_a}\n{comment_extra}"
            p3["pos"] = copy.deepcopy(pos_current)
            p3[a_extra] = a
            extra = v.get("extra", {})
            p3.update(extra)
            oobb_base.append_full(thing, **p3)
            pos_current[1] += pos_shift
    pos_current[0] += pos_shift
    pos_current[1] = 0

    if full_object:
        return thing
    else:
        return thing["components"]


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="test_motor_tt_01", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
