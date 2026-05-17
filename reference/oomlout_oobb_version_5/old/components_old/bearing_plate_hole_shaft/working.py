d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bearing_plate_hole_shaft'
    d["name_long"] = 'Bearing Plates: Shaft Hole'
    d["description"] = 'Cuts the central shaft hole in a bearing plate; shape varies by shaft type.'
    d["category"] = 'Bearing Plates'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'width', "description": 'Plate width in OOBB units.', "type": 'number', "default": 1})
    v.append({"name": 'height', "description": 'Plate height in OOBB units.', "type": 'number', "default": 1})
    v.append({"name": 'thickness', "description": 'Plate thickness in mm.', "type": 'number', "default": 3})
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'shaft', "description": 'Shaft type: m6, coupler_flanged, motor_tt_01, motor_servo_standard_01, etc.', "type": 'string', "default": '"m6"'})
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
    v.append({"name": 'bearing', "description": 'Bearing type identifier.', "type": 'string', "default": '"608"'})
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

    return oobb_get_items_oobb_bearing_plate.get_bearing_plate_hole_shaft(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing_plate_hole_shaft", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
