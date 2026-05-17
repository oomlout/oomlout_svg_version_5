d = {}


def describe():
    global d
    d = {}
    d["name"] = 'other_ptfe_tube_holder'
    d["name_long"] = 'Other: PTFE Tube Holder'
    d["description"] = 'PTFE tube holder; delegates to oobb_get_items_oobb_other.'
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
    import oobb_get_items_oobb_other

    return oobb_get_items_oobb_other.get_other_ptfe_tube_holder(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="other_ptfe_tube_holder", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
