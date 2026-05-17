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
    d["name"] = "sphere_rectangle"
    d["name_long"] = "OPSC Composite Shapes: Sphere Rectangle"
    d["description"] = "Legacy opsc sphere-swept rectangle shape migrated into the component system."
    d["category"] = "OPSC Composite Shapes"
    d["shape_aliases"] = ["sphere_rectangle"]
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
    params["shape"] = "sphere_rectangle"
    return [opsc.opsc_easy(**params)]


def render(params):
    import copy
    import opsc
    from solid2 import hull, union

    p2 = copy.deepcopy(params)
    m = p2.get("m", "")
    p2.pop("rot", None)
    p2.setdefault("r", 5)

    height = p2["size"][2]
    radius = p2["r"]

    hole_params = copy.deepcopy(p2)
    hole_params["m"] = ""
    hole_params["h"] = height - radius * 2
    hole_params["type"] = "positive"
    hole_params["shape"] = "hole"
    hole_params["pos"] = [0, 0, radius]

    sphere_bottom = copy.deepcopy(p2)
    sphere_bottom["m"] = ""
    sphere_bottom["type"] = "positive"
    sphere_bottom["shape"] = "sphere"
    sphere_bottom["pos"] = [0, 0, radius]

    sphere_top = copy.deepcopy(p2)
    sphere_top["m"] = ""
    sphere_top["type"] = "positive"
    sphere_top["shape"] = "sphere"
    sphere_top["pos"] = [0, 0, height - radius]

    def _corner_sets():
        return [copy.deepcopy(hole_params), copy.deepcopy(sphere_bottom), copy.deepcopy(sphere_top)]

    tls = _corner_sets()
    trs = _corner_sets()
    bls = _corner_sets()
    brs = _corner_sets()

    for group, x_sign, y_sign in [
        (tls, -1, 1),
        (trs, 1, 1),
        (bls, -1, -1),
        (brs, 1, -1),
    ]:
        for item in group:
            item["pos"][0] = x_sign * (p2["size"][0] - p2["r"] * 2) / 2
            item["pos"][1] = y_sign * (p2["size"][1] - p2["r"] * 2) / 2
            item.pop("size", None)

    def _union_group(items):
        return union()([opsc.get_opsc_item(item) for item in items])

    solid_obj = hull()(
        _union_group(tls),
        _union_group(trs),
        _union_group(bls),
        _union_group(brs),
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
      'preview_rot': [45, 0, 25],
      'kwargs': {'type': 'positive', 'size': [24, 16, 10], 'r': 3, 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [45, 0, 25],
      'kwargs': {'type': 'positive', 'size': [32, 20, 12], 'r': 4, 'pos': [0, 0, 0]}}]

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


