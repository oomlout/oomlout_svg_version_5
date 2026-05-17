import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_rot'
    d["name_long"] = 'OOBB Geometry Helpers: Rotation Helper'
    d["description"] = 'Helper that extracts and returns a [rx,ry,rz] rotation list from kwargs.'
    d["category"] = 'OOBB Geometry Helpers'
    d["shape_aliases"] = []
    d["returns"] = 'List [rx, ry, rz].'
    v = []
    v.append({"name": 'rot', "description": 'Explicit [rx,ry,rz] rotation list; returned directly if present.', "type": 'list', "default": '""'})
    v.append({"name": 'rot_x', "description": 'X rotation in degrees.', "type": 'number', "default": 0})
    v.append({"name": 'rot_y', "description": 'Y rotation in degrees.', "type": 'number', "default": 0})
    v.append({"name": 'rot_z', "description": 'Z rotation in degrees.', "type": 'number', "default": 0})
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
    """Extract rotation from kwargs. Returns rot list."""
    rot = kwargs.get("rot", "")
    if rot == "":
        rot_x = kwargs.get('rot_x', 0)
        rot_y = kwargs.get('rot_y', 0)
        rot_z = kwargs.get('rot_z', 0)
        rot = [rot_x, rot_y, rot_z]
        kwargs["rot"] = rot
        kwargs.pop('rot_x', None)
        kwargs.pop('rot_y', None)
        kwargs.pop('rot_z', None)
        kwargs.pop("rot", None)
    return rot


def test():
    import copy
    import os
    import oobb
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [0, 0, 0],
      'helper_kwargs': {'rot': [30, 20, 10]},
      'companion_geometry_kwargs': {'shape': 'cube',
                                    'type': 'positive',
                                    'size': [24, 18, 12],
                                    'pos': [0, 0, 0]}}]

    generated_files = []

    for sample in samples:
        helper_kwargs = copy.deepcopy(sample["helper_kwargs"])
        companion_kwargs = copy.deepcopy(sample["companion_geometry_kwargs"])
        companion_kwargs["rot"] = action(**helper_kwargs)

        result = oobb.oobb_easy(**companion_kwargs)
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


