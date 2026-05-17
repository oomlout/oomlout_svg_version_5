d = {}


def describe():
    global d
    d = {}
    d["name"] = 'ziptie_holder_jack'
    d["name_long"] = 'Other: Ziptie Holder Jack'
    d["description"] = 'Ziptie holder jack component; delegates to oobb_get_items_oobb_old.'
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
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_ziptie_holder_jack(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="ziptie_holder_jack", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
