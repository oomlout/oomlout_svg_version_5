import copy
import os
import sys

from components.gridfinity_tray_raw import working as gridfinity_tray_raw_component

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_COMPONENT_ROOT = os.path.dirname(os.path.abspath(__file__))
_WRAPPER_FILE = os.path.join(_COMPONENT_ROOT, "gridfinity_tray_raw_wrapper.scad")

d = {}

MODULE_DEFAULTS = copy.deepcopy(gridfinity_tray_raw_component.MODULE_DEFAULTS)
MODULE_DEFAULTS["offset_radius"] = 0
MODULE_DEFAULTS["solid_center"] = True


def _variable(name, description, value_type, default):
    return {"name": name, "description": description, "type": value_type, "default": default}


def describe():
    global d
    base = copy.deepcopy(gridfinity_tray_raw_component.define())
    base["name"] = "gridfinity_tray_raw_offset"
    base["name_long"] = "Gridfinity: Tray Raw Offset"
    base["description"] = (
        "Returns a local wrapper around gridfinity_tray_raw from the tray_raw component directory, "
        "using the same repo-style public size inputs where gridfinity_width is X, "
        "gridfinity_height is Y, and gridfinity_depth is Z."
    )
    base["shape_aliases"] = ["gridfinity_tray_raw_offset"]
    base["notes"] = [
        "This simplified wrapper directly reuses the gridfinity_tray_raw component module.",
        "The local offset wrapper applies offset_radius in the wrapper layer around the reused tray_raw geometry.",
        "Optional solid_center adds a centered filler cube so the tray can be made solid.",
        "Use this path when you want tray_raw behavior from the offset component directory with wrapper-level adjustments.",
    ]

    variables = []
    inserted_offset = False
    for variable in base.get("variables", []):
        variables.append(copy.deepcopy(variable))
        if variable.get("name") == "gridfinity_depth":
            variables.append(
                _variable(
                    "offset_radius",
                    "Wrapper-level offset radius applied around the reused tray_raw geometry in X, Y, and Z.",
                    "number",
                    0,
                )
            )
            variables.append(
                _variable(
                    "solid_center",
                    "If true, unions a centered filler cube into the tray body.",
                    "bool",
                    True,
                )
            )
            inserted_offset = True

    if not inserted_offset:
        variables.append(
            _variable(
                "offset_radius",
                "Wrapper-level offset radius applied around the reused tray_raw geometry in X, Y, and Z.",
                "number",
                0,
            )
        )
        variables.append(
            _variable(
                "solid_center",
                "If true, unions a centered filler cube into the tray body.",
                "bool",
                True,
            )
        )

    base["variables"] = variables
    d = base
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

    inclusion = kwargs.get("inclusion", "all")
    if isinstance(inclusion, list):
        inclusion = "all" if inclusion == ["laser", "3dpr", "true"] else ",".join(str(item) for item in inclusion)

    return {
        "type": kwargs.get("type", kwargs.get("t", "positive")),
        "shape": "raw_scad",
        "file": _WRAPPER_FILE,
        "module": "gridfinity_tray_raw_offset_raw",
        "module_kwargs": module_kwargs,
        "pos": copy.deepcopy(kwargs.get("pos", [0, 0, 0])),
        "rot": copy.deepcopy(kwargs.get("rot", [0, 0, 0])),
        "inclusion": inclusion,
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
                "gridfinity_depth": 3,
                "offset_radius": 0,
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
                "offset_radius": 3,
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
