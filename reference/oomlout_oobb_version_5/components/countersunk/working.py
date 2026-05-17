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
    d["name"] = "countersunk"
    d["name_long"] = "OPSC Composite Shapes: Countersunk"
    d["description"] = "Legacy opsc countersunk screw shape migrated into the component system."
    d["category"] = "OPSC Composite Shapes"
    d["shape_aliases"] = ["countersunk"]
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
    params["shape"] = "countersunk"
    return [opsc.opsc_easy(**params)]


def render(params):
    import copy
    import opsc
    from solid2 import union

    p2 = copy.deepcopy(params)
    counter_rad = p2["r"]
    p2["r"] = opsc.radius_dict[p2["r"]]

    hp = copy.deepcopy(p2)
    hp["type"] = "positive"
    hp["shape"] = "hole"
    hp.pop("rot", None)
    hol = opsc.get_opsc_item(hp)

    cp = copy.deepcopy(p2)
    cp["h"] = opsc.countersunk_dict[counter_rad]["height"]
    cp["r2"] = opsc.countersunk_dict[counter_rad]["little_rad"]
    cp["r1"] = opsc.countersunk_dict[counter_rad]["big_rad"]
    del cp["r"]
    cp.pop("rot", None)
    cp["type"] = "positive"
    cp["shape"] = "cylinder"
    cp["pos"] = [0, 0, 0]
    top = opsc.get_opsc_item(cp)
    return union()(hol, top)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [70, 0, 20],
      'kwargs': {'type': 'positive', 'r': 'm3', 'rot': [0, 0, 0], 'pos': [0, 0, 0]}}]

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


