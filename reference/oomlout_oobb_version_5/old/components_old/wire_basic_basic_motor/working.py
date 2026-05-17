d = {}


def describe():
    global d
    d = {}
    d["name"] = 'wire_basic_basic_motor'
    d["name_long"] = 'Wire Bundles: Basic+Basic+Motor'
    d["description"] = 'Two basic wires and one motor wire bundle routing.'
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

    return oobb_get_items_oobb_wire.get_wire_basic_basic_motor(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="wire_basic_basic_motor", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
