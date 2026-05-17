d = {}


def describe():
    global d
    d = {}
    d["name"] = 'jig_screw_sorter_m3_03_03'
    d["name_long"] = 'Jigs: M3 Screw Sorter (3×3)'
    d["description"] = 'Tray jig with a grid of M3 countersunk screw sorter holes, 3×3 OOBB tray base.'
    d["category"] = 'Jigs'
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

    return oobb_get_items_oobb_old.get_jig_screw_sorter_m3_03_03(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="jig_screw_sorter_m3_03_03", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
