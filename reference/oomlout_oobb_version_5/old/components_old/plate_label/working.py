d = {}


def describe():
    global d
    d = {}
    d["name"] = 'plate_label'
    d["name_long"] = 'Plates: Label Plate'
    d["description"] = 'Label plate that composes a sub-plate with right-side holes.'
    d["category"] = 'Plates'
    d["shape_aliases"] = ['plate_label']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'width', "description": 'Plate width in OOBB units.', "type": 'number', "default": 1})
    v.append({"name": 'height', "description": 'Plate height in OOBB units.', "type": 'number', "default": 1})
    v.append({"name": 'thickness', "description": 'Plate depth in mm.', "type": 'number', "default": 3})
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
    v.append({"name": 'holes', "description": 'Hole presence flag.', "type": 'bool', "default": True})
    v.append({"name": 'both_holes', "description": 'Both-holes flag.', "type": 'bool', "default": True})
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
    """Build and return the thing dict for plate_label."""
    import copy
    import oobb_base

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)

    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)
    kwargs["pos"] = pos

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size", "")

    #get the plate
    p3 = copy.deepcopy(kwargs)
    pos1 = copy.deepcopy(pos)
    shift_x = 0
    shift_y = 0
    shift_z = 0
    pos1 = [pos1[0] + shift_x, pos1[1] + shift_y, pos1[2] + shift_z]
    p3["pos"] = pos1
    p3["type"] = "plate"
    p3["width"] = width
    p3["height"] = height
    p3["holes"] = "right"
    p3["full_object"] = False

    p3.pop("extra", "")
    width_plate = oobb_base.get_thing_from_dict(p3)
    th.append(width_plate)

    if full_object:
        return thing
    else:  # only return the elements
        return th


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate_label", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
