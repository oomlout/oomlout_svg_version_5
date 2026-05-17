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
    d["name"] = "oobb_overhang"
    d["name_long"] = "OOBB Geometry Primitives: Overhang Bridge"
    d["description"] = "Two-layer 3D-print overhang bridge geometry sized to a named radius footprint."
    d["category"] = "OOBB Geometry Primitives"
    d["shape_aliases"] = ["overhang"]
    d["returns"] = "List of geometry component dicts."
    v = []
    v.append({"name": "pos", "description": "3-element [x,y,z] position.", "type": "list", "default": "[0,0,0]"})
    v.append({"name": "radius_name", "description": 'Named radius key: `"m3"`, `"m3_nut"`, `"m2"`, `"m6"`.', "type": "string", "default": '"m3"'})
    v.append({"name": "zz", "description": 'Z anchor: `"bottom"` or `"top"`.', "type": "string", "default": '"bottom"'})
    v.append({"name": "type", "description": "Geometry type: positive or negative.", "type": "string", "default": '"positive"'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable


def action(**kwargs):
    import oobb
    """Geometry component."""

    return_value = []
    height_layer = 0.3
    radius_name = kwargs.get("radius_name", "m3")
    zz = kwargs.get("zz", "bottom")

    if radius_name == "m3":
        width = 3.5
        height = 6.5
    elif radius_name == "m3_nut":
        height = (oobb.gv("nut_radius_m3_3dpr") * 2) / 1.154
        width = oobb.gv("hole_radius_m3_3dpr") * 2
    elif radius_name == "m2":
        width = 2.5
        height = 5.5
    elif radius_name == "m6":
        width = 5.75
        height = 10
    else:
        width = 3.5
        height = 6.5

    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_cube_center"
    p2["rotX"] = 0
    p2["rotY"] = 0
    p2["rotZ"] = 0
    p2["inclusion"] = "3dpr"
    p2["size"] = [width, height, height_layer]
    p2["pos"] = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    return_value.append(oobb.oe(**p2))

    p2 = copy.deepcopy(kwargs)
    p2["shape"] = "oobb_cube_center"
    p2["rotX"] = 0
    p2["rotY"] = 0
    p2["rotZ"] = 0
    p2["inclusion"] = "3dpr"
    p2["size"] = [width, width, height_layer]
    p2["pos"] = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    if zz == "bottom":
        p2["pos"][2] += height_layer
    else:
        p2["pos"][2] -= height_layer
    return_value.append(oobb.oe(**p2))

    return return_value


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [
        {
            "filename": "test_1",
            "preview_rot": [70, 0, 20],
            "kwargs": {"pos": [0, 0, 0], "radius_name": "m3", "zz": "bottom", "type": "positive"},
        },
        {
            "filename": "test_2",
            "preview_rot": [70, 0, 20],
            "kwargs": {"pos": [0, 0, 0], "radius_name": "m3_nut", "zz": "top", "type": "positive"},
        },
    ]

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
