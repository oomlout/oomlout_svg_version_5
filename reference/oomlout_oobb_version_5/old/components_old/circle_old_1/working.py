d = {}


def describe():
    global d
    d = {}
    d["name"] = 'circle_old_1'
    d["name_long"] = 'Circles: Circle (Legacy)'
    d["description"] = 'Legacy circular geometry builder with optional holes, both-holes, extra nut, and center-hole patterns.'
    d["category"] = 'Circles'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'diameter', "description": 'Circle diameter in OOBB units.', "type": 'number', "default": 1})
    v.append({"name": 'thickness', "description": 'Circle thickness in mm.', "type": 'number', "default": 3})
    v.append({"name": 'holes', "description": 'Add standard hole patterns.', "type": 'bool', "default": True})
    v.append({"name": 'both_holes', "description": 'Also add oobe (intermediate) holes.', "type": 'bool', "default": False})
    v.append({"name": 'exclude_d3_holes', "description": 'Skip diagonal 45° holes on diameter-3 circles.', "type": 'bool', "default": False})
    v.append({"name": 'exclude_center_holes', "description": 'Skip center-region holes.', "type": 'bool', "default": False})
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
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

    return oobb_get_items_oobb_old.get_circle_old_1(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="circle_old_1", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
