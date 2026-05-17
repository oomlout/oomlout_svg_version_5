d = {}


def describe():
    global d
    d = {}
    d["name"] = 'screws'
    d["name_long"] = 'Part Sets: Screws'
    d["description"] = 'Part set for screw items; see individual screw variant components for geometry.'
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

    getter = getattr(oobb_make_sets, "get_screws")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)
