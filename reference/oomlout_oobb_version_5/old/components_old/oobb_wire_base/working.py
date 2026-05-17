d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_wire_base'
    d["name_long"] = 'OOBB Wire Cutouts: Wire Base'
    d["description"] = 'Base wire cutout delegate; forwards all kwargs to the legacy wire builder.'
    d["category"] = 'OOBB Wire Cutouts'
    d["shape_aliases"] = ['wire_base']
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
    import oobb_get_items_oobb_wire

    return oobb_get_items_oobb_wire.get_oobb_wire_base(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="oobb_wire_base", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
