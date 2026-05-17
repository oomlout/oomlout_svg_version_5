d = {}


def describe():
    global d
    d = {}
    d["name"] = 'threaded_insert'
    d["name_long"] = 'Fasteners: Threaded Insert'
    d["description"] = 'Generates a heat-set threaded insert profile plus pilot hole geometry.'
    d["category"] = 'Fasteners'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'radius_name', "description": 'Thread size designation, e.g. m3, m4.', "type": 'string', "default": '"m3"'})
    v.append({"name": 'style', "description": 'Insert style profile identifier.', "type": 'string', "default": '"01"'})
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
    import oobb_base as ob

    wid = kwargs["radius_name"]
    style = kwargs.get("style", "01")
    thing = ob.get_default_thing(**kwargs)
    width = ob.gv(f"threaded_insert_{style}_radius_{wid}_true")
    depth = ob.gv(f"threaded_insert_{style}_depth_{wid}_true")
    thing.update({"description": f"threaded insert {wid}x{depth}"})
    thing.update({"width_mm": width})
    thing.update({"depth_mm": depth})

    th = thing["components"]
    th.extend(ob.oe(t="p", s="oobb_threaded_insert", rn=wid, hole=False))
    th.extend(ob.oe(t="n", s="oobb_hole", rn=wid, depth=100, z=-10, m=""))

    return thing


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="threaded_insert", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
