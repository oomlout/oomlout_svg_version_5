import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_COMPONENT_ROOT = os.path.dirname(os.path.abspath(__file__))
_WRAPPER_FILE = os.path.join(_COMPONENT_ROOT, "gridfinity_gridflock_raw_wrapper.scad")
_GRIDFLOCK_FILE = os.path.join(_COMPONENT_ROOT, "gridflock.scad")
_GRIDFLOCK_MODULE = "gridflock"

d = {}

MODULE_DEFAULTS = {
    "gridfinity_width": 2,
    "gridfinity_depth": 2,
    "plate_size": [84, 84],
    "bed_size": [250, 220],
    "baseplate_dimensions": [42, 42],
    "magnets": False,
    "magnet_style": 1,
    "magnet_frame_style": 1,
    "magnet_diameter": 5.9,
    "magnet_height": 2.25,
    "magnet_top": 0.5,
    "magnet_bottom": 0.75,
    "magnet_border": 2,
    "magnet_release_width": 3,
    "click": False,
    "click_style": 1,
    "click1_distance": 1,
    "click1_steepness": 1,
    "click1_outer_length": 30,
    "click1_inner_length": 0,
    "click1_height": 3,
    "click1_strength": 1.6,
    "click1_wall_strength": 1,
    "clickgroove_gap_length": 25,
    "clickgroove_tab_length": 10,
    "clickgroove_strength": 1.4,
    "clickgroove_wall_strength": 1,
    "clickgroove_depth": 0.9,
    "connector_intersection_puzzle": True,
    "intersection_puzzle_fit": 1,
    "connector_edge_puzzle": False,
    "edge_puzzle_count": 1,
    "edge_puzzle_dim": [10, 2.5],
    "edge_puzzle_dim_c": [3, 1.2],
    "edge_puzzle_gap": 0.15,
    "edge_puzzle_magnet_border": True,
    "edge_puzzle_magnet_border_width": 2.5,
    "edge_puzzle_height_female": 2.25,
    "edge_puzzle_height_male_delta": 0.25,
    "filler_x": 1,
    "filler_y": 1,
    "filler_fraction": [2, 2],
    "filler_minimum_size": [15, 15],
    "alignment": [0.5, 0.5],
    "numbering": True,
    "number_depth": 0.5,
    "number_size": 3,
    "number_font": "sans-serif",
    "number_squeeze_size": 2,
    "bottom_chamfer": [0, 0, 0, 0],
    "top_chamfer": [0, 0, 0, 0],
    "plate_wall_thickness": [0, 0, 0, 0],
    "plate_wall_height": [0, 0],
    "vertical_screw_diameter": 3.2,
    "vertical_screw_countersink_top": [0, 0],
    "vertical_screw_counterbore_top": [0, 0],
    "vertical_screw_plate_corners": False,
    "vertical_screw_plate_corner_inset": [1, 1],
    "vertical_screw_plate_edges": False,
    "vertical_screw_segment_corners": False,
    "vertical_screw_segment_corner_inset": [1, 1],
    "vertical_screw_segment_edges": False,
    "vertical_screw_other": False,
    "thumbscrews": False,
    "thumbscrew_diameter": 15.8,
    "x_segment_algorithm": 0,
    "y_row_count_first": [0, 0],
    "x_column_count_first": 0,
    "stacked_print": False,
    "stacked_print_layer_height": 0.2,
    "stacked_print_min_gap": 0.5,
    "stacked_print_duplicates": 1,
    "stacked_print_flip_first": 0,
    "stacked_print_flip": 1,
    "stacked_print_slice": 0.3,
    "solid_base": 0,
    "plate_corner_radius": 4,
    "edge_adjust": [0, 0, 0, 0],
    "cell_override": "",
    "top_slice": 0,
}


def _variable(name, description, value_type, default):
    return {"name": name, "description": description, "type": value_type, "default": default}


