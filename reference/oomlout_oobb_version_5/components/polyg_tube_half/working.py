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
    d["name"] = "polyg_tube_half"
    d["name_long"] = "OPSC Composite Shapes: Half Polygon Tube"
    d["description"] = "Legacy opsc half polygon tube shape migrated into the component system."
    d["category"] = "OPSC Composite Shapes"
    d["shape_aliases"] = ["polyg_tube_half"]
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
    params["shape"] = "polyg_tube_half"
    return [opsc.opsc_easy(**params)]


def render(params):
    import copy
    from solid2 import cube, difference, translate

    from components.polyg_tube.working import render as render_polyg_tube

    p2 = copy.deepcopy(params)
    for key in ["pos", "rotX", "rotY", "rotZ"]:
        p2.pop(key, None)

    item = render_polyg_tube(p2)
    width = p2.get("r1", 10) * 2
    height = p2.get("r1", 10)
    depth = p2.get("depth", 10)
    cut_cube = translate([0, height / 2, depth / 2])(cube(size=[width, height, depth], center=True))
    return difference()(item, cut_cube)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [60, 0, 25],
      'kwargs': {'type': 'positive', 'sides': 6, 'r1': 12, 'r2': 8, 'depth': 6, 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [60, 0, 25],
      'kwargs': {'type': 'positive', 'sides': 8, 'r1': 14, 'r2': 10, 'depth': 6, 'pos': [0, 0, 0]}}]

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


