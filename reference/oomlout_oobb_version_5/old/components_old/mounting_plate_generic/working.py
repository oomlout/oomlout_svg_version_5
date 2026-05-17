d = {}


def describe():
    global d
    d = {}
    d["name"] = 'mounting_plate_generic'
    d["name_long"] = 'Holders: Generic Mounting Plate'
    d["description"] = 'Generic configurable mounting plate with OOBB hole patterns.'
    d["category"] = 'Holders'
    d["shape_aliases"] = []
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
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_mounting_plate_generic(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="mounting_plate_generic", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
