d = {}


def describe():
    global d
    d = {}
    d["name"] = 'shaft_center'
    d["name_long"] = 'Shafts: Shaft Center'
    d["description"] = 'Shaft center geometry; delegates to oobb_get_items_oobb.'
    d["category"] = 'Shafts'
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
    import oobb_get_items_oobb

    return oobb_get_items_oobb.get_shaft_center(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="shaft_center", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
