d = {}


def describe():
    global d
    d = {}
    d["name"] = 'jigs'
    d["name_long"] = 'Part Sets: Jigs'
    d["description"] = 'Delegates to the legacy get_jig function; extra field selects the sub-type.'
    d["category"] = 'Part Sets'
    d["shape_aliases"] = ['jgs']
    d["returns"] = 'List of part definition dicts.'
    v = []
    v.append({"name": 'extra', "description": 'Selects the jig sub-type function.', "type": 'string', "default": '(required)'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable
def items(size="oobb", **kwargs):
    jgs = []
    jgs.append({"type": "jig", "extra": "tray_03_03", "width": 5, "height": 5, "thickness": 6, "size": size})
    jgs.append({"type": "jig", "extra": "screw_sorter_m3_03_03", "width": 3, "height": 3, "thickness": 15, "size": size})
    return jgs


def test(**kwargs):
    result = items(**kwargs)
    return isinstance(result, list) and all(isinstance(item, dict) for item in result)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_jig(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="jig", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
