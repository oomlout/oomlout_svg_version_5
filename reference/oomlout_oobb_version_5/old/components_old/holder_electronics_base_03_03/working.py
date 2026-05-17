d = {}


def describe():
    global d
    d = {}
    d["name"] = 'holder_electronics_base_03_03'
    d["name_long"] = 'Holders: Electronics Base 3×3'
    d["description"] = '3×3-unit electronics base plate holder.'
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

    return oobb_get_items_oobb_old.get_holder_electronics_base_03_03(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_electronics_base_03_03", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
