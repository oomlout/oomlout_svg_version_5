d = {}


def describe():
    global d
    d = {}
    d["name"] = 'nut_m3'
    d["name_long"] = 'Fasteners: M3 Nut'
    d["description"] = "M3 nut pocket with optional through-hole; wrapper over oobb_nut with radius_name='m3'."
    d["category"] = 'Fasteners'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'hole', "description": 'Include a through-hole.', "type": 'bool', "default": False})
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
    import oobb_get_items_other

    return oobb_get_items_other.get_nut_m3(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="nut_m3", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
