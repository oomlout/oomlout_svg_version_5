d = {}


def describe():
    global d
    d = {}
    d["name"] = 'shaft_couplers'
    d["name_long"] = 'Part Sets: Shaft Couplers'
    d["description"] = 'Delegates to the legacy get_shaft_coupler function.'
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

    getter = getattr(oobb_make_sets, "get_shaft_couplers")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_shaft_coupler(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="shaft_coupler", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
