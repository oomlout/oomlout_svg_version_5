d = {}


def describe():
    global d
    d = {}
    d["name"] = 'test_oobb_motor_servo_standard_01'
    d["name_long"] = 'Tests: Standard Servo Orientation Test'
    d["description"] = 'Servo orientation and screw-rotation test fixtures for standard servo profiles.'
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
    kwargs.pop("type", "")

    pos_current = [0, 0, 0]
    pos_shift = 150

    versions = []
    base = {}
    base["shape"] = "oobb_motor_servo_standard_01"
    base["comment_extra"] = ""
    base["m"] = ""
    base["extra"] = {}

    versions.append(copy.deepcopy(base))

    b = copy.deepcopy(base)
    b["extra"]["rot_y"] = 180
    b["comment_extra"] = " rot_y : 180"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["rot_y"] = 90
    b["comment_extra"] = " rot_y : 90"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["rot_x"] = 90
    b["comment_extra"] = " rot_x : 90"
    versions.append(b)

    b = copy.deepcopy(base)
    b["extra"]["screw_rot_y"] = True
    b["comment_extra"] = " screw_rot_y : True"
    versions.append(b)

    for v in versions:
        p3 = copy.deepcopy(kwargs)
        comment_extra = v["comment_extra"]
        p3["shape"] = v["shape"]
        p3["type"] = "positive"
        p3["comment"] = f"{v['shape']}{comment_extra}\n"
        p3["pos"] = copy.deepcopy(pos_current)
        p3["m"] = ""
        p3.update(v["extra"])
        oobb_base.append_full(thing, **p3)
        pos_current[1] += pos_shift

    if full_object:
        return thing
    else:
        return thing["components"]


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="test_oobb_motor_servo_standard_01", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
