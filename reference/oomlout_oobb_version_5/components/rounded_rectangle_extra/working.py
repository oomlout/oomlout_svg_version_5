import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from solidpython_compat import apply_modifier

d = {}


def describe():
    global d
    d = {}
    d["name"] = "rounded_rectangle_extra"
    d["name_long"] = "OPSC Composite Shapes: Rounded Rectangle Extra"
    d["description"] = "Legacy opsc inset rounded rectangle shape migrated into the component system."
    d["category"] = "OPSC Composite Shapes"
    d["shape_aliases"] = ["rounded_rectangle_extra"]
    d["returns"] = "List of geometry component dicts."
    d["variables"] = []
    return d


def define():
    global d
    if not d:
        describe()
    defined = {}
    defined.update(d)
    return defined


def action(**kwargs):
    import opsc

    params = copy.deepcopy(kwargs)
    params.setdefault("type", "positive")
    params["shape"] = "rounded_rectangle_extra"
    return [opsc.opsc_easy(**params)]


def render(params):
    import copy
    import opsc
    from solid2 import hull

    m = params.get("m", "")
    p2 = copy.deepcopy(params)
    inset = p2.get("inset", 0)
    radius = p2.get("r", 5)
    rot_y = p2.get("rotY", 0)
    p2.pop("r", "")
    p2["r1"] = radius
    p2["r2"] = radius - inset / 2
    change = p2["r1"]
    if rot_y == 180:
        p2["r2"] = radius
        p2["r1"] = radius - inset / 2
        change = p2["r2"]

    p2["m"] = ""
    p2["h"] = p2["size"][2]
    p2["pos"] = p2.get("pos", [0, 0, 0])
    p2["type"] = "positive"
    p2["shape"] = "cylinder"
    p2["pos"] = [0, 0, 0]
    p2.pop("rot", None)

    tl = copy.deepcopy(p2)
    tr = copy.deepcopy(p2)
    bl = copy.deepcopy(p2)
    br = copy.deepcopy(p2)
    tl["pos"][0] = -(p2["size"][0] - change * 2) / 2
    tl["pos"][1] = (p2["size"][1] - change * 2) / 2
    tr["pos"][0] = (p2["size"][0] - change * 2) / 2
    tr["pos"][1] = (p2["size"][1] - change * 2) / 2
    bl["pos"][0] = -(p2["size"][0] - change * 2) / 2
    bl["pos"][1] = -(p2["size"][1] - change * 2) / 2
    br["pos"][0] = (p2["size"][0] - change * 2) / 2
    br["pos"][1] = -(p2["size"][1] - change * 2) / 2
    for corner in [tl, tr, bl, br]:
        del corner["size"]

    solid_obj = hull()(
        opsc.get_opsc_item(tl),
        opsc.get_opsc_item(tr),
        opsc.get_opsc_item(bl),
        opsc.get_opsc_item(br),
    )
    return apply_modifier(solid_obj, m)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [55, 0, 25],
      'kwargs': {'type': 'positive',
                 'size': [24, 14, 6],
                 'r': 4,
                 'inset': 2,
                 'rotY': 0,
                 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [55, 0, 25],
      'kwargs': {'type': 'positive',
                 'size': [24, 14, 6],
                 'r': 4,
                 'inset': 2,
                 'rotY': 180,
                 'pos': [0, 0, 0]}}]

    generated_files = []

    for sample in samples:
        kwargs = copy.deepcopy(sample["kwargs"])
        result = action(**kwargs)
        if isinstance(result, dict) and "components" in result:
            components = copy.deepcopy(result["components"])
        elif isinstance(result, list):
            components = result
        else:
            components = [result]

        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        png_path = os.path.join(sample_dir, "image.png")

        opsc.opsc_make_object(
            scad_path,
            components,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_preview_images(scad_path, sample_dir)
        generated_files.append(png_path)

    return generated_files


