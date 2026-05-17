d = {}


def describe():
    global d
    d = {}
    d["name"] = 'holder_motor_generic'
    d["name_long"] = 'Holders: Generic Motor'
    d["description"] = 'Generic configurable motor holder.'
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
    import oobb_get_items_oobb_holder

    return oobb_get_items_oobb_holder.get_holder_motor_generic(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_motor_generic", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
