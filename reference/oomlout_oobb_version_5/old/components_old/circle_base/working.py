d = {}


def describe():
    global d
    d = {}
    d["name"] = 'circle_base'
    d["name_long"] = 'Circles: Circle Base'
    d["description"] = 'Base circular geometry builder with optional shaft hole, perimeter holes, and doughnut cutout.'
    d["category"] = 'Circles'
    d["shape_aliases"] = ['circle_base']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'diameter', "description": 'Circle diameter in OOBB units.', "type": 'number', "default": 1})
    v.append({"name": 'thickness', "description": 'Circle thickness in mm.', "type": 'number', "default": 3})
    v.append({"name": 'size', "description": 'OOBB grid size prefix.', "type": 'string', "default": '"oobb"'})
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
    v.append({"name": 'shaft', "description": 'Shaft type; suppresses middle hole when set.', "type": 'string', "default": '""'})
    v.append({"name": 'holes', "description": 'Add perimeter holes.', "type": 'bool', "default": True})
    v.append({"name": 'both_holes', "description": 'Add both oobb and oobe holes.', "type": 'bool', "default": True})
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
    """Build and return the thing dict for circle_base."""
    import copy
    import oobb
    from oobb_arch.helpers.shaft_helpers import get_shaft_center

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    diameter = kwargs.get("diameter", 1)
    width = diameter
    height = diameter
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)
    shaft = kwargs.get("shaft", "")

    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)
    kwargs["pos"] = pos

    # get the default thing
    thing = oobb.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size", "")

    th.append(oobb.get_comment("circle main", "p"))
    # add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"{size}_circle"
    p3["width"] = width
    p3["height"] = height
    p3["depth"] = thickness
    p3["pos"] = pos
    #p3["m"] = ""
    oobb.append_full(thing, **p3)

    doughnut_diameter = 0
    #doughnut_cutout
    if "doughnut" in extra:
        doughnut_diameter = float(extra.replace("doughnut_", ""))
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"{size}_circle"
        p3["width"] = doughnut_diameter
        p3["height"] = doughnut_diameter
        p3["depth"] = thickness
        p3["pos"] = pos
        p3["diameter"] = doughnut_diameter
        #p3["m"] = "#"
        oobb.append_full(thing, **p3)

    # add holes
    if holes:
        th.append(oobb.get_comment("holes main", "n"))
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"{size}_holes"
        p3["width"] = width
        p3["height"] = height
        p3["pos"] = pos
        p3["holes"] = "all"
        p3["both_holes"] = both_holes
        p3["circle"] = True
        if shaft != "":
            p3["middle"] = False
            pass

        #p3["m"] = "#"
        oobb.append_full(thing, **p3)
        #th.extend(oobb.oobb_easy(**p3))

        if diameter == 1.5:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "n"
            p3["shape"] = f"{size}_hole"
            p3["width"] = width
            p3["height"] = height
            p3["pos"] = pos
            p3["radius_name"] = "m3"
            poss = []
            shift = 5.303
            poss.append([shift, shift, 0])
            poss.append([-shift, shift, 0])
            poss.append([shift, -shift, 0])
            poss.append([-shift, -shift, 0])
            p3["pos"] = poss
            p3["m"] = "#"
            oobb.append_full(thing, **p3)

    if shaft != "":
        get_shaft_center(thing, **kwargs)

    if full_object:
        return thing
    else:  # only return the elements
        return th


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="circle_base", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
