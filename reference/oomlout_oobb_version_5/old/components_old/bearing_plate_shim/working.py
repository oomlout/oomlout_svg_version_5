d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bearing_plate_shim'
    d["name_long"] = 'Bearing Plates: Shim'
    d["description"] = "Thin shim ring sized to fit between a bearing's OD catch and ID."
    d["category"] = 'Bearing Plates'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'bearing_type', "description": 'Bearing type identifier.', "type": 'string', "default": '"6803"'})
    v.append({"name": 'thickness', "description": 'Shim thickness in mm.', "type": 'number', "default": 3})
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

    return oobb_get_items_oobb_old.get_bearing_plate_shim(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing_plate_shim", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
