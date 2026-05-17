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
    d["name"] = 'oobb_cylinder'
    d["name_long"] = 'OOBB Geometry Primitives: Cylinder'
    d["description"] = 'Cylinder geometry across all render modes, supporting named, explicit, or dual-end radii and z-centering.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'depth', "description": 'Cylinder height in mm.', "type": 'number', "default": 250})
    v.append({"name": 'radius_name', "description": 'Named radius for mode-aware lookup.', "type": 'string', "default": '""'})
    v.append({"name": 'radius', "description": 'Explicit radius in mm.', "type": 'number', "default": 0})
    v.append({"name": 'radius_1', "description": 'Explicit start radius in mm for tapered cylinders.', "type": 'number', "default": 0})
    v.append({"name": 'radius_2', "description": 'Explicit end radius in mm for tapered cylinders.', "type": 'number', "default": 0})
    v.append({"name": 'zz', "description": 'Z anchor point: center, bottom, top.', "type": 'string', "default": '"center"'})
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
    import opsc
    """Geometry component."""
    zz = kwargs.get("zz", "center")
    radius_name = kwargs.get("radius_name", "")

    modes = ["laser", "3dpr", "true"]
    return_value = []
    # deciding how to define depth either string or name
    try:
        depth = kwargs["depth"]
    except:
        try:
            depth = kwargs["depth_mm"]
        except:
            depth = 250
    # figuring out z so it is in the middle of the object
    try:
        kwargs["pos"][2] = kwargs["pos"][2] - depth / 2
    except:
        try:
            kwargs["z"] = kwargs["z"] - depth / 2
        except:
            pass
    if zz == "bottom":
        kwargs["pos"][2] += depth / 2
    if zz == "top":
        kwargs["pos"][2] -= depth / 2

    for mode in modes:
        kwargs["shape"] = "cylinder"
        has_explicit_r = "r" in kwargs or "r1" in kwargs or "r2" in kwargs or "radius" in kwargs or "radius_1" in kwargs or "radius_2" in kwargs
        if radius_name != "" and not has_explicit_r:
            kwargs.update({"r": oobb.gv(radius_name, mode)})
        else:
            try:
                kwargs.update({"r": kwargs["radius"]})
            except:
                try:
                    kwargs.update({"r": kwargs["r"]})
                except:
                    #using r1 and r2
                    try:
                        kwargs.update({"r1": kwargs["radius_1"]})
                        kwargs.update({"r2": kwargs["radius_2"]})
                    except:
                        try:
                            kwargs.update({"r1": kwargs["r1"]})
                            kwargs.update({"r2": kwargs["r2"]})
                        except:
                            print("no radius defined errror in oobb_get_items get_oobb_cylinder")
                            pass

                    pass

        if isinstance(depth, str):
            kwargs.update({"h": oobb.gv(depth, mode)})
        else:
            kwargs.update({"h": depth})
        kwargs.update({"inclusion": mode})
        return_value.append(opsc.opsc_easy(**kwargs))
    return return_value

    # electronic

    #      battery_box


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [45, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'depth': 12, 'radius_name': 'hole_radius_m6', 'zz': 'center'}},
     {'filename': 'test_2',
      'preview_rot': [45, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'depth': 18, 'radius': 6, 'zz': 'center'}}]

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


