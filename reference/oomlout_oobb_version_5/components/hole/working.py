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
    d["name"] = "hole"
    d["name_long"] = "OPSC Composite Shapes: Hole"
    d["description"] = "Legacy opsc cylindrical hole shape migrated into the component system."
    d["category"] = "OPSC Composite Shapes"
    d["shape_aliases"] = ["hole"]
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
    params.setdefault("type", "negative")
    params["shape"] = "hole"
    return [opsc.opsc_easy(**params)]


def render(params):
    import copy
    import opsc

    p2 = copy.deepcopy(params)
    try:
        p2["r"] = p2["r"]
    except KeyError:
        p2["r"] = p2["radius"]

    if isinstance(p2["r"], str):
        p2["r"] = opsc.radius_dict[p2["r"]]

    if "h" not in p2:
        p2["h"] = 200
        p2["pos"] = [0, 0, -100]

    p2["center"] = True
    p2["shape"] = "cylinder"
    p2["type"] = "positive"
    return opsc.get_opsc_item(p2)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [60, 0, 25],
      'kwargs': {'type': 'positive', 'r': 3, 'h': 10, 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [60, 0, 25],
      'kwargs': {'type': 'positive', 'r': 5, 'h': 12, 'pos': [0, 0, 0]}}]

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


