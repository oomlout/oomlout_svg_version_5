import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_COMPONENT_ROOT = os.path.dirname(os.path.abspath(__file__))
_WRAPPER_FILE = os.path.join(_COMPONENT_ROOT, "gridfinity_tray_raw_wrapper.scad")

d = {}

MODULE_DEFAULTS = {
    "gridfinity_width": 2,
    "gridfinity_height": 1,
    "gridfinity_depth": 3,
    "filled_in": "disabled",
    "wall_thickness": 0,
    "headroom": 0.8,
    "lip_style": "normal",
    "lip_side_relief_trigger": [1, 1],
    "lip_top_relief_height": -1,
    "lip_top_relief_width": -1,
    "lip_top_notches": True,
    "lip_clip_position": "disabled",
    "lip_non_blocking": False,
    "height_includes_lip": False,
    "chamber_wall_thickness": [1.2, 1.2],
    "chamber_wall_headroom": 0,
    "chamber_wall_top_radius": 0,
    "vertical_chambers": 1,
    "vertical_separator_bend_separation": 0,
    "vertical_separator_bend_angle": 45,
    "vertical_separator_bend_position": 0,
    "vertical_separator_cut_depth": 0,
    "horizontal_chambers": 1,
    "horizontal_separator_bend_separation": 0,
    "horizontal_separator_bend_angle": 45,
    "horizontal_separator_bend_position": 0,
    "horizontal_separator_cut_depth": 0,
    "vertical_irregular_subdivisions": False,
    "vertical_separator_config": "10.5|21|42|50|60",
    "horizontal_irregular_subdivisions": False,
    "horizontal_separator_config": "10.5|21|42|50|60",
    "enable_magnets": False,
    "enable_screws": False,
    "magnet_size": [6.5, 2.4],
    "magnet_easy_release": "auto",
    "magnet_side_access": "disabled",
    "magnet_captive_height": 0,
    "magnet_crush_depth": 0,
    "magnet_chamfer": 0,
    "screw_size": [3, 6],
    "center_magnet_size": [0, 0],
    "hole_overhang_remedy": 2,
    "box_corner_attachments_only": "enabled",
    "floor_thickness": 0.7,
    "cavity_floor_radius": -1,
    "efficient_floor": "off",
    "sub_pitch": 1,
    "flat_base": "off",
    "spacer": False,
    "minimum_printable_pad_size": 0.2,
    "flat_base_rounded_radius": -1,
    "flat_base_rounded_easyPrint": -1,
    "align_grid_x": "near",
    "align_grid_y": "near",
    "label_style": "disabled",
    "label_position": "left",
    "label_dividers": "disabled",
    "label_size": [0, 14, 0, 0.6],
    "label_relief": [0, 0, 0, 0.6],
    "label_walls": [0, 1, 0, 0],
    "sliding_lid_enabled": False,
    "sliding_lid_thickness": 0,
    "sliding_lid_min_wall_thickness": 0,
    "sliding_lid_min_support": 0,
    "sliding_lid_clearance": 0.1,
    "sliding_lid_pull_style": "disabled",
    "sliding_lid_nub_size": 0.5,
    "fingerslide": "none",
    "fingerslide_radius": -3,
    "fingerslide_walls": [1, 0, 0, 0],
    "fingerslide_lip_aligned": True,
    "tapered_corner": "none",
    "tapered_corner_size": 10,
    "tapered_setback": -1,
    "wallpattern_enabled": False,
    "wallpattern_style": "hexgrid",
    "wallpattern_strength": 2,
    "wallpattern_walls": [1, 1, 1, 1],
    "wallpattern_rotate_grid": False,
    "wallpattern_cell_size": [10, 10],
    "wallpattern_dividers_enabled": "disabled",
    "wallpattern_hole_sides": 6,
    "wallpattern_hole_radius": 0.5,
    "wallpattern_fill": "none",
    "wallpattern_border": 0,
    "wallpattern_depth": 0,
    "wallpattern_pattern_grid_chamfer": 0,
    "wallpattern_pattern_voronoi_noise": 0.75,
    "wallpattern_pattern_brick_weight": 5,
    "wallpattern_pattern_quality": 0.4,
    "wallpattern_colored": "disabled",
    "floorpattern_enabled": False,
    "floorpattern_style": "hexgrid",
    "floorpattern_strength": 2,
    "floorpattern_rotate_grid": False,
    "floorpattern_cell_size": [10, 10],
    "floorpattern_hole_sides": 6,
    "floorpattern_hole_radius": 0.5,
    "floorpattern_fill": "crop",
    "floorpattern_border": 0,
    "floorpattern_depth": 0,
    "floorpattern_pattern_grid_chamfer": 0,
    "floorpattern_pattern_voronoi_noise": 0.75,
    "floorpattern_pattern_brick_weight": 5,
    "floorpattern_pattern_quality": 0.4,
    "wallcutout_vertical": "disabled",
    "wallcutout_vertical_position": [-2, -0.5, -0.5, -0.5],
    "wallcutout_vertical_width": 0,
    "wallcutout_vertical_angle": 70,
    "wallcutout_vertical_height": 0,
    "wallcutout_vertical_corner_radius": 5,
    "wallcutout_horizontal": "disabled",
    "wallcutout_horizontal_position": [-2, -0.5, -0.5, -0.5],
    "wallcutout_horizontal_width": 0,
    "wallcutout_horizontal_angle": 70,
    "wallcutout_horizontal_height": 0,
    "wallcutout_horizontal_corner_radius": 5,
    "extension_x_enabled": "disabled",
    "extension_x_position": 0.5,
    "extension_y_enabled": "disabled",
    "extension_y_position": 0.5,
    "extension_tabs_enabled": True,
    "extension_tab_size": [10, 0, 0, 0],
    "text_1": False,
    "text_size": 0,
    "text_depth": 0.3,
    "text_offset": [0, 0],
    "text_font": "Aldo",
    "text_2": False,
    "text_2_text": "Gridfinity Extended",
    "cut": [0, 0, 0],
    "enable_help": "disabled",
    "pitch": [42, 42, 7],
    "clearance": [0.5, 0.5, 0],
    "set_colour": "enable",
    "render_position": "center",
    "fa": 6,
    "fs": 0.4,
    "fn": 0,
    "random_seed": 0,
    "force_render": True,
}


