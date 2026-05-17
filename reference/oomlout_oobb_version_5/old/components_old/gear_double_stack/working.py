d = {}


def describe():
    global d
    d = {}
    d["name"] = 'gear_double_stack'
    d["name_long"] = 'Gears: Double Stack Gear'
    d["description"] = 'Stacks two gear layers (each half the total thickness) with per-layer diameter and extra settings.'
    d["category"] = 'Gears'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'diameter', "description": 'List of two diameters (one per gear layer) in OOBB units.', "type": 'list', "default": 1})
    v.append({"name": 'thickness', "description": 'Total gear stack thickness in mm (split equally).', "type": 'number', "default": 3})
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
    v.append({"name": 'shaft', "description": 'Shaft type.', "type": 'string', "default": '"m6"'})
    v.append({"name": 'holes', "description": 'Add holes to each layer.', "type": 'bool', "default": True})
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
    import oobb_get_items_oobb

    return oobb_get_items_oobb.get_gear_double_stack(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="gear_double_stack", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
