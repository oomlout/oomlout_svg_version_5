d = {}


def describe():
    global d
    d = {}
    d["name"] = 'plate_nut_dict'
    d["name_long"] = 'Plates: Plate Nut Dict'
    d["description"] = 'Delegates to oobb_get_items_oobb_wire.get_plate_nut_dict.'
    d["category"] = 'Plates'
    d["shape_aliases"] = ['plate_nut_dict']
    d["returns"] = 'List of geometry component dicts.'
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
def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_wire

    return oobb_get_items_oobb_wire.get_plate_nut_dict(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate_nut_dict", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
