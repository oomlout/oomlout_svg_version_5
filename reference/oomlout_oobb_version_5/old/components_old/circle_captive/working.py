d = {}


def describe():
    global d
    d = {}
    d["name"] = 'circle_captive'
    d["name_long"] = 'Circles: Circle Captive'
    d["description"] = 'Circular geometry with a captive shaft hole and press-fit M3/M6 nuts around the perimeter.'
    d["category"] = 'Circles'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'shaft', "description": 'Shaft type used to cut the captive hole.', "type": 'string', "default": '""'})
    v.append({"name": 'diameter', "description": 'Circle diameter in OOBB units.', "type": 'number', "default": 1})
    v.append({"name": 'thickness', "description": 'Circle thickness in mm.', "type": 'number', "default": 3})
    v.append({"name": 'holes', "description": 'Add perimeter holes.', "type": 'bool', "default": True})
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

    return oobb_get_items_oobb_old.get_circle_captive(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="circle_captive", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
