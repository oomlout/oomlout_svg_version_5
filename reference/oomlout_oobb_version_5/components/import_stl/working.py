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
    d["name"] = "import_stl"
    d["name_long"] = "OPSC Geometry Primitives: Import STL"
    d["description"] = "Imported STL primitive exposed through the component system."
    d["category"] = "OPSC Geometry Primitives"
    d["shape_aliases"] = ["import_stl"]
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
    params["shape"] = "import_stl"
    return [opsc.opsc_easy(**params)]


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [35, 0, 25],
      'kwargs': {'type': 'positive',
                 'file': 'test_assets/sample_block.stl',
                 'scale': 1,
                 'pos': [0, 0, 0]}}]

    fixture_rel = os.path.join("test_assets", "sample_block.stl")
    fixture_path = os.path.join(folder, fixture_rel)
    if not os.path.exists(fixture_path):
        os.makedirs(os.path.dirname(fixture_path), exist_ok=True)
        fixture_source = 'solid sample_block\nfacet normal 0 0 -1\nouter loop\nvertex 0 0 0\nvertex 10 10 0\nvertex 10 0 0\nendloop\nendfacet\nfacet normal 0 0 -1\nouter loop\nvertex 0 0 0\nvertex 0 10 0\nvertex 10 10 0\nendloop\nendfacet\nfacet normal 0 0 1\nouter loop\nvertex 0 0 5\nvertex 10 0 5\nvertex 10 10 5\nendloop\nendfacet\nfacet normal 0 0 1\nouter loop\nvertex 0 0 5\nvertex 10 10 5\nvertex 0 10 5\nendloop\nendfacet\nfacet normal 0 -1 0\nouter loop\nvertex 0 0 0\nvertex 10 0 0\nvertex 10 0 5\nendloop\nendfacet\nfacet normal 0 -1 0\nouter loop\nvertex 0 0 0\nvertex 10 0 5\nvertex 0 0 5\nendloop\nendfacet\nfacet normal 0 1 0\nouter loop\nvertex 0 10 0\nvertex 0 10 5\nvertex 10 10 5\nendloop\nendfacet\nfacet normal 0 1 0\nouter loop\nvertex 0 10 0\nvertex 10 10 5\nvertex 10 10 0\nendloop\nendfacet\nfacet normal -1 0 0\nouter loop\nvertex 0 0 0\nvertex 0 0 5\nvertex 0 10 5\nendloop\nendfacet\nfacet normal -1 0 0\nouter loop\nvertex 0 0 0\nvertex 0 10 5\nvertex 0 10 0\nendloop\nendfacet\nfacet normal 1 0 0\nouter loop\nvertex 10 0 0\nvertex 10 10 0\nvertex 10 10 5\nendloop\nendfacet\nfacet normal 1 0 0\nouter loop\nvertex 10 0 0\nvertex 10 10 5\nvertex 10 0 5\nendloop\nendfacet\nendsolid sample_block\n'
        with open(fixture_path, "w", encoding="utf-8") as fixture_file:
            fixture_file.write(fixture_source)

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


