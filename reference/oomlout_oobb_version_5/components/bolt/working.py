d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bolt'
    d["name_long"] = 'Fasteners: Bolt'
    d["description"] = 'Generates a hex-head bolt with specified size and length.'
    d["category"] = 'Fasteners'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'radius_name', "description": 'Bolt size designation, e.g. m5, m6.', "type": 'string', "default": '"m6"'})
    v.append({"name": 'depth', "description": 'Bolt length in mm.', "type": 'number', "default": 20})
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
    """Build and return the bolt thing dict."""
    import oobb_base as ob

    wid = kwargs["radius_name"]
    depth = kwargs["depth"]
    thing = ob.get_default_thing(**kwargs)
    thing.update({"description": f"bolt {wid}x{depth}"})
    thing.update({"depth_mm": depth})

    thing.update({"components": []})
    thing["components"].extend(ob.oe(
        t="positive", s="oobb_bolt", rn=wid, depth=depth, rotY=0, include_nut=False))

    return thing


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1', 'preview_rot': [70, 0, 20], 'kwargs': {'radius_name': 'm6', 'depth': 25}},
     {'filename': 'test_2', 'preview_rot': [70, 0, 20], 'kwargs': {'radius_name': 'm3', 'depth': 16}}]

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


