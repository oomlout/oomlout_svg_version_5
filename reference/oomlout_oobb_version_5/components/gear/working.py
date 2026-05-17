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
    d["name"] = "gear"
    d["name_long"] = "OPSC Mechanical Shapes: Gear"
    d["description"] = "Legacy opsc involute gear shape migrated into the component system."
    d["category"] = "OPSC Mechanical Shapes"
    d["shape_aliases"] = ["gear"]
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
    params["shape"] = "gear"
    return [opsc.opsc_easy(**params)]


def render(params):
    from solid2 import import_scad

    default = {
        "number_of_teeth": params.get("number_of_teeth", 24),
        "circular_pitch": params.get("circular_pitch", False),
        "diametral_pitch": params.get("diametral_pitch", 0.533333),
        "pressure_angle": params.get("pressure_angle", 20),
        "clearance": params.get("clearance", 0.5),
        "gear_thickness": params.get("gear_thickness", params.get("depth", 10)),
        "rim_thickness": params.get("rim_thickness", params.get("gear_thickness", params.get("depth", 10))),
        "rim_width": params.get("rim_width", 0),
        "hub_thickness": params.get("hub_thickness", 0),
        "hub_diameter": params.get("hub_diameter", 0),
        "bore_diameter": params.get("bore_diameter", 0),
        "circles": params.get("circles", 0),
        "backlash": params.get("backlash", 0.5),
        "twist": params.get("twist", 0),
        "involute_facets": params.get("involute_facets", 0),
        "flat": params.get("flat", False),
    }

    involute_gear = import_scad("MCAD/involute_gears.scad")
    return involute_gear.gear(**default)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [65, 0, 20],
      'kwargs': {'type': 'positive', 'number_of_teeth': 16, 'depth': 5, 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [65, 0, 20],
      'kwargs': {'type': 'positive', 'number_of_teeth': 24, 'depth': 6, 'pos': [0, 0, 0]}}]

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


