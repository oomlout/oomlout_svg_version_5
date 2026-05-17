d = {}


def describe():
    global d
    d = {}
    d["name"] = 'test_oobb_screw_socket_cap'
    d["name_long"] = 'Tests: Socket Cap Screw Test'
    d["description"] = 'Socket cap screw test fixtures; style fixed to socket_cap.'
    d["category"] = 'Tests'
    d["shape_aliases"] = []
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
    import copy
    import oobb_base

    p3 = copy.deepcopy(kwargs)
    p3["style"] = "socket_cap"
    p3["type"] = "test_oobb_screw"
    return oobb_base.get_thing_from_dict(p3)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="test_oobb_screw_socket_cap", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