def _variable(name, description, value_type, default):
    return {"name": name, "description": description, "type": value_type, "default": default}


def describe():
    global d
    d = {}
    d["name"] = "gridfinity_tray_raw"
    d["name_long"] = "Gridfinity: Tray Raw"
    d["description"] = (
        "Returns a raw OpenSCAD wrapper around the vendored Gridfinity Extended basic cup, "
        "using repo-style public size inputs where gridfinity_width is X, gridfinity_height is Y, "
        "and gridfinity_depth is Z."
    )
    d["category"] = "Gridfinity"
    d["shape_aliases"] = ["gridfinity_tray_raw"]
    d["returns"] = "Raw SCAD geometry component dict."
    d["source"] = "https://github.com/ostat/gridfinity_extended_openscad"
    d["notes"] = [
        "Backed by the vendored Gridfinity Extended basic cup implementation.",
        "Additional wrapper kwargs matching the local SCAD module parameters are forwarded to the raw SCAD wrapper.",
    ]
    v = []
    v.append(_variable("gridfinity_width", "Width in Gridfinity units along X.", "number", 2))
    v.append(_variable("gridfinity_height", "Height in Gridfinity units along Y.", "number", 1))
    v.append(_variable("gridfinity_depth", "Depth in Gridfinity units along Z.", "number", 3))
    v.append(_variable("filled_in", "Fill the cup into a solid block or fill the lip.", "string", '"disabled"'))
    v.append(_variable("wall_thickness", "Outer wall thickness in mm. Zero uses upstream auto sizing.", "number", 0))
    v.append(_variable("headroom", "Undersize the top by this amount for easier stacking.", "number", 0.8))
    v.append(_variable("lip_style", "Cup lip style.", "string", '"normal"'))
    v.append(_variable("vertical_chambers", "Number of vertical chambers.", "number", 1))
    v.append(_variable("horizontal_chambers", "Number of horizontal chambers.", "number", 1))
    v.append(_variable("enable_magnets", "Enable base magnet holes.", "bool", False))
    v.append(_variable("enable_screws", "Enable base screw holes.", "bool", False))
    v.append(_variable("magnet_size", "Magnet diameter and height [d,h] in mm.", "list", "[6.5,2.4]"))
    v.append(_variable("screw_size", "Screw diameter and height [d,h] in mm.", "list", "[3,6]"))
    v.append(_variable("floor_thickness", "Minimum thickness above cutouts in the base.", "number", 0.7))
    v.append(_variable("efficient_floor", "Efficient floor mode.", "string", '"off"'))
    v.append(_variable("sub_pitch", "Bottom pad subdivision pitch.", "number", 1))
    v.append(_variable("flat_base", "Internal base style.", "string", '"off"'))
    v.append(_variable("label_style", "Label style.", "string", '"disabled"'))
    v.append(_variable("label_position", "Label position.", "string", '"left"'))
    v.append(_variable("sliding_lid_enabled", "Enable the sliding lid geometry.", "bool", False))
    v.append(_variable("fingerslide", "Finger slide style.", "string", '"none"'))
    v.append(_variable("tapered_corner", "Tapered corner style.", "string", '"none"'))
    v.append(_variable("wallpattern_enabled", "Enable wall cutout patterns.", "bool", False))
    v.append(_variable("floorpattern_enabled", "Enable floor patterns.", "bool", False))
    v.append(_variable("wallcutout_vertical", "Vertical wall cutout mode.", "string", '"disabled"'))
    v.append(_variable("wallcutout_horizontal", "Horizontal wall cutout mode.", "string", '"disabled"'))
    v.append(_variable("extension_x_enabled", "Extendable tab mode on X.", "string", '"disabled"'))
    v.append(_variable("extension_y_enabled", "Extendable tab mode on Y.", "string", '"disabled"'))
    v.append(_variable("text_1", "Add the bin size to the bottom text.", "bool", False))
    v.append(_variable("text_2", "Enable custom bottom text.", "bool", False))
    v.append(_variable("text_2_text", "Custom bottom text value.", "string", '"Gridfinity Extended"'))
    v.append(_variable("pitch", "Gridfinity pitch [x,y,z] in mm.", "list", "[42,42,7]"))
    v.append(_variable("clearance", "Clearance [x,y,z] in mm.", "list", "[0.5,0.5,0]"))
    v.append(_variable("set_colour", "Color handling mode for the upstream renderer.", "string", '"enable"'))
    v.append(_variable("render_position", "Upstream render position mode.", "string", '"center"'))
    v.append(_variable("fa", "OpenSCAD fragment angle.", "number", 6))
    v.append(_variable("fs", "OpenSCAD fragment size.", "number", 0.4))
    v.append(_variable("fn", "OpenSCAD fragment count override.", "number", 0))
    v.append(_variable("random_seed", "Random seed for procedural features.", "number", 0))
    v.append(_variable("force_render", "Force render on costly upstream components.", "bool", True))
    v.append(_variable("pos", "3-element [x,y,z] position.", "list", "[0,0,0]"))
    v.append(_variable("rot", "Rotation [rx,ry,rz] in degrees.", "list", "[0,0,0]"))
    v.append(_variable("type", "Geometry type: positive or negative.", "string", '"positive"'))
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable


