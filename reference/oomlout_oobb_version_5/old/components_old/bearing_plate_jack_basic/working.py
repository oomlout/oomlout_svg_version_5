d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bearing_plate_jack_basic'
    d["name_long"] = 'Bearing Plates: Jack Basic'
    d["description"] = 'Legacy bearing-plate with a basic jack (simpler variant, includes 3D-print slice logic).'
    d["category"] = 'Bearing Plates'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
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

    return oobb_get_items_oobb_old.get_bearing_plate_jack_basic(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing_plate_jack_basic", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
