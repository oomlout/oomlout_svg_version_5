d = {}


def describe():
    global d
    d = {}
    d["name"] = 'test_rotation'
    d["name_long"] = 'Tests: Rotation Test Fixtures'
    d["description"] = 'Rotation/transform debug fixtures for item orientation verification.'
    d["category"] = 'Tests'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'thickness', "description": 'Fixture thickness in mm.', "type": 'number', "default": 3})
    v.append({"name": 'size', "description": 'Grid system: oobb or oobe.', "type": 'string', "default": '"oobb"'})
    v.append({"name": 'holes', "description": 'Include reference holes.', "type": 'bool', "default": True})
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

    thickness = kwargs.get("thickness", 3)
    kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)

    kwargs.get("holes", True)
    kwargs.get("both_holes", False)
    kwargs["pos"] = pos

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size", "")
    kwargs.pop("extra", "")

    pos_current = [0, 0, 0]
    comment_extra = ""

    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)

    pos_current = [300, 0, 0]
    comment_extra = " rot_y : 180"

    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_y"] = 180
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)

    if full_object:
        return thing
    else:
        return thing["components"]


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="test_rotation", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
