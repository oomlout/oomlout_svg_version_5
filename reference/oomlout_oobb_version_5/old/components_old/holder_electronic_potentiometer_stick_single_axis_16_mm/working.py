d = {}


def describe():
    global d
    d = {}
    d["name"] = 'holder_electronic_potentiometer_stick_single_axis_16_mm'
    d["name_long"] = 'Holders: 16mm Single-Axis Joystick'
    d["description"] = 'Holder for a single-axis 16 mm joystick-style potentiometer.'
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

    return oobb_get_items_oobb_holder.get_holder_electronic_potentiometer_stick_single_axis_16_mm(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_electronic_potentiometer_stick_single_axis_16_mm", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
