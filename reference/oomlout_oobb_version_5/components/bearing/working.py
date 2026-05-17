import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

d = {}


def describe():
    global d
    d = {}
    d["name"] = "bearing"
    d["name_long"] = "OPSC Mechanical Shapes: Bearing"
    d["description"] = "Legacy opsc bearing profile shape migrated into the component system."
    d["category"] = "OPSC Mechanical Shapes"
    d["shape_aliases"] = ["bearing"]
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
    params["shape"] = "bearing"
    return [opsc.opsc_easy(**params)]


def render(params):
    import copy
    import opsc
    from solid2 import difference, translate, union

    p2 = copy.deepcopy(params)
    inner_diameter = p2["id"]
    outer_diameter = p2["od"]
    pos = p2["pos"]
    depth = p2["depth"]
    depth_extra = p2.get("depth_extra", 100)
    clearance_bearing_original = p2.get("clearance_bearing", 2)
    clearance = p2.get("clearance", "")

    depth_bearing = depth
    if clearance != "":
        depth_bearing = depth + 250

    p2["shape"] = "cylinder"
    p2["h"] = depth_bearing
    main_inner = copy.deepcopy(p2)
    main_inner["r"] = inner_diameter
    main_outer = copy.deepcopy(p2)
    pos1 = copy.deepcopy(pos)
    if clearance == "bottom":
        pos1[2] += -depth_bearing
    main_outer["pos"] = pos1
    main_outer["r"] = outer_diameter

    p2["h"] = 100
    p2["pos"] = [pos[0], pos[1], pos[2] - 50]
    extra_inner = copy.deepcopy(p2)
    extra_outer = copy.deepcopy(p2)

    clearance_bearing = outer_diameter - inner_diameter - clearance_bearing_original / 2
    exclude_clearance = p2.get("exclude_clearance", False)

    extra_inner["r"] = inner_diameter + clearance_bearing / 2
    extra_outer["r"] = outer_diameter - clearance_bearing / 2

    mi = opsc.get_opsc_item(main_inner)
    mo = opsc.get_opsc_item(main_outer)
    eo = opsc.get_opsc_item(extra_outer)

    if not exclude_clearance:
        ei = opsc.get_opsc_item(extra_inner)
        if inner_diameter > 10:
            shape = translate([0, 0, -depth / 2])(union()(difference()(mo, mi), difference()(eo, ei)))
        else:
            shape = translate([0, 0, -depth / 2])(union()(difference()(mo, mi), difference()(eo)))
    else:
        ex = 4
        extra_inner["h"] = depth + ex + depth_extra
        extra_inner["pos"] = [pos[0], pos[1], pos[2] - ex / 2 - depth_extra / 2]
        ei = opsc.get_opsc_item(extra_inner)
        shape = translate([0, 0, -depth / 2])(mo, ei)
    return shape


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [45, 0, 25],
      'kwargs': {'type': 'positive', 'id': 4, 'od': 11, 'depth': 4, 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [45, 0, 25],
      'kwargs': {'type': 'positive', 'id': 8, 'od': 22, 'depth': 7, 'pos': [0, 0, 0]}}]

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


