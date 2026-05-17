d = {}


def describe():
    global d
    d = {}
    d["name"] = 'pulley_gt2_shield_double'
    d["name_long"] = 'Other: GT2 Double Shield Pulley'
    d["description"] = 'GT2 pulley with double side shields; delegates to oobb_get_items_oobb.'
    d["category"] = 'Other'
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

    return oobb_get_items_oobb.get_pulley_gt2_shield_double(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="pulley_gt2_shield_double", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
