d = {}


def describe():
    global d
    d = {}
    d["name"] = 'jack_basic'
    d["name_long"] = 'Other: Jack Basic'
    d["description"] = 'Legacy jack component — a plate with an extending cube tab and M6 bolt holes for wall-mounting.'
    d["category"] = 'Other'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'width', "description": 'Width in OOBB units.', "type": 'number', "default": 2})
    v.append({"name": 'height', "description": 'Height in OOBB units.', "type": 'number', "default": 2})
    v.append({"name": 'thickness', "description": 'Plate thickness in mm.', "type": 'number', "default": 3})
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

    return oobb_get_items_oobb_old.get_jack_basic(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="jack_basic", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
