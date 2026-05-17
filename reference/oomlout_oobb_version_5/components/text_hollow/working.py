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
    d["name"] = "text_hollow"
    d["name_long"] = "OPSC Composite Shapes: Hollow Text"
    d["description"] = "Legacy opsc hollow-text shape migrated into the component system."
    d["category"] = "OPSC Composite Shapes"
    d["shape_aliases"] = ["text_hollow"]
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
    params["shape"] = "text_hollow"
    return [opsc.opsc_easy(**params)]


def render(params):
    import copy
    import opsc
    from solid2 import linear_extrude, offset, text
    from solid2 import difference as solid_difference

    wall_thickness = params.get("wall_thickness", 0.5)
    extra = params.get("extra", "")

    p2 = copy.deepcopy(params)
    p2["shape"] = "text"
    text_big = opsc.get_opsc_item(p2)

    p3 = copy.deepcopy(params)
    little_text = text(
        text=p3["text"],
        size=p3["size"],
        font=p3["font"],
        halign=p3["halign"],
        valign=p3["valign"],
    )
    little_text = offset(r=-wall_thickness)(little_text)
    little_text = linear_extrude(p3["height"] - wall_thickness)(little_text)
    p3["pos"][2] = p3["pos"][2] - wall_thickness
    if extra == "reverse":
        p3["pos"][2] = p3["pos"][2] + wall_thickness * 2
    little_text = opsc.get_opsc_transform(p3, little_text)
    return solid_difference()(text_big, little_text)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [65, 0, 25],
      'kwargs': {'type': 'positive',
                 'text': 'OOBB',
                 'size': 10,
                 'height': 3,
                 'font': 'DejaVu Sans:style=Bold',
                 'halign': 'center',
                 'valign': 'center',
                 'wall_thickness': 0.8,
                 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [65, 0, 25],
      'kwargs': {'type': 'positive',
                 'text': 'A',
                 'size': 16,
                 'height': 4,
                 'font': 'DejaVu Sans:style=Bold',
                 'halign': 'center',
                 'valign': 'center',
                 'wall_thickness': 1,
                 'extra': 'reverse',
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


