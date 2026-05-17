d = {}


def describe():
    global d
    d = {}
    d["name"] = 'plate_ninety_degree'
    d["name_long"] = 'Plates: 90-Degree Plate'
    d["description"] = '90-degree plate with multi-axis M6/M3 hole patterns.'
    d["category"] = 'Plates'
    d["shape_aliases"] = ['plate_ninety_degree']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'width', "description": 'Plate width in OOBB units.', "type": 'number', "default": 1})
    v.append({"name": 'height', "description": 'Plate height in OOBB units.', "type": 'number', "default": 1})
    v.append({"name": 'thickness', "description": 'Plate depth in mm.', "type": 'number', "default": 3})
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
    v.append({"name": 'holes', "description": 'Generate the hole grid.', "type": 'bool', "default": True})
    v.append({"name": 'both_holes', "description": 'Add holes on both faces.', "type": 'bool', "default": True})
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
    """Build and return the thing dict for plate_ninety_degree."""
    import copy
    import oobb_base

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    thickness_oobb = 0
    if thickness >= 14:
        thickness_oobb = (thickness + 1) / 15

    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)

    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)
    kwargs["pos"] = pos

    plate_pos = [0, 0, -thickness/2]
    plate_pos = [pos[0] + plate_pos[0], pos[1] + plate_pos[1], pos[2] + plate_pos[2]]

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size", "")

    th.append(oobb_base.get_comment("plate main", "p"))
    # add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"{size}_plate"
    p3["width"] = width
    p3["height"] = height
    p3["depth"] = thickness
    p3["pos"] = plate_pos
    p3["r"] = 2.5
    #p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    #th.append(oobb_base.oobb_easy(**p3))

    holes_m6_vertical = []
    holes_m6_horizontal = []
    holes_m3_vertical = []
    holes_m3_horizontal = []

    for w in range(1, width+1):
        for h in range(1, height+1):
            for t in range(1, int(thickness_oobb)+1):
                #vertical even horizontal odd
                if w % 2 == 0:
                    holes_m6_vertical.append([[h, w, t], [0, 0, 0], "m6"])
                else:
                    holes_m6_horizontal.append([[h, w, t], [90, 0, 0], "m6"])

                if w+1 <= width:
                    holes_m3_horizontal.append([[h, w+0.5, t], [90, 0, 0], "m3"])
                    holes_m3_vertical.append([[h, w+0.5, t], [0, 0, 0], "m3"])
    hole_list = []
    hole_list.extend(holes_m6_vertical)
    hole_list.extend(holes_m6_horizontal)
    hole_list.extend(holes_m3_vertical)
    hole_list.extend(holes_m3_horizontal)
    if holes:
        for hole in hole_list:
            p3 = copy.deepcopy(kwargs)
            pos1 = copy.deepcopy(pos)
            #x
            x_shift = (hole[0][1]-1) * 15 - width/2 * 15 + 7.5

            #y
            y_shift = (hole[0][0]-1) * 15 - height/2 * 15 + 7.5

            #z
            z_shift = (hole[0][2]-1) * 15 - thickness_oobb/2 * 15 + 7.5

            pos1[0] += x_shift
            pos1[1] += y_shift
            pos1[2] += z_shift
            p3["type"] = "n"
            p3["shape"] = f"{size}_hole_new"
            p3["width"] = width
            p3["height"] = height
            p3["pos"] = pos1
            p3["both_holes"] = both_holes
            p3["holes"] = "single"
            p3["radius_name"] = hole[2]
            p3["rot"] = hole[1]
            p3["zz"] = "middle"
            #p3["m"] = "#"
            p3["depth"] = 250
            oobb_base.append_full(thing, **p3)

    if full_object:
        return thing
    else:  # only return the elements
        return th


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate_ninety_degree", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
