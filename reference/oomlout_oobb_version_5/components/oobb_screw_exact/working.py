import copy
import os
import re
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

d = {}


def describe():
    global d
    d = {}
    d["name"] = "oobb_screw_exact"
    d["name_long"] = "OOBB Part: Exact Screw"
    d["description"] = (
        "Part builder that accepts the preferred OOBB screw naming format and maps it "
        "to the GitHub BelfrySCAD BOSL2 screw wrapper."
    )
    d["category"] = "Fasteners"
    d["shape_aliases"] = []
    d["returns"] = "Thing dict with computed GitHub/BOSL2 screw fields and generated components."
    v = []
    v.append({"name": "thread_size", "description": 'Preferred OOBB thread token, for example `"m2_diameter"` or `"m3_diameter"`.', "type": "string", "default": '"m3_diameter"'})
    v.append({"name": "length", "description": 'Preferred OOBB length token, for example `"10_mm_length"`.', "type": "string", "default": '"10_mm_length"'})
    v.append({"name": "drive_style", "description": 'Preferred OOBB drive token, for example `"hex_head"`, `"phillips_head"`, `"torx_head"`, `"slot_head"`.', "type": "string", "default": '"hex_head"'})
    v.append({"name": "screw_style", "description": 'Preferred OOBB screw head token, for example `"countersunk"`, `"socket_cap"`, `"button"`, `"pan"`.', "type": "string", "default": '"countersunk"'})
    v.append({"name": "screw_color", "description": 'Display color for the screw. `"black"` is softened to a dark grey to preserve visible detail.', "type": "string", "default": '"silver"'})
    v.append({"name": "screw_colour", "description": "British spelling alias for `screw_color`.", "type": "string", "default": '""'})
    v.append({"name": "modes", "description": 'Preferred OOBB render modes list, for example `["3dpr"]`.', "type": "list", "default": '["3dpr"]'})
    v.append({"name": "mode", "description": 'Optional direct mode override passed through to the GitHub screw wrapper.', "type": "list", "default": '["3dpr"]'})
    v.append({"name": "pos", "description": "3-element [x,y,z] position.", "type": "list", "default": "[0,0,0]"})
    v.append({"name": "rot", "description": "Rotation [rx,ry,rz] in degrees.", "type": "list", "default": "[0,0,0]"})
    v.append({"name": "oobb_name", "description": 'Logical OOBB name for the part. Defaults to `"screw"`.', "type": "string", "default": '"screw"'})
    v.append({"name": "oomp_mode", "description": 'Metadata mode, usually `"project"`.', "type": "string", "default": '"project"'})
    v.append({"name": "oomp_description_main", "description": 'Optional OOMP main description.', "type": "string", "default": '"screw_"'})
    v.append({"name": "oomp_description_extra", "description": "Optional OOMP extra description.", "type": "string", "default": '""'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable


def _normalize_type_name(raw_type):
    if not isinstance(raw_type, str) or raw_type == "":
        return "oobb_screw_exact"
    if "\\" in raw_type or "/" in raw_type or ":" in raw_type:
        return "oobb_screw_exact"
    return raw_type


def _thread_size_to_spec_base(thread_size):
    if not isinstance(thread_size, str) or thread_size == "":
        return "M3"

    match = re.match(r"^m(?P<size>[\d_]+)_diameter$", thread_size.lower())
    if match:
        return f"M{match.group('size').replace('_', '.')}"

    match = re.match(r"^#?(?P<size>\d+)_diameter$", thread_size.lower())
    if match:
        return f"#{match.group('size')}"

    cleaned = thread_size.replace("_diameter", "").replace("_", "").upper()
    if cleaned.startswith("M") or cleaned.startswith("#"):
        return cleaned
    return cleaned or "M3"


def _length_token_to_mm(length_value):
    if isinstance(length_value, (int, float)):
        return float(length_value)
    if not isinstance(length_value, str) or length_value == "":
        return 10.0

    match = re.match(r"^(?P<value>[\d_]+)_mm_length$", length_value.lower())
    if match:
        return float(match.group("value").replace("_", "."))

    match = re.match(r"^(?P<value>[\d.]+)$", length_value)
    if match:
        return float(match.group("value"))

    return 10.0


def _map_drive_style(drive_style):
    if not isinstance(drive_style, str) or drive_style == "":
        return "none"

    lookup = {
        "none": "none",
        "none_head": "none",
        "hex": "hex",
        "hex_head": "hex",
        "socket_hex": "hex",
        "allen_head": "hex",
        "slot": "slot",
        "slot_head": "slot",
        "slotted_head": "slot",
        "phillips": "phillips",
        "phillips_head": "phillips",
        "ph0_head": "ph0",
        "ph1_head": "ph1",
        "ph2_head": "ph2",
        "ph3_head": "ph3",
        "ph4_head": "ph4",
        "torx": "torx",
        "torx_head": "torx",
        "t10_head": "t10",
        "t15_head": "t15",
        "t20_head": "t20",
        "t25_head": "t25",
    }
    return lookup.get(drive_style.lower(), drive_style.lower().replace("_head", ""))


def _map_screw_style(screw_style):
    if not isinstance(screw_style, str) or screw_style == "":
        return "socket"

    lookup = {
        "none": "none",
        "grub": "none",
        "set_screw": "none",
        "hex": "hex",
        "hex_head": "hex",
        "socket": "socket",
        "socket_cap": "socket",
        "socket_cap_head": "socket",
        "socket_ribbed": "socket ribbed",
        "button": "button",
        "button_head": "button",
        "countersunk": "flat",
        "flat": "flat",
        "flat_head": "flat",
        "flat_sharp": "flat sharp",
        "flat_small": "flat small",
        "flat_large": "flat large",
        "flat_undercut": "flat undercut",
        "flat_82": "flat 82",
        "flat_100": "flat 100",
        "pan": "pan",
        "pan_head": "pan",
        "pan_flat": "pan flat",
        "round": "round",
        "fillister": "fillister",
        "cheese": "cheese",
    }
    return lookup.get(screw_style.lower(), screw_style.lower().replace("_", " "))


def _map_screw_color(params):
    color = params.get("screw_color", params.get("screw_colour", "silver"))
    if not isinstance(color, str) or color == "":
        return "silver"

    normalized = color.strip().lower()
    if normalized == "black":
        return "#444444"
    return color


def action(**kwargs):
    import oobb
    """Build a screw part using preferred OOBB naming and GitHub BOSL2 mapping."""

    params = copy.deepcopy(kwargs)
    params["type"] = _normalize_type_name(params.get("type", "oobb_screw_exact"))
    params.setdefault("oobb_name", "screw")

    thread_size = params.get("thread_size", "m3_diameter")
    length_token = params.get("length", "10_mm_length")
    drive_style = params.get("drive_style", "hex_head")
    screw_style = params.get("screw_style", "countersunk")
    screw_color = _map_screw_color(params)
    pos = copy.deepcopy(params.get("pos", [0, 0, 0]))
    modes = params.get("mode", params.get("modes", ["3dpr"]))

    spec_base = _thread_size_to_spec_base(thread_size)
    length_mm = _length_token_to_mm(length_token)
    github_drive = _map_drive_style(drive_style)
    github_head = _map_screw_style(screw_style)
    github_spec = f"{spec_base},{int(length_mm) if float(length_mm).is_integer() else length_mm}"

    thing = oobb.get_default_thing(**params)
    thing.update(
        {
            "description": f"exact screw {thread_size} {length_token} {screw_style} {drive_style}",
            "depth_mm": length_mm,
            "thread_size": thread_size,
            "length": length_token,
            "drive_style": drive_style,
            "screw_style": screw_style,
            "screw_color": screw_color,
            "github_shape": "github_belfryscad_bosl2_screw",
            "github_repo": "https://github.com/BelfrySCAD/BOSL2",
            "github_source_file": "https://github.com/BelfrySCAD/BOSL2/wiki/screws.scad",
            "github_spec": github_spec,
            "github_head": github_head,
            "github_drive": github_drive,
            "github_length_mm": length_mm,
        }
    )

    p3 = copy.deepcopy(params)
    p3["type"] = "positive"
    p3["shape"] = "github_belfryscad_bosl2_screw"
    p3["spec"] = github_spec
    p3["length"] = length_mm
    p3["drive"] = github_drive
    p3["head"] = github_head
    p3["mode"] = modes
    p3["pos"] = pos
    p3["color"] = screw_color

    for key in [
        "modes",
        "oobb_name",
        "oomp_mode",
        "oomp_run",
        "oomp_description_main",
        "oomp_description_extra",
        "thread_size",
        "drive_style",
        "screw_style",
        "screw_color",
        "screw_colour",
    ]:
        p3.pop(key, None)

    oobb.append_full(thing, **p3)
    return thing


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [
        {
            "filename": "test_1",
            "preview_rot": [70, 0, 20],
            "kwargs": {
                "thread_size": "m2_diameter",
                "length": "10_mm_length",
                "drive_style": "hex_head",
                "screw_style": "countersunk",
                "screw_color": "black",
                "modes": ["3dpr"],
            },
        },
        {
            "filename": "test_2",
            "preview_rot": [70, 0, 20],
            "kwargs": {
                "thread_size": "m3_diameter",
                "length": "16_mm_length",
                "drive_style": "torx_head",
                "screw_style": "button",
                "screw_color": "silver",
                "modes": ["true"],
            },
        },
    ]

    generated_files = []

    for sample in samples:
        result = action(**copy.deepcopy(sample["kwargs"]))
        components = copy.deepcopy(result["components"])

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
