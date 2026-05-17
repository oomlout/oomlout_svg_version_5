d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bearing_wheel'
    d["name_long"] = 'Other: Bearing Wheel'
    d["description"] = 'Circular wheel with o-ring groove, bearing cutout, and connecting screws.'
    d["category"] = 'Other'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'oring_type', "description": 'O-ring size identifier (drives wheel diameter).', "type": 'string', "default": '"327"'})
    v.append({"name": 'thickness', "description": 'Wheel thickness in mm (9=single, 15=dual bearing).', "type": 'number', "default": 9})
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'bearing_type', "description": 'Bearing type for the central cutout.', "type": 'string', "default": '"606"'})
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

    return oobb_get_items_oobb_old.get_bearing_wheel(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing_wheel", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
