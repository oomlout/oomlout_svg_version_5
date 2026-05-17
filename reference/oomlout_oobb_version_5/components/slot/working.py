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
    d["name"] = "slot"
    d["name_long"] = "OPSC Composite Shapes: Slot"
    d["description"] = "Legacy opsc slot shape migrated into the component system."
    d["category"] = "OPSC Composite Shapes"
    d["shape_aliases"] = ["slot"]
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
    params["shape"] = "slot"
    return [opsc.opsc_easy(**params)]


def render(params):
    import copy
    import opsc
    from solid2 import hull

    p3 = copy.deepcopy(params)
    pos = p3.get("pos", [0, 0, 0])
    width = p3.get("width", p3.get("w", 1))

    p3["r1"] = p3.get("radius_1", p3.get("r1", 0))
    p3["r2"] = p3.get("radius_2", p3.get("r2", 0))

    for rad in ["r1", "r2", "r"]:
        test = p3.get(rad, "")
        if isinstance(test, str) and test != "":
            p3[rad] = opsc.radius_dict[p3[rad]]

    r = p3.get("r", "")
    if r != "":
        p3["r1"] = r
        p3["r2"] = r

    p3["type"] = "positive"
    p3["shape"] = "cylinder"

    left = copy.deepcopy(p3)
    left["pos"] = copy.deepcopy(pos)
    left["pos"][0] += width / 2

    right = copy.deepcopy(p3)
    right["pos"] = copy.deepcopy(pos)
    right["pos"][0] += -width / 2

    left_obj = opsc.get_opsc_item(left)
    right_obj = opsc.get_opsc_item(right)
    return apply_modifier(hull()(left_obj, right_obj), p3.get("m", ""))


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [60, 0, 25],
      'kwargs': {'type': 'positive', 'r': 3, 'w': 14, 'h': 6, 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [60, 0, 25],
      'kwargs': {'type': 'positive', 'r1': 4, 'r2': 2, 'w': 16, 'h': 6, 'pos': [0, 0, 0]}}]

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


