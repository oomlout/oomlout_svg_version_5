d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bearing_plates'
    d["name_long"] = 'Part Sets: Bearing Plates'
    d["description"] = 'Delegates to get_bearing_plate for bearing plate geometry.'
    d["category"] = 'Part Sets'
    d["shape_aliases"] = []
    d["returns"] = 'List of part definition dicts.'
    v = []
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

    getter = getattr(oobb_make_sets, "get_bearing_plates")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_bearing_plate

    return oobb_get_items_oobb_bearing_plate.get_bearing_plate(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing_plate", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
