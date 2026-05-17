d = {}


def describe():
    global d
    d = {}
    d["name"] = 'plates'
    d["name_long"] = 'Part Sets: Plates'
    d["description"] = 'Dispatches to get_plate_<extra> or falls back to get_plate_base for rectangular plates.'
    d["category"] = 'Part Sets'
    d["shape_aliases"] = []
    d["returns"] = 'List of part definition dicts.'
    v = []
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
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

    getter = getattr(oobb_make_sets, "get_plates")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import copy
    import importlib
    import sys

    import oobb_get_items_oobb

    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    p3.pop("extra", "")
    p3["type"] = f"plate_{extra}"
    if extra != "":
        function_name = "get_plate_" + extra
        importlib.reload(sys.modules[oobb_get_items_oobb.__name__])
        try:
            function_to_call = getattr(sys.modules[oobb_get_items_oobb.__name__], function_name)
            return function_to_call(**kwargs)
        except Exception:
            print(f"Function {function_name} not found using basic plate")
            return oobb_get_items_oobb.get_plate_base(**kwargs)
    else:
        return oobb_get_items_oobb.get_plate_base(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
