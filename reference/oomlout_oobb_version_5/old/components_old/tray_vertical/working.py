d = {}


def describe():
    global d
    d = {}
    d["name"] = 'tray_vertical'
    d["name_long"] = 'Trays: Vertical Tray'
    d["description"] = 'Vertically-oriented tray.'
    d["category"] = 'Trays'
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

    return oobb_get_items_oobb_old.get_tray_vertical(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="tray_vertical", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
