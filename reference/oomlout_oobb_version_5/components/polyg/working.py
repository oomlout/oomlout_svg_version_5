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
    d["name"] = "polyg"
    d["name_long"] = "OPSC Composite Shapes: Polygon Prism"
    d["description"] = "Legacy opsc polygon-prism shape migrated into the component system."
    d["category"] = "OPSC Composite Shapes"
    d["shape_aliases"] = ["polyg"]
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
    params["shape"] = "polyg"
    return [opsc.opsc_easy(**params)]


def _regular_polygon_points(num_sides, radius):
    import math

    angle = 2 * math.pi / num_sides
    points = []
    for i in range(num_sides):
        x = radius * math.cos(i * angle)
        y = radius * math.sin(i * angle)
        points.append((x, y))
    return points


def render(params):
    import copy
    import opsc

    p2 = copy.deepcopy(params)
    p2.pop("rot", "")
    p2.pop("rotX", "")
    p2.pop("rotY", "")
    p2.pop("rotZ", "")
    p2["type"] = "positive"
    p2["shape"] = "polygon"
    p2["pos"] = [0, 0, 0]

    sides = p2.get("sides", 6)
    radius = p2["r"]
    extra_clearance = p2.get("extra_clearance", 0)
    if extra_clearance != 0:
        p2["height"] = p2.get("height", 0) + extra_clearance
    radius_full = radius + extra_clearance / 2
    p2["points"] = _regular_polygon_points(sides, radius_full)
    return opsc.get_opsc_item(p2)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [55, 0, 25],
      'kwargs': {'type': 'positive', 'sides': 6, 'r': 8, 'height': 6, 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [55, 0, 25],
      'kwargs': {'type': 'positive', 'sides': 3, 'r': 10, 'height': 5, 'pos': [0, 0, 0]}}]

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


