d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bearing_plate_connecting_screw_center'
    d["name_long"] = 'Bearing Plates: Connecting Screw Center'
    d["description"] = 'Adds countersunk connecting screws at the center zone of a bearing plate.'
    d["category"] = 'Bearing Plates'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'thickness', "description": 'Plate thickness in mm.', "type": 'number', "default": 3})
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'bearing', "description": 'Bearing type identifier, e.g. 6704.', "type": 'string', "default": '"6704"'})
    v.append({"name": 'shaft', "description": 'Shaft type identifier, e.g. m6.', "type": 'string', "default": '"m6"'})
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

    return oobb_get_items_oobb_bearing_plate.get_bearing_plate_connecting_screw_center(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing_plate_connecting_screw_center", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