def _resolve_gridfinity_size_inputs(kwargs):
    return {
        "gridfinity_width": copy.deepcopy(
            kwargs.get("gridfinity_width", kwargs.get("width", MODULE_DEFAULTS["gridfinity_width"]))
        ),
        "gridfinity_height": copy.deepcopy(
            kwargs.get("gridfinity_height", kwargs.get("height", MODULE_DEFAULTS["gridfinity_height"]))
        ),
        "gridfinity_depth": copy.deepcopy(
            kwargs.get("gridfinity_depth", kwargs.get("depth", MODULE_DEFAULTS["gridfinity_depth"]))
        ),
    }


def action(**kwargs):
    module_kwargs = {
        key: copy.deepcopy(kwargs.get(key, default_value))
        for key, default_value in MODULE_DEFAULTS.items()
    }
    module_kwargs.update(_resolve_gridfinity_size_inputs(kwargs))
    return_value = {
        "type": kwargs.get("type", kwargs.get("t", "positive")),
        "shape": "raw_scad",
        "file": _WRAPPER_FILE,
        "module": "gridfinity_tray_raw",
        "module_kwargs": module_kwargs,
        "pos": copy.deepcopy(kwargs.get("pos", [0, 0, 0])),
        "rot": copy.deepcopy(kwargs.get("rot", [0, 0, 0])),
        "inclusion": kwargs.get("inclusion", "all"),
        "m": kwargs.get("m", ""),
    }
    return return_value


def test():
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [
        {
            "filename": "test_1",
            "preview_rot": [55, 0, 25],
            "kwargs": {
                "gridfinity_width": 2,
                "gridfinity_height": 1,
                "gridfinity_depth": 3,
                "pos": [0, 0, 0],
                "rot": [0, 0, 0],
                "type": "positive",
            },
        },
        {
            "filename": "test_2",
            "preview_rot": [55, 0, 25],
            "kwargs": {
                "width": 2,
                "height": 1,
                "depth": 3,
                "vertical_chambers": 2,
                "label_style": "normal",
                "label_position": "center",
                "pos": [0, 0, 0],
                "rot": [0, 0, 0],
                "type": "positive",
            },
        },
    ]

    generated_files = []

    for sample in samples:
        result = action(**copy.deepcopy(sample["kwargs"]))
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