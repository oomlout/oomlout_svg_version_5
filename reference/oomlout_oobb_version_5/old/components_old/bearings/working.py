d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bearings'
    d["name_long"] = 'Part Sets: Bearings'
    d["description"] = 'Builds a bearing solid+hole cylinder pair from named bearing lookup tables.'
    d["category"] = 'Part Sets'
    d["shape_aliases"] = []
    d["returns"] = 'List of part definition dicts.'
    v = []
    v.append({"name": 'bearing_name', "description": 'Bearing identifier, e.g. 608, 6704.', "type": 'string', "default": '(required)'})
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

    getter = getattr(oobb_make_sets, "get_bearings")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb as ob

    bearing_name = kwargs["bearing_name"]
    thing = ob.get_default_thing(**kwargs)
    thing.update({"description": f"bearing {bearing_name}"})

    th = thing["components"]
    th.extend(ob.oe(t="positive", s="oobb_cylinder",
              radius_name=f'bearing_{bearing_name}_od', depth=f"bearing_{bearing_name}_depth"))
    th.extend(ob.oe(t="negative", s="oobb_cylinder",
              radius_name=f'bearing_{bearing_name}_id', depth=f"bearing_{bearing_name}_depth"))

    return thing


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
