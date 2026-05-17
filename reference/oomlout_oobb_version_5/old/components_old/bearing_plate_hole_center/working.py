d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bearing_plate_hole_center'
    d["name_long"] = 'Bearing Plates: Hole Center'
    d["description"] = 'Adds center-zone fastener holes (M3 holes/nuts or circle pattern) matching the bearing type.'
    d["category"] = 'Bearing Plates'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'shaft', "description": 'Shaft type identifier.', "type": 'string', "default": '"m6"'})
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
    v.append({"name": 'thickness', "description": 'Plate thickness in mm.', "type": 'number', "default": 3})
    v.append({"name": 'bearing', "description": 'Bearing type identifier.', "type": 'string', "default": '"6704"'})
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
    import oobb_get_items_oobb_bearing_plate

    return oobb_get_items_oobb_bearing_plate.get_bearing_plate_hole_center(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing_plate_hole_center", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
