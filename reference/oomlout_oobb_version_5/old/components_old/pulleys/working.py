d = {}


def describe():
    global d
    d = {}
    d["name"] = 'pulleys'
    d["name_long"] = 'Part Sets: Pulleys'
    d["description"] = 'Delegates to oobb_get_items_oobb.get_pulley_gt2 for GT2 pulley geometry.'
    d["category"] = 'Part Sets'
    d["shape_aliases"] = []
    d["returns"] = 'List of part definition dicts.'
    v = []
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
    import oobb_make_sets

    getter = getattr(oobb_make_sets, "get_pulleys")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb

    return oobb_get_items_oobb.get_pulley_gt2(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="pulley_gt2", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
