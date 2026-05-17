d = {}


def describe():
    global d
    d = {}
    d["name"] = 'holder_motor_stepper_nema_17_flat_shifted_spacer_10_mm'
    d["name_long"] = 'Holders: NEMA-17 Stepper Motor (Flat Shifted 10mm Spacer)'
    d["description"] = '10 mm spacer variant of the shifted flat NEMA-17 holder.'
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

    return oobb_get_items_oobb_holder.get_holder_motor_stepper_nema_17_flat_shifted_spacer_10_mm(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_motor_stepper_nema_17_flat_shifted_spacer_10_mm", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
