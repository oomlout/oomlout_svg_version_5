d = {}


def describe():
    global d
    d = {}
    d["name"] = 'wire_basic_basic_basic_basic'
    d["name_long"] = 'Wire Bundles: Basic+Basic+Basic+Basic'
    d["description"] = 'Four basic wire bundle routing; delegates to oobb_get_items_oobb_wire.'
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

    return oobb_get_items_oobb_wire.get_wire_basic_basic_basic_basic(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="wire_basic_basic_basic_basic", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
