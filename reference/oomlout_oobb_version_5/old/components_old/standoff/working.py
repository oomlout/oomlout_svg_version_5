d = {}


def describe():
    global d
    d = {}
    d["name"] = 'standoff'
    d["name_long"] = 'Fasteners: Standoff'
    d["description"] = 'Generates a standoff with a through-hole for a selected hardware thread size.'
    d["category"] = 'Fasteners'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'radius_name', "description": 'Thread size designation, e.g. m3, m5.', "type": 'string', "default": '"m3"'})
    v.append({"name": 'depth', "description": 'Standoff length in mm.', "type": 'number', "default": 10})
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
    depth = kwargs["depth"]
    thing = ob.get_default_thing(**kwargs)
    width = ob.gv(f"nut_radius_{wid}_true")

    thing.update({"description": f"standoff {wid}x{depth}x{depth}"})
    thing.update({"width_mm": width})
    thing.update({"depth_mm": depth})
    thing.update({"height_mm": width/1.154})

    th = thing["components"]
    th.extend(ob.oe(t="p", s="oobb_standoff", rn=wid, hole=True, depth=depth))

    return thing


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="standoff", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
