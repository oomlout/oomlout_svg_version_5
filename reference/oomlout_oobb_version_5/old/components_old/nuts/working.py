d = {}


def describe():
    global d
    d = {}
    d["name"] = 'nuts'
    d["name_long"] = 'Part Sets: Nuts'
    d["description"] = 'Builds a nut solid+through-hole pair using named radius lookup tables.'
    d["category"] = 'Part Sets'
    d["shape_aliases"] = []
    d["returns"] = 'List of part definition dicts.'
    v = []
    v.append({"name": 'radius_name', "description": 'Named radius key, e.g. m3, m6.', "type": 'string', "default": '(required)'})
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

    getter = getattr(oobb_make_sets, "get_nuts")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_base as ob

    wid = kwargs["radius_name"]

    thing = ob.get_default_thing(**kwargs)
    width = ob.gv(f"nut_radius_{wid}_true")
    depth = ob.gv(f"nut_depth_{wid}_true")
    thing.update({"description": f"nut {wid}x{depth}"})
    thing.update({"width_mm": width})
    thing.update({"depth_mm": depth})
    thing.update({"height_mm": width/1.154})

    th = thing["components"]
    th.extend(ob.oe(t="p", s="oobb_nut", rn=wid))
    th.extend(ob.oe(t="n", s="oobb_hole", rn=wid, depth=100, z=-10, m=""))

    return thing


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="nut", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
