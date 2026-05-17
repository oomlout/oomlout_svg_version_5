import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_COMPONENT_ROOT = os.path.dirname(os.path.abspath(__file__))
_WRAPPER_FILE = os.path.join(_COMPONENT_ROOT, "gridfinity_base_raw_wrapper.scad")

d = {}

MODULE_DEFAULTS = {
    "gridfinity_width": 2,
    "gridfinity_height": 1,
    "outer_width": [0, 0],
    "outer_depth": [0, 0],
    "outer_height": 0,
    "oversize_method": "fill",
    "position_fill_grid_x": "near",
    "position_fill_grid_y": "near",
    "position_grid_in_outer_x": "center",
    "position_grid_in_outer_y": "center",
    "plate_corner_radius": 3.75,
    "secondary_corner_radius": 3.75,
    "corner_roles": [1, 1, 1, 1],
    "enable_magnets": False,
    "magnet_size": [6.5, 2.4],
    "magnet_z_offset": 0,
    "magnet_top_cover": 0,
    "magnet_release_method": "none",
    "reduced_wall_height": -1,
    "reduce_wall_taper": False,
    "corner_screw_enabled": False,
    "center_screw_enabled": False,
    "weighted_enable": False,
    "plate_options": "default",
    "custom_grid_enabled": False,
    "grid_positions": [[1]],
    "remove_bottom_taper": False,
    "connector_only": False,
    "connector_position": "center_wall",
    "connector_clip_enabled": False,
    "connector_clip_size": 10,
    "connector_clip_tolerance": 0.1,
    "connector_butterfly_enabled": False,
    "connector_butterfly_size": [5, 4, 1.5],
    "connector_butterfly_radius": 0.1,
    "connector_butterfly_tolerance": 0.1,
    "connector_filament_enabled": False,
    "connector_filament_diameter": 2,
    "connector_filament_length": 8,
    "connector_snaps_style": "disabled",
    "connector_snaps_clearance": 0.5,
    "pitch": [42, 42, 7],
    "clearance": [0.5, 0.5, 0],
    "set_colour": "enable",
    "render_position": "center",
    "cut": [0, 0, 0],
    "enable_help": False,
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
    d["name"] = "gridfinity_base_raw"
    d["name_long"] = "Gridfinity: Base Raw"
    d["description"] = (
        "Returns a raw OpenSCAD wrapper around the vendored Gridfinity Extended baseplate generator, "
        "using repo-style width and height inputs while keeping a broad first-pass upstream option surface."
    )
    d["category"] = "Gridfinity"
    d["shape_aliases"] = ["gridfinity_base_raw"]
    d["returns"] = "Raw SCAD geometry component dict."
    d["source"] = "https://github.com/ostat/gridfinity_extended_openscad"
    d["notes"] = [
        "Backed by a self-contained vendored copy of Gridfinity Extended inside this component folder.",
        "gridfinity_width and gridfinity_height accept either grid-unit numbers or upstream-style [grid,mm] tuples.",
        "Legacy gridfinity_depth and depth aliases are still accepted for compatibility.",
        "The wrapper converts public size inputs into both the upstream environment dimensions and the scalar baseplate cell counts.",
    ]

    variables = []
    variables.append(_variable("gridfinity_width", "Width in Gridfinity units along X, or [grid,mm].", "number|list", 2))
    variables.append(_variable("gridfinity_height", "Height in Gridfinity units along Y, or [grid,mm].", "number|list", 1))
    variables.append(_variable("outer_width", "Outer width in Gridfinity units or [grid,mm].", "number|list", "[0,0]"))
    variables.append(_variable("outer_depth", "Outer depth in Gridfinity units or [grid,mm].", "number|list", "[0,0]"))
    variables.append(_variable("outer_height", "Outer frame height in millimeters.", "number", 0))
    variables.append(_variable("oversize_method", "Oversize method: fill, crop, or outer.", "string", '"fill"'))
    variables.append(_variable("position_fill_grid_x", "X alignment for filling partial grid space.", "string", '"near"'))
    variables.append(_variable("position_fill_grid_y", "Y alignment for filling partial grid space.", "string", '"near"'))
    variables.append(_variable("position_grid_in_outer_x", "X alignment of the grid inside the outer frame.", "string", '"center"'))
    variables.append(_variable("position_grid_in_outer_y", "Y alignment of the grid inside the outer frame.", "string", '"center"'))
    variables.append(_variable("plate_corner_radius", "Outer plate corner radius in millimeters.", "number", 3.75))
    variables.append(_variable("secondary_corner_radius", "Secondary inner corner radius in millimeters.", "number", 3.75))
    variables.append(_variable("enable_magnets", "Enable baseplate magnet pockets.", "bool", False))
    variables.append(_variable("magnet_size", "Magnet diameter and height [d,h] in millimeters.", "list", "[6.5,2.4]"))
    variables.append(_variable("magnet_release_method", "Magnet release method: none, slot, or hole.", "string", '"none"'))
    variables.append(_variable("corner_screw_enabled", "Enable corner screw holes.", "bool", False))
    variables.append(_variable("center_screw_enabled", "Enable the center hold-down screw hole.", "bool", False))
    variables.append(_variable("weighted_enable", "Enable weight cavities in the frame.", "bool", False))
    variables.append(_variable("reduced_wall_height", "Reduced wall height in millimeters. -1 keeps upstream behavior.", "number", -1))
    variables.append(_variable("reduce_wall_taper", "Reduce wall taper when walls are shortened.", "bool", False))
    variables.append(_variable("plate_options", "Baseplate style option, typically default or cnclaser.", "string", '"default"'))
    variables.append(_variable("custom_grid_enabled", "Enable custom grid cell layout.", "bool", False))
    variables.append(_variable("grid_positions", "Custom grid positions matrix passed to the upstream baseplate module.", "list", "[[1]]"))
    variables.append(_variable("remove_bottom_taper", "Remove the default Gridfinity bottom taper.", "bool", False))
    variables.append(_variable("connector_only", "Generate connector-only geometry for the frame system.", "bool", False))
    variables.append(_variable("connector_position", "Frame connector position: disabled, center_wall, intersection, or both.", "string", '"center_wall"'))
    variables.append(_variable("connector_clip_enabled", "Enable clip-style frame connectors.", "bool", False))
    variables.append(_variable("connector_butterfly_enabled", "Enable butterfly frame connectors.", "bool", False))
    variables.append(_variable("connector_filament_enabled", "Enable filament frame connectors.", "bool", False))
    variables.append(_variable("connector_snaps_style", "Connector snap style: disabled, larger, smaller, or wall.", "string", '"disabled"'))
    variables.append(_variable("pitch", "Gridfinity pitch [x,y,z] in millimeters.", "list", "[42,42,7]"))
    variables.append(_variable("clearance", "Environment clearance [x,y,z] in millimeters.", "list", "[0.5,0.5,0]"))
    variables.append(_variable("set_colour", "Color handling mode for the upstream renderer.", "string", '"enable"'))
    variables.append(_variable("render_position", "Render position mode, usually center.", "string", '"center"'))
    variables.append(_variable("cut", "Debug cut [x,y,z].", "list", "[0,0,0]"))
    variables.append(_variable("fa", "OpenSCAD fragment angle.", "number", 6))
    variables.append(_variable("fs", "OpenSCAD fragment size.", "number", 0.4))
    variables.append(_variable("fn", "OpenSCAD fragment count override.", "number", 0))
    variables.append(_variable("random_seed", "Random seed for the upstream environment.", "number", 0))
    variables.append(_variable("force_render", "Force render on costly upstream components.", "bool", True))
    variables.append(_variable("pos", "3-element [x,y,z] position.", "list", "[0,0,0]"))
    variables.append(_variable("rot", "Rotation [rx,ry,rz] in degrees.", "list", "[0,0,0]"))
    variables.append(_variable("type", "Geometry type: positive or negative.", "string", '"positive"'))
    d["variables"] = variables
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable


def _resolve_dimension_input(kwargs, public_name, alias_name, default_value):
    if public_name in kwargs:
        return copy.deepcopy(kwargs[public_name])
    if alias_name in kwargs:
        return copy.deepcopy(kwargs[alias_name])
    return copy.deepcopy(default_value)


def _resolve_gridfinity_size_inputs(kwargs):
    return {
        "gridfinity_width": _resolve_dimension_input(
            kwargs, "gridfinity_width", "width", MODULE_DEFAULTS["gridfinity_width"]
        ),
        "gridfinity_height": _resolve_dimension_input(
            kwargs,
            "gridfinity_height",
            "height",
            _resolve_dimension_input(kwargs, "gridfinity_depth", "depth", MODULE_DEFAULTS["gridfinity_height"]),
        ),
    }


def action(**kwargs):
    module_kwargs = {
        key: copy.deepcopy(kwargs.get(key, default_value))
        for key, default_value in MODULE_DEFAULTS.items()
    }
    module_kwargs.update(_resolve_gridfinity_size_inputs(kwargs))

    return {
        "type": kwargs.get("type", kwargs.get("t", "positive")),
        "shape": "raw_scad",
        "file": _WRAPPER_FILE,
        "module": "gridfinity_base_raw",
        "module_kwargs": module_kwargs,
        "pos": copy.deepcopy(kwargs.get("pos", [0, 0, 0])),
        "rot": copy.deepcopy(kwargs.get("rot", [0, 0, 0])),
        "inclusion": kwargs.get("inclusion", "all"),
        "m": kwargs.get("m", ""),
    }


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
                "pos": [0, 0, 0],
                "rot": [0, 0, 0],
                "type": "positive",
            },
        },
        {
            "filename": "test_2",
            "preview_rot": [55, 0, 25],
            "kwargs": {
                "width": [3.5, 0],
                "height": [2.2, 0],
                "oversize_method": "crop",
                "enable_magnets": True,
                "corner_screw_enabled": True,
                "connector_clip_enabled": True,
                "connector_position": "both",
                "remove_bottom_taper": True,
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