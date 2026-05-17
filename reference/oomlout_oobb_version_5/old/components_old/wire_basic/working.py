d = {}


def describe():
    global d
    d = {}
    d["name"] = 'wire_basic'
    d["name_long"] = 'Wire Bundles: Basic 3-Wire'
    d["description"] = '3-wire basic bundle routing (basic+basic+basic); delegates to oobb_get_items_oobb_wire.'
    d["category"] = 'Wire Bundles'
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
    import oobb_get_items_oobb_wire

    return oobb_get_items_oobb_wire.get_wire_basic(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="wire_basic", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
