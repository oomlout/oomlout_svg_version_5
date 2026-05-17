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
    d["name"] = "d_shaft"
    d["name_long"] = "OPSC Mechanical Shapes: D Shaft"
    d["description"] = "Legacy opsc D-shaft shape migrated into the component system."
    d["category"] = "OPSC Mechanical Shapes"
    d["shape_aliases"] = ["d_shaft"]
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
    params["shape"] = "d_shaft"
    return [opsc.opsc_easy(**params)]


def render(kwargs):
    import copy
    import opsc
    from solid2 import difference

    radius = kwargs.get("radius", kwargs.get("r", ""))
    flat_diameter = kwargs.get("id", "")
    depth = kwargs.get("depth", kwargs.get("h", ""))
    typ = kwargs.get("type", kwargs.get("t", "positive"))
    pos = kwargs.get("pos", [0, 0, 0])
    typ_other = ""
    if typ == "negative":
        typ = "n"
    if typ == "positive":
        typ = "p"
    if typ == "n":
        typ_other = "p"
    if typ == "p":
        typ_other = "n"
    if typ == "pp":
        typ_other = "nn"
    if typ == "nn":
        typ_other = "pp"

    shaft = copy.deepcopy(kwargs)
    shaft["shape"] = "cylinder"
    shaft["h"] = depth
    shaft["r"] = radius
    shaft["pos"] = [pos[0], pos[1], pos[2] - depth]
    shaft["type"] = typ
    shaft_shape = opsc.get_opsc_item(shaft)

    indent = copy.deepcopy(kwargs)
    indent["shape"] = "cube"
    indent.pop("r", "")
    dif = radius * 2 - flat_diameter
    indent["size"] = [radius * 2, dif, depth]
    indent["pos"] = [pos[0] - radius, pos[1] + radius - dif, pos[2] - depth]
    indent["type"] = typ_other
    indent_shape = opsc.get_opsc_item(indent)
    return difference()(shaft_shape, indent_shape)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [70, 0, 20],
      'kwargs': {'type': 'positive', 'r': 4, 'id': 6, 'depth': 8, 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [70, 0, 20],
      'kwargs': {'type': 'positive', 'r': 6, 'id': 9, 'depth': 10, 'pos': [0, 0, 0]}}]

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


