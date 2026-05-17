d = {}


def describe():
    global d
    d = {}
    d["name"] = 'holder_motor_gearmotor_01'
    d["name_long"] = 'Holders: Gearmotor'
    d["description"] = 'Gearmotor holder (revision 01).'
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

    return oobb_get_items_oobb_old.get_holder_motor_gearmotor_01(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_motor_gearmotor_01", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
