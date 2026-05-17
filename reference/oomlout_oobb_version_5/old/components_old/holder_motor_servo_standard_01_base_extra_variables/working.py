d = {}


def describe():
    global d
    d = {}
    d["name"] = 'holder_motor_servo_standard_01_base_extra_variables'
    d["name_long"] = 'Holders: Standard Servo Motor (Base Extra Variables)'
    d["description"] = 'Base sub-part of the standard servo holder with extra configurable variables.'
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

    return oobb_get_items_oobb_holder.get_holder_motor_servo_standard_01_base_extra_variables(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_motor_servo_standard_01_base_extra_variables", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
