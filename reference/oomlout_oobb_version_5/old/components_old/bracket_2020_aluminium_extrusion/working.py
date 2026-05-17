d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bracket_2020_aluminium_extrusion'
    d["name_long"] = 'Other: 2020 Aluminium Extrusion Bracket'
    d["description"] = 'Bracket plate with M6 and intermediate holes for attaching to 2020 aluminium extrusion.'
    d["category"] = 'Other'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'width', "description": 'Bracket width in OOBB units.', "type": 'number', "default": 10})
    v.append({"name": 'height', "description": 'Bracket height in OOBB units.', "type": 'number', "default": 10})
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

    return oobb_get_items_oobb_old.get_bracket_2020_aluminium_extrusion(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bracket_2020_aluminium_extrusion", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
