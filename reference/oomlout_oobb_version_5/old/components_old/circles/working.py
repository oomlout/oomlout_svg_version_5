d = {}


def describe():
    global d
    d = {}
    d["name"] = 'circles'
    d["name_long"] = 'Part Sets: Circles'
    d["description"] = 'Dispatches to a get_plate_<extra> function or falls back to get_circle_base based on the extra field.'
    d["category"] = 'Part Sets'
    d["shape_aliases"] = ['circle']
    d["returns"] = 'List of part definition dicts.'
    v = []
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
    v.append({"name": 'thickness', "description": 'Plate depth used to compute z-position offsets.', "type": 'number', "default": 3})
    v.append({"name": 'zz', "description": 'Vertical anchor: bottom, middle, top.', "type": 'string', "default": '"bottom"'})
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
def items(size="oobb", **kwargs):
    import oobb_make_sets

    getter = getattr(oobb_make_sets, "get_circles")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)


def action(**kwargs):
    """Build and return the circle thing dict."""
    import copy
    import importlib
    import sys

    import oobb_get_items_oobb

    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    thickness = p3.get("thickness", 3)
    zz = p3.get("zz", "bottom")
    pos = p3.get("pos", [0, 0, 0])
    p3.pop("extra", "")
    p3["type"] = f"plate_{extra}"

    if zz == "bottom":
        pos[2] += 0
    elif zz == "middle":
        pos[2] += -thickness / 2
    elif zz == "top":
        pos[2] += -thickness

    if extra != "" and "doughnut" not in extra:
        function_name = "get_plate_" + extra
        importlib.reload(sys.modules[oobb_get_items_oobb.__name__])
        function_to_call = getattr(sys.modules[oobb_get_items_oobb.__name__], function_name)
        return function_to_call(**kwargs)
    else:
        return oobb_get_items_oobb.get_circle_base(**kwargs)


def test(**kwargs):
    """Smoke test: verify action() returns a well-formed thing dict."""
    try:
        result = action(diameter=3, thickness=3, size="oobb", type="circle")
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
