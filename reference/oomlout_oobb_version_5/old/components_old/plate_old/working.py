d = {}


def describe():
    global d
    d = {}
    d["name"] = 'plate_old'
    d["name_long"] = 'Plates: Plate (Legacy)'
    d["description"] = 'Legacy plate builder; delegates to get_plate_old.'
    d["category"] = 'Plates'
    d["shape_aliases"] = ['plate_old']
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

    return oobb_get_items_oobb_old.get_plate_old(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate_old", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
