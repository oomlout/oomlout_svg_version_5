d = {}


def describe():
    global d
    d = {}
    d["name"] = 'ci_holes_center'
    d["name_long"] = 'Circles: Intercardinal Holes Center'
    d["description"] = 'Adds M3 holes and/or slots at the center intercardinal positions of a circular part.'
    d["category"] = 'Circles'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'slots', "description": 'Add slot cutouts on the X axis.', "type": 'bool', "default": True})
    v.append({"name": 'holes', "description": 'Add hole cutouts on the Y axis.', "type": 'bool', "default": True})
    v.append({"name": 'inserts', "description": 'Add threaded insert pockets instead of holes.', "type": 'bool', "default": False})
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

    return oobb_get_items_oobb_old.get_ci_holes_center(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="ci_holes_center", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
