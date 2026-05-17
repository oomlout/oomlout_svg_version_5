d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bearing_circles'
    d["name_long"] = 'Part Sets: Bearing Circles'
    d["description"] = 'Delegates to the legacy get_bearing_circle function for bearing circle geometry.'
    d["category"] = 'Part Sets'
    d["shape_aliases"] = ['bcs']
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
    bcs = []
    bcs.append({"type": "bearing_circle", "diameter": 3, "thickness": 12, "bearing": "606", "size": size})
    return bcs


def test(**kwargs):
    result = items(**kwargs)
    return isinstance(result, list) and len(result) >= 1 and isinstance(result[0], dict)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_bearing_circle(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing_circle", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
