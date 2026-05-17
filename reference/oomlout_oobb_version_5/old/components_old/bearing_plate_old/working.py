d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bearing_plate_old'
    d["name_long"] = 'Bearing Plates: Legacy Bearing Plate'
    d["description"] = 'Legacy monolithic bearing plate builder with full hole/shaft/bearing patterns in one call.'
    d["category"] = 'Bearing Plates'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'shaft', "description": 'Shaft type identifier.', "type": 'string', "default": '"m6"'})
    v.append({"name": 'radius_name', "description": 'Hole radius name for perimeter holes.', "type": 'string', "default": '"m6"'})
    v.append({"name": 'width', "description": 'Plate width in OOBB units.', "type": 'number', "default": '""'})
    v.append({"name": 'height', "description": 'Plate height in OOBB units.', "type": 'number', "default": '""'})
    v.append({"name": 'thickness', "description": 'Plate thickness in mm.', "type": 'number', "default": '""'})
    v.append({"name": 'bearing_type', "description": 'Bearing type identifier.', "type": 'string', "default": '"608"'})
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
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

    return oobb_get_items_oobb_old.get_bearing_plate_old(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing_plate_old", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
