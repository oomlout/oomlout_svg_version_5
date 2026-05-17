d = {}


def describe():
    global d
    d = {}
    d["name"] = 'smd_magazine_large'
    d["name_long"] = 'SMD Magazines: Large'
    d["description"] = 'Large SMD magazine tray.'
    d["category"] = 'SMD Magazines'
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

    return oobb_get_items_oobb_old.get_smd_magazine_large(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="smd_magazine_large", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
