d = {}


def describe():
    global d
    d = {}
    d["name"] = 'wires'
    d["name_long"] = 'Part Sets: Wires'
    d["description"] = 'Dispatches to get_wire_<extra> in oobb_get_items_oobb_wire; requires non-empty extra.'
    d["category"] = 'Part Sets'
    d["shape_aliases"] = []
    d["returns"] = 'List of part definition dicts.'
    v = []
    v.append({"name": 'extra', "description": 'Wire sub-type selector (joined with _ if list).', "type": 'string', "default": '(required)'})
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

    getter = getattr(oobb_make_sets, "get_wires")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import copy

    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    p3.pop("extra")
    p3["type"] = f"wire_{extra}"
    if extra != "":
        if type(extra) == list:
            extra = "_".join(extra)
        current_module = __import__("oobb_get_items_oobb_wire")
        function_name = "get_wire_" + extra
        try:
            function_to_call = getattr(current_module, function_name)
        except:
            function_to_call = getattr(current_module, "get_oobb_wire_base")
        return function_to_call(**kwargs)
    else:
        raise Exception("No extra")


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="wire", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
