d = {}


def describe():
    global d
    d = {}
    d["name"] = 'others'
    d["name_long"] = 'Part Sets: Others'
    d["description"] = 'Dispatches to get_other_<extra> in oobb_get_items_oobb_other; requires a non-empty extra field.'
    d["category"] = 'Part Sets'
    d["shape_aliases"] = ['ots']
    d["returns"] = 'List of part definition dicts.'
    v = []
    v.append({"name": 'extra', "description": 'Selects which get_other_* function to call.', "type": 'string', "default": '(required)'})
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
    ots = []

    ots.append({"type": "other", "extra": "timing_belt_clamp_gt2", "width": 2.5, "height": 1.5, "thickness": 14, "size": size})
    ots.append({"type": "other", "extra": "timing_belt_clamp_gt2", "width": 2.5, "height": 1.5, "thickness": 6, "size": size})

    ots.append({"type": "other", "extra": "corner_cube", "width": 2, "height": 2, "thickness": 29, "size": size})

    ots.append({"type": "other", "extra": "bolt_stacker", "diameter": 1.5, "thickness": 24, "size": size})
    ots.append({"type": "other", "extra": "bolt_stacker", "width": 1, "height": 6, "thickness": 3, "size": size})

    heights = [7, 5, 3]
    shafts = ["m6", "quarter_inch_pipe_thread"]
    for h in heights:
        for s in shafts:
            ots.append({"type": "other", "extra": "ptfe_tube_holder", "width": 1, "height": h, "thickness": 14, "size": size, "shaft": s})
            ots.append({"type": "other", "extra": "ptfe_tube_holder_ninety_degree", "width": 1, "height": h, "thickness": 14, "size": size, "shaft": s})

    return ots


def test(**kwargs):
    result = items(**kwargs)
    return isinstance(result, list) and len(result) >= 1 and all(isinstance(item, dict) for item in result)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import copy

    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    p3.pop("extra")
    p3["type"] = f"holder_{extra}"
    if extra != "":
        current_module = __import__("oobb_get_items_oobb_other")
        function_name = "get_other_" + extra
        function_to_call = getattr(current_module, function_name)
        return function_to_call(**kwargs)
    else:
        raise Exception("No extra")


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="other", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
