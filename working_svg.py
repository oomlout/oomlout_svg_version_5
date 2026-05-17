import copy
import opsvg
import yaml
import os
import svg_help


def main(**kwargs):
    make_svg(**kwargs)

def make_svg(**kwargs):
    typ = svg_help.get_typ(**kwargs)
    oomp_mode = "project"
    #oomp_mode = "oobb"
    filt = ""
    build_variables = svg_help.get_build_variables(typ, filter=filt)
    if True:
        kwargs["filter"] = build_variables["filter"]
        kwargs["save_type"] = build_variables["save_type"]
        kwargs["navigation"] = build_variables["navigation"]
        kwargs["overwrite"] = build_variables["overwrite"]
        kwargs["oomp_mode"] = oomp_mode
    parts = get_parts(kwargs, oomp_mode)

    kwargs["parts"] = parts

    svg_help.make_parts(**kwargs)

    if kwargs["navigation"]:
        oobb_style = False
        sort = svg_help.get_navigation_sort(oobb_style=oobb_style)
        svg_help.generate_navigation(sort=sort)


def get_parts(kwargs, oomp_mode):
    parts = []

    #load parts from parts/folder/working.yaml
    parts_directory = os.path.join(os.path.dirname(__file__), "parts")
    if not os.path.isdir(parts_directory):
        return parts

    for folder in os.listdir(parts_directory):
        folder_path = os.path.join(parts_directory, folder)
        if not os.path.isdir(folder_path):
            continue

        working_yaml_path = os.path.join(folder_path, "working.yaml")
        if not os.path.isfile(working_yaml_path):
            continue

        with open(working_yaml_path, "r", encoding="utf-8") as infile:
            loaded_part = yaml.safe_load(infile)

        if not isinstance(loaded_part, dict):
            continue

        svg_details = loaded_part.get("svg_details")
        if not isinstance(svg_details, dict):
            continue

        part = loaded_part

        part_kwargs = copy.deepcopy(kwargs)
        part_kwargs.update(copy.deepcopy(loaded_part.get("kwargs", {})))
        svg_details_safe = {k: v for k, v in svg_details.items()
                            if k not in ("width", "height", "depth") or isinstance(v, (int, float))}
        part_kwargs.update(copy.deepcopy(svg_details_safe))
        part["kwargs"] = part_kwargs
        part["oobb_name"] = part.get("oobb_name", svg_details.get("svg_name", "default"))

        if oomp_mode == "oobb":
            part["kwargs"]["oomp_size"] = part["oobb_name"]

        parts.append(part)

    return parts


def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)
    rot = kwargs.get("rot", [0,0,0])
    pos = kwargs.get("pos", [0,0,0])
    extra = kwargs.get("extra", "")



    #add plate
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"oobb_plate"
        p3["depth"] = depth
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add holes
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"oobb_holes"
        p3["depth"] = depth
        p3["radius_name"] = "m6"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add text
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"text"
        p3["text"] = "Base Plate"
        p3["size"] = 10.0
        p3["font"] = "sans-serif"
        p3["halign"] = "left"
        p3["valign"] = "center"
        p3["color"] = "#000000"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    if prepare_print:
        svg_help.prepare_base_for_print(thing, pos, **kwargs)


def get_a4_sheet(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)
    rot = kwargs.get("rot", [0,0,0])
    pos = kwargs.get("pos", [0,0,0])
    extra = kwargs.get("extra", "")

    sheet_width  = 210.0
    sheet_height = 297.0

    content_inset  = 10.0
    content_width  = sheet_width  - 2 * content_inset
    content_height = sheet_height - 2 * content_inset

    #add background
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"rect"
        p3["size"] = [sheet_width, sheet_height, depth]
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add content area
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"rounded_rectangle"
        p3["size"] = [content_width, content_height, depth]
        p3["r"] = 5.0
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add title text
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"text"
        p3["text"] = "A4 Demo Sheet"
        p3["size"] = 14.0
        p3["font"] = "sans-serif"
        p3["halign"] = "center"
        p3["valign"] = "center"
        p3["color"] = "#ffffff"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[1] += sheet_height / 2 - 30.0
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add subtitle text
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"text"
        p3["text"] = "oomlout SVG pipeline"
        p3["size"] = 7.0
        p3["font"] = "sans-serif"
        p3["halign"] = "center"
        p3["valign"] = "center"
        p3["color"] = "#ffffff"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[1] += sheet_height / 2 - 48.0
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add version label
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"text"
        p3["text"] = "v1.0"
        p3["size"] = 4.0
        p3["font"] = "sans-serif"
        p3["halign"] = "right"
        p3["valign"] = "center"
        p3["color"] = "#ffffff"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += sheet_width  / 2 - 8.0
        pos1[1] -= sheet_height / 2 - 8.0
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add triangle marker
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"polygon"
        p3["points"] = [[0, 4], [-6, -4], [6, -4]]
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += sheet_width  / 2 - 20.0
        pos1[1] += sheet_height / 2 - 20.0
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add corner punch
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"circle"
        p3["r"] = 4.0
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] -= sheet_width  / 2 - 20.0
        pos1[1] += sheet_height / 2 - 20.0
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add adjustment slot
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"slot"
        p3["r"] = 3.0
        p3["w"] = 40.0
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[1] -= sheet_height / 2 - 20.0
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    if prepare_print:
        svg_help.prepare_base_for_print(thing, pos, **kwargs)


def get_label_76x50(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)
    rot = kwargs.get("rot", [0,0,0])
    pos = kwargs.get("pos", [0,0,0])
    extra = kwargs.get("extra", "")

    label_width   = 76.2
    label_height  = 50.4
    header_height = 12.0
    header_y      = label_height / 2 - header_height / 2

    #add label outline
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"rounded_rectangle"
        p3["size"] = [label_width, label_height, depth]
        p3["r"] = 3.0
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add header bar
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"rect"
        p3["size"] = [label_width, header_height, depth]
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[1] += header_y
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add header title
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"text"
        p3["text"] = "OOMLOUT"
        p3["size"] = 9.0
        p3["font"] = "sans-serif"
        p3["halign"] = "center"
        p3["valign"] = "center"
        p3["color"] = "#ffffff"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[1] += header_y
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add bullet mark
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"circle"
        p3["r"] = 1.5
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] -= label_width / 2 - 8.0
        pos1[1] += header_y - header_height - 4.0
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add part name
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"text"
        p3["text"] = "Bracket  4 x 2"
        p3["size"] = 5.0
        p3["font"] = "sans-serif"
        p3["halign"] = "left"
        p3["valign"] = "center"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] -= label_width / 2 - 13.0
        pos1[1] += header_y - header_height - 4.0
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add description
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"text"
        p3["text"] = "L-shaped laser-cut plate"
        p3["size"] = 4.0
        p3["font"] = "sans-serif"
        p3["halign"] = "left"
        p3["valign"] = "center"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] -= label_width / 2 - 6.0
        pos1[1] += header_y - header_height - 11.0
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    #add part number footer
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["shape"] = f"text"
        p3["text"] = "OOBB-BKT-4x2-001"
        p3["size"] = 3.0
        p3["font"] = "sans-serif"
        p3["halign"] = "right"
        p3["valign"] = "center"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += label_width  / 2 - 4.0
        pos1[1] -= label_height / 2 - 5.0
        p3["pos"] = pos1
        opsvg.se(thing,**p3)

    if prepare_print:
        svg_help.prepare_base_for_print(thing, pos, **kwargs)


if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)
