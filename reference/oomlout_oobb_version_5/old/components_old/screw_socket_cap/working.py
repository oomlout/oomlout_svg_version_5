d = {}


def describe():
    global d
    d = {}
    d["name"] = 'screw_socket_cap'
    d["name_long"] = 'Fasteners: Socket Cap Screw'
    d["description"] = 'Generates a socket head cap screw with configurable thread size and length.'
    d["category"] = 'Fasteners'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'radius_name', "description": 'Screw thread size, e.g. m3, m5.', "type": 'string', "default": '"m3"'})
    v.append({"name": 'depth', "description": 'Screw length/depth in mm.', "type": 'number', "default": 12})
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
    thing.update({"description": f"screw socket cap {wid}x{depth}"})
    thing.update({"depth_mm": depth})

    thing.update({"components": []})
    thing["components"].extend(ob.oe(
        t="positive", s="oobb_screw_socket_cap", rn=wid, depth=depth, include_nut=False))

    return thing


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="screw_socket_cap", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
