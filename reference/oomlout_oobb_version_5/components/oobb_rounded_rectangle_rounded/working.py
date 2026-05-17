import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


# ---------- cross-component helper imports ----------
import importlib.util
def _load_component(folder_name):
    path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
    spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_rot_mod = _load_component("oobb_rot")
get_rot = _rot_mod.action

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_rounded_rectangle_rounded'
    d["name_long"] = 'OOBB Geometry Primitives: Rounded Rectangle (Rounded Edges)'
    d["description"] = 'Rounded rectangle with rounded top and bottom edges (sphere-swept corners) wrapped in a rotation object.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['rounded_rectangle_rounded']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'size', "description": 'Overall [x,y,z] dimensions in mm.', "type": 'list', "default": '[20,10,5]'})
    v.append({"name": 'radius', "description": 'Corner radius of the base shape.', "type": 'number', "default": 5})
    v.append({"name": 'radius_rounded', "description": 'Rounding radius for top/bottom edges.', "type": 'number', "default": 2.5})
    v.append({"name": 'extra', "description": 'Extra variant/modifier string.', "type": 'string', "default": '""'})
    v.append({"name": 'rot', "description": 'Rotation [rx,ry,rz] in degrees.', "type": 'list', "default": '[0,0,0]'})
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
    import oobb
    import opsc
    """Geometry component."""
    extra = kwargs.get("extra", "")
    pos = kwargs.get("pos", [0, 0, 0])
    #rot = kwargs.get("rot",[0,0,0])
    rot = [0,0,0]
    radius = kwargs.get("radius", 5)
    radius_rounded = kwargs.get("radius_rounded", 2.5)
    size = kwargs.get("size", [20, 10, 5])
    wid = size[0]
    hei = size[1]
    dep = size[2]
    if True:

        # setting up for rotation object
        typ = kwargs.get("type", "p")
        kwargs["type"] = "positive" #needs to be positive for the difference to work
        rot_original = get_rot(**kwargs)   
        kwargs.pop("rot", None)
        kwargs.pop("rot_x", None)
        kwargs.pop("rot_y", None)
        kwargs.pop("rot_z", None)

        # storing pos and popping it out to add it in rotation element     
        pos_original = copy.deepcopy(copy.deepcopy(kwargs.get("pos", [0, 0, 0])))
        pos_original_original = copy.deepcopy(pos_original)
        kwargs.pop("pos", None)
        pos = [0,0,0]
        kwargs["pos"] = pos

        return_value = []


        #main_piece
        if True:
            size_main = copy.deepcopy(size)
            size_main[2] = size_main[2] - radius_rounded * 2

            #positive_rounded_rectangle
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "rounded_rectangle"
            p3["type"] = "positive"
            p3["size"] = size_main
            pos1 = copy.deepcopy(pos)
            pos1[2] += radius_rounded
            p3["pos"] = pos1
            return_value.append(opsc.opsc_easy(**p3))
        #top and bottom piece and rounding
        shift_z_1 = 0
        shift_z_2 = dep - radius_rounded
        if True:
            shift_z = dep/2 - radius_rounded/2
            dep_2 = radius_rounded
            wid_little = wid - radius_rounded * 2
            hei_little = hei - radius_rounded * 2
            dep_little = radius_rounded
            size_little = [wid_little, hei_little, dep_little]
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "rounded_rectangle"
            p3["type"] = "positive"
            p3["size"] = size_little
            p3["radius"] = radius - radius_rounded
            poss = []
            pos1 = copy.deepcopy(pos)
            pos11 = copy.deepcopy(pos1)
            pos11[2] += shift_z_1
            poss.append(pos11)
            pos12 = copy.deepcopy(pos1)
            pos12[2] = shift_z_2
            poss.append(pos12)
            p4 = copy.deepcopy(p3)
            p4["pos"] = pos11
            return_value.append(opsc.opsc_easy(**p4))
            p5 = copy.deepcopy(p3)
            p5["pos"] = pos12
            return_value.append(opsc.opsc_easy(**p5))
            #cylinders
            shift_x_cyl = wid/2 - radius_rounded
            dep_cyl = hei - radius*2
            dep_cyl_short = wid - radius*2
            shift_y_cyl = dep_cyl/2
            shift_z_cyl = dep_cyl/2 + radius_rounded
            shift_x_cyl_short = -dep_cyl_short/2# - radius
            shift_y_cyl_short = hei/2 - radius_rounded
            shift_z_cyl_short = dep_cyl_short/2 + radius_rounded
            if True:
                #cylinder long                
                rad_cyl = radius_rounded
                p3 = copy.deepcopy(kwargs)
                p3["shape"] = "oobb_cylinder"
                p3["type"] = "positive"
                p3["depth"] = dep_cyl
                p3["radius"] = rad_cyl
                pos1 = copy.deepcopy(pos)
                pos1[0] += shift_x_cyl
                pos1[1] += shift_y_cyl
                pos1[2] += shift_z_cyl
                pos11 = copy.deepcopy(pos1)
                p3["pos"] = pos11
                #p3["m"] = "#"
                rot1 = copy.deepcopy(rot)
                rot1[0] += 90
                p3["rot"] = rot1
                p3.pop("size", None)
                return_value.append(oobb.oobb_easy(**p3))
                p4 = copy.deepcopy(p3)
                pos12 = copy.deepcopy(pos1)
                pos12[0] += -(wid - radius_rounded*2)
                p4["pos"] = pos12
                return_value.append(oobb.oobb_easy(**p4))
                p5 = copy.deepcopy(p3)
                pos13 = copy.deepcopy(pos1)
                pos13[2] += dep - radius_rounded*2
                p5["pos"] = pos13
                return_value.append(oobb.oobb_easy(**p5))
                p6 = copy.deepcopy(p3)
                pos14 = copy.deepcopy(pos1)
                pos14[0] += -(wid - radius_rounded*2)
                pos14[2] += dep - radius_rounded*2
                p6["pos"] = pos14
                return_value.append(oobb.oobb_easy(**p6))
                #cylinder_short
                rad_cyl = radius_rounded
                p3 = copy.deepcopy(kwargs)
                p3["shape"] = "oobb_cylinder"
                p3["type"] = "positive"
                p3["depth"] = dep_cyl_short
                p3["radius"] = rad_cyl
                pos1 = copy.deepcopy(pos)
                pos1[0] += shift_x_cyl_short
                pos1[1] += shift_y_cyl_short
                pos1[2] += shift_z_cyl_short
                pos11 = copy.deepcopy(pos1)
                p3["pos"] = pos11
                #p3["m"] = "#"
                rot1 = copy.deepcopy(rot)
                rot1[1] += 90
                p3["rot"] = rot1
                p3.pop("size", None)
                return_value.append(oobb.oobb_easy(**p3))
                p4 = copy.deepcopy(p3)
                pos12 = copy.deepcopy(pos1)
                pos12[1] += -(hei - radius_rounded*2)
                p4["pos"] = pos12
                return_value.append(oobb.oobb_easy(**p4))
                p5 = copy.deepcopy(p3)
                pos13 = copy.deepcopy(pos1)
                pos13[2] += dep - radius_rounded*2
                p5["pos"] = pos13
                return_value.append(oobb.oobb_easy(**p5))
                p6 = copy.deepcopy(p3)
                pos14 = copy.deepcopy(pos1)
                pos14[1] += -(hei - radius_rounded*2)
                pos14[2] += dep - radius_rounded*2
                p6["pos"] = pos14
                return_value.append(oobb.oobb_easy(**p6))
                #corner_spheres
                if True:
                    p3 = copy.deepcopy(kwargs)
                    p3["shape"] = "oring"
                    p3["depth"] = radius_rounded * 2
                    p3["id"] = radius - radius_rounded*2
                    pos1 = copy.deepcopy(pos)
                    pos1[2] += radius_rounded
                    pos11 = copy.deepcopy(pos1)
                    pos11[0] += -wid/2 + radius
                    pos11[1] += -hei/2 + radius
                    pos11[2] += 0
                    p3["pos"] = pos11
                    p3.pop("size", None)
                    #p3["m"] = "#"   
                    return_value.append(oobb.oobb_easy(**p3))
                    p4 = copy.deepcopy(p3)
                    pos12 = copy.deepcopy(pos1)
                    pos12[0] += wid/2 - radius
                    pos12[1] += -hei/2 + radius
                    p4["pos"] = pos12
                    return_value.append(oobb.oobb_easy(**p4))
                    p5 = copy.deepcopy(p3)
                    pos13 = copy.deepcopy(pos1)
                    pos13[0] += wid/2 - radius
                    pos13[1] += hei/2 - radius
                    p5["pos"] = pos13
                    return_value.append(oobb.oobb_easy(**p5))
                    p6 = copy.deepcopy(p3)
                    pos14 = copy.deepcopy(pos1)
                    pos14[0] += -wid/2 + radius
                    pos14[1] += hei/2 - radius
                    p6["pos"] = pos14
                    return_value.append(oobb.oobb_easy(**p6))
                    p7 = copy.deepcopy(p3)
                    pos15 = copy.deepcopy(pos1)
                    pos15[0] += -wid/2 + radius
                    pos15[1] += -hei/2 + radius
                    pos15[2] += dep - radius_rounded*2
                    p7["pos"] = pos15
                    return_value.append(oobb.oobb_easy(**p7))
                    p8 = copy.deepcopy(p3)
                    pos16 = copy.deepcopy(pos1)
                    pos16[0] += wid/2 - radius
                    pos16[1] += -hei/2 + radius
                    pos16[2] += dep - radius_rounded*2
                    p8["pos"] = pos16
                    return_value.append(oobb.oobb_easy(**p8))
                    p9 = copy.deepcopy(p3)
                    pos17 = copy.deepcopy(pos1)
                    pos17[0] += wid/2 - radius
                    pos17[1] += hei/2 - radius
                    pos17[2] += dep - radius_rounded*2
                    p9["pos"] = pos17
                    return_value.append(oobb.oobb_easy(**p9))
                    p10 = copy.deepcopy(p3)
                    pos18 = copy.deepcopy(pos1)
                    pos18[0] += -wid/2 + radius
                    pos18[1] += hei/2 - radius
                    pos18[2] += dep - radius_rounded*2
                    p10["pos"] = pos18
                    return_value.append(oobb.oobb_easy(**p10))



        #pos = copy.deepcopy(p3.get("pos", [0, 0, 0]))
        #pos[2] += 50
        #p3["pos"] = pos


        #p3["m"] = "#"
        return_value.append(opsc.opsc_easy(**p3))

        # packaging as a rotation object
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = typ
        return_value_2["pos"] = pos_original
        return_value_2["rot"] = rot_original
        return_value_2["objects"] = return_value
        return_value_2 = [return_value_2]

        return return_value_2     


    #sphere with squash ability


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [55, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'size': [30, 20, 8],
                 'radius': 5,
                 'radius_rounded': 2,
                 'extra': '',
                 'rot': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [55, 0, 25],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'size': [36, 24, 10],
                 'radius': 6,
                 'radius_rounded': 3,
                 'extra': '',
                 'rot': [0, 0, 0]}}]

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


