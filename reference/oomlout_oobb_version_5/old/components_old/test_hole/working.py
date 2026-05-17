d = {}


def describe():
    global d
    d = {}
    d["name"] = 'test_hole'
    d["name_long"] = 'Tests: Hole Test Plate'
    d["description"] = 'Plate with a grid of progressively sized hole cutouts for fit testing.'
    d["category"] = 'Tests'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'width', "description": 'Plate width in grid units.', "type": 'number', "default": 3})
    v.append({"name": 'height', "description": 'Plate height in grid units.', "type": 'number', "default": 3})
    v.append({"name": 'shaft', "description": 'Starting hole diameter in mm.', "type": 'number', "default": 3})
    v.append({"name": 'bearing', "description": 'Increment step between holes in mm.', "type": 'number', "default": 0.5})
    v.append({"name": 'thickness', "description": 'Plate thickness in mm.', "type": 'number', "default": 3})
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
    import math
    import oobb_base

    kwargs.pop("style", "")
    pos = kwargs.get("pos", [0, 0, 0])
    full_object = kwargs.get("full_object", True)
    hole_size = kwargs.get("shaft", 3)
    increment = kwargs.get("bearing", 0.5)

    kwargs["pos"] = pos

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size", "")
    kwargs.pop("extra", "")
    kwargs.pop("type", "")
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)
    thickness = kwargs.get("thickness", 3)

    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "oobb_plate"
    p3["type"] = "positive"
    p3["width"] = width
    p3["height"] = height
    p3["depth"] = thickness
    oobb_base.append_full(thing, **p3)

    wid = width
    hei = height
    extra = -increment * 4
    for w in range(0, wid):
        for h in range(0, hei):
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_hole"
            p3["type"] = "negative"
            p3["width"] = wid
            p3["height"] = hei
            p3["depth"] = 3
            x = (w * 15) - math.floor(wid / 2) * 15
            y = (h * 15) - math.floor(hei / 2) * 15
            pos1 = copy.deepcopy(p3["pos"])
            pos1[0] += x
            pos1[1] += y
            p3["pos"] = pos1
            p3["radius"] = (hole_size + extra) / 2
            oobb_base.append_full(thing, **p3)
            extra += increment

    if full_object:
        return thing
    else:
        return thing["components"]


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="test_hole", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