def describe():
    global d
    d = {}
    d["name"] = "gridfinity_gridflock_raw"
    d["name_long"] = "Gridfinity: GridFlock Raw"
    d["description"] = (
        "Returns a raw OpenSCAD wrapper around the vendored GridFlock segmented baseplate generator, "
        "using repo-style public size inputs where gridfinity_width is X and gridfinity_depth is Y."
    )
    d["category"] = "Gridfinity"
    d["shape_aliases"] = ["gridfinity_gridflock_raw"]
    d["returns"] = "Raw SCAD geometry component dict."
    d["source"] = "https://github.com/yawkat/GridFlock"
    d["notes"] = [
        "Backed by the vendored GridFlock baseplate implementation and its gridfinity-rebuilt dependency.",
        "plate_size is derived from gridfinity_width and gridfinity_depth unless explicitly provided in millimeters.",
        "The vendored SCAD now exposes a real gridflock(...) module, so parameters flow through module_kwargs instead of generated source.",
    ]

    v = []
    v.append(_variable("gridfinity_width", "Width in Gridfinity units along X.", "number", 2))
    v.append(_variable("gridfinity_depth", "Depth in Gridfinity units along Y.", "number", 2))
    v.append(_variable("plate_size", "Explicit plate size [x,y] in millimeters. Overrides derived unit sizing.", "list", "[84,84]"))
    v.append(_variable("bed_size", "Printer bed size [x,y] in millimeters.", "list", "[250,220]"))
    v.append(_variable("baseplate_dimensions", "Base Gridfinity cell dimensions [x,y] in millimeters.", "list", "[42,42]"))
    v.append(_variable("magnets", "Enable Gridfinity magnet pockets.", "bool", False))
    v.append(_variable("magnet_style", "Magnet style enum from upstream GridFlock.", "number", 1))
    v.append(_variable("magnet_frame_style", "Magnet frame style enum from upstream GridFlock.", "number", 1))
    v.append(_variable("click", "Enable click-latch features.", "bool", False))
    v.append(_variable("click_style", "Click-latch style enum from upstream GridFlock.", "number", 1))
    v.append(_variable("connector_intersection_puzzle", "Enable intersection puzzle connectors between segments.", "bool", True))
    v.append(_variable("intersection_puzzle_fit", "Intersection connector fit from 0 (loose) to 1 (tight).", "number", 1))
    v.append(_variable("connector_edge_puzzle", "Enable edge puzzle connectors between segments.", "bool", False))
    v.append(_variable("edge_puzzle_count", "Number of edge puzzle connectors per cell edge.", "number", 1))
    v.append(_variable("filler_x", "Filler mode in X: 0 none, 1 integer fraction, 2 dynamic.", "number", 1))
    v.append(_variable("filler_y", "Filler mode in Y: 0 none, 1 integer fraction, 2 dynamic.", "number", 1))
    v.append(_variable("filler_fraction", "Integer filler fractions [x,y].", "list", "[2,2]"))
    v.append(_variable("alignment", "Padding alignment [x,y] from 0 to 1.", "list", "[0.5,0.5]"))
    v.append(_variable("numbering", "Emboss segment numbers on the underside.", "bool", True))
    v.append(_variable("bottom_chamfer", "Bottom chamfer [north,east,south,west] in millimeters.", "list", "[0,0,0,0]"))
    v.append(_variable("top_chamfer", "Top chamfer [north,east,south,west] in millimeters.", "list", "[0,0,0,0]"))
    v.append(_variable("plate_wall_thickness", "Plate wall thickness [north,east,south,west] in millimeters.", "list", "[0,0,0,0]"))
    v.append(_variable("plate_wall_height", "Plate wall heights [above,below] in millimeters.", "list", "[0,0]"))
    v.append(_variable("vertical_screw_plate_corners", "Enable vertical screw holes at plate corners.", "bool", False))
    v.append(_variable("vertical_screw_segment_corners", "Enable vertical screw holes at segment corners.", "bool", False))
    v.append(_variable("vertical_screw_other", "Enable vertical screw holes at other intersections.", "bool", False))
    v.append(_variable("thumbscrews", "Enable Gridfinity Refined thumbscrew cutouts.", "bool", False))
    v.append(_variable("x_segment_algorithm", "Segmentation algorithm in X: 0 ideal, 1 incremental.", "number", 0))
    v.append(_variable("y_row_count_first", "Override first Y segment row counts [odd,even].", "list", "[0,0]"))
    v.append(_variable("x_column_count_first", "Override first X segment column count for incremental mode.", "number", 0))
    v.append(_variable("stacked_print", "Enable stacked-print segment output.", "bool", False))
    v.append(_variable("stacked_print_duplicates", "Duplicate each segment this many times in stacked-print mode.", "number", 1))
    v.append(_variable("solid_base", "Solid base thickness in millimeters.", "number", 0))
    v.append(_variable("plate_corner_radius", "Corner radius of the generated plate in millimeters.", "number", 4))
    v.append(_variable("edge_adjust", "Padding adjustment [north,east,south,west] in millimeters.", "list", "[0,0,0,0]"))
    v.append(_variable("cell_override", "Per-cell override string using c, s, and e codes.", "string", '""'))
    v.append(_variable("top_slice", "Cut this much from the top of the baseplate in millimeters.", "number", 0))
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
        "gridfinity_depth": copy.deepcopy(
            kwargs.get("gridfinity_depth", kwargs.get("depth", MODULE_DEFAULTS["gridfinity_depth"]))
        ),
    }


def _resolve_plate_size(kwargs, size_inputs, baseplate_dimensions):
    explicit_plate_size = kwargs.get("plate_size")
    if explicit_plate_size is not None:
        return copy.deepcopy(explicit_plate_size)
    return [
        size_inputs["gridfinity_width"] * baseplate_dimensions[0],
        size_inputs["gridfinity_depth"] * baseplate_dimensions[1],
    ]


def action(**kwargs):
    module_kwargs = {
        key: copy.deepcopy(kwargs.get(key, default_value))
        for key, default_value in MODULE_DEFAULTS.items()
    }

    size_inputs = _resolve_gridfinity_size_inputs(kwargs)
    module_kwargs.update(size_inputs)

    baseplate_dimensions = copy.deepcopy(kwargs.get("baseplate_dimensions", MODULE_DEFAULTS["baseplate_dimensions"]))
    module_kwargs["baseplate_dimensions"] = baseplate_dimensions
    module_kwargs["plate_size"] = _resolve_plate_size(kwargs, size_inputs, baseplate_dimensions)

    return {
        "type": kwargs.get("type", kwargs.get("t", "positive")),
        "shape": "raw_scad",
        "file": _GRIDFLOCK_FILE,
        "module": _GRIDFLOCK_MODULE,
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
                "gridfinity_depth": 2,
                "pos": [0, 0, 0],
                "rot": [0, 0, 0],
                "type": "positive",
            },
        },
        {
            "filename": "test_2",
            "preview_rot": [55, 0, 25],
            "kwargs": {
                "width": 3,
                "depth": 2,
                "bed_size": [100, 100],
                "magnets": True,
                "connector_intersection_puzzle": False,
                "connector_edge_puzzle": True,
                "plate_wall_thickness": [1, 1, 1, 1],
                "plate_wall_height": [4, 0],
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