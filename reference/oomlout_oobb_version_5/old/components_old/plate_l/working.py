d = {}


def describe():
    global d
    d = {}
    d["name"] = 'plate_l'
    d["name_long"] = 'Plates: L-Shaped Plate'
    d["description"] = 'L-shaped plate geometry; delegates to oobb_get_items_oobb.get_plate_l.'
    d["category"] = 'Plates'
    d["shape_aliases"] = ['plate_l']
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
    import oobb_get_items_oobb

    return oobb_get_items_oobb.get_plate_l(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate_l", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
