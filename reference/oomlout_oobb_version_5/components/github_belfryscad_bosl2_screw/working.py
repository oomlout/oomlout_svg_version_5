import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_COMPONENT_ROOT = os.path.dirname(os.path.abspath(__file__))

d = {}

_HEAD_TYPES = [
    "none",
    "hex",
    "socket",
    "socket ribbed",
    "button",
    "flat",
    "flat sharp",
    "flat small",
    "flat large",
    "flat undercut",
    "flat 82",
    "flat 100",
    "round",
    "fillister",
    "pan",
    "pan flat",
    "cheese",
]

_DRIVE_TYPES = [
    "none",
    "hex",
    "slot",
    "phillips",
    "ph0",
    "ph1",
    "ph2",
    "ph3",
    "ph4",
    "torx",
    "t10",
    "t15",
    "t20",
    "t25",
]


def describe():
    global d
    d = {}
    d["name"] = "github_belfryscad_bosl2_screw"
    d["name_long"] = "GitHub BelfrySCAD BOSL2: Screw"
    d["description"] = (
        "Raw OpenSCAD wrapper around BOSL2 `screw()` from `screws.scad`, using the local "
        "`git/BOSL2` clone and the repo raw_scad insertion path."
    )
    d["category"] = "External Library Wrappers"
    d["shape_aliases"] = ["github_belfryscad_bosl2_screw", "belfryscad_bosl2_screw", "bosl2_screw"]
    d["returns"] = "Raw SCAD geometry component dict."
    d["source"] = "https://github.com/BelfrySCAD/BOSL2"
    d["source_file"] = "https://github.com/BelfrySCAD/BOSL2/wiki/screws.scad"
    d["notes"] = [
        "Uses a generated raw_scad wrapper module instead of placeholder cylinders.",
        "Requires the BOSL2 repo to be available at git/BOSL2.",
        "Head styles documented from BOSL2: " + ", ".join(_HEAD_TYPES),
        "Drive styles documented from BOSL2: " + ", ".join(_DRIVE_TYPES),
    ]
    v = []
    v.append({"name": "pos", "description": "3-element [x,y,z] position.", "type": "list", "default": "[0,0,0]"})
    v.append({"name": "rot", "description": "Rotation [rx,ry,rz] in degrees.", "type": "list", "default": "[0,0,0]"})
    v.append({"name": "type", "description": "Geometry type: positive or negative.", "type": "string", "default": '"positive"'})
    v.append({"name": "color", "description": "Display color passed through to the rendered screw object.", "type": "string", "default": '""'})
    v.append({"name": "spec", "description": 'BOSL2 screw specification string, for example `"M3,12"` or `"#8-32,3/4"`.', "type": "string", "default": '"M3,12"'})
    v.append({"name": "head", "description": "BOSL2 head type.", "type": "string", "default": '"socket"'})
    v.append({"name": "drive", "description": "BOSL2 drive type.", "type": "string", "default": '"none"'})
    v.append({"name": "length", "description": "Overall screw length in mm.", "type": "number", "default": 12})
    v.append({"name": "l", "description": "Alias for `length`.", "type": "number", "default": 12})
    v.append({"name": "thread", "description": 'Thread type or specification. BOSL2 default is `"coarse"`.', "type": "string", "default": '"coarse"'})
    v.append({"name": "drive_size", "description": "Optional BOSL2 drive recess size override.", "type": "number", "default": '""'})
    v.append({"name": "thread_len", "description": "Threaded portion length in mm.", "type": "number", "default": '""'})
    v.append({"name": "undersize", "description": "BOSL2 screw undersize override.", "type": "number", "default": 0})
    v.append({"name": "shaft_undersize", "description": "BOSL2 shaft undersize override.", "type": "number", "default": 0})
    v.append({"name": "head_undersize", "description": "BOSL2 head undersize override.", "type": "number", "default": 0})
    v.append({"name": "tolerance", "description": 'BOSL2 screw tolerance, e.g. `"6g"` or `"2A"`.', "type": "string", "default": '""'})
    v.append({"name": "blunt_start", "description": "If true and threaded, create blunt-start threads in BOSL2.", "type": "bool", "default": True})
    v.append({"name": "details", "description": "If true, request BOSL2 detailed geometry.", "type": "bool", "default": False})
    v.append({"name": "atype", "description": 'BOSL2 anchor type, one of `"screw"`, `"head"`, `"shaft"`, `"threads"`, `"shank"`.', "type": "string", "default": '"screw"'})
    v.append({"name": "anchor", "description": 'BOSL2 anchor, for example `"center"`, `"top"`, `"bottom"`.', "type": "string", "default": '"center"'})
    v.append({"name": "mode", "description": 'Render modes: `"laser"`, `"3dpr"`, `"true"`.', "type": "list", "default": '["laser","3dpr","true"]'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable


def _bosl2_root():
    return os.path.join(_COMPONENT_ROOT, "git", "BOSL2")


def _build_wrapper_source():
    return '''include <git/BOSL2/std.scad>
include <git/BOSL2/screws.scad>

module github_belfryscad_bosl2_screw_raw(
    spec="M3,12",
    head="socket",
    drive="none",
    length=12,
    thread="coarse",
    drive_size=undef,
    thread_len=undef,
    undersize=undef,
    shaft_undersize=undef,
    head_undersize=undef,
    tolerance=undef,
    blunt_start=true,
    details=false,
    atype="screw",
    anchor="center"
) {{
    let(
        $tags_shown="ALL",
        $tags_hidden=[],
        $tag="",
        $tags=""
    )
    screw(
        spec=spec,
        head=head,
        drive=drive,
        thread=thread,
        drive_size=drive_size,
        length=length,
        thread_len=thread_len,
        undersize=undersize,
        shaft_undersize=shaft_undersize,
        head_undersize=head_undersize,
        tolerance=tolerance,
        blunt_start=blunt_start,
        details=details,
        atype=atype,
        anchor=anchor
    );
}}
'''


def action(**kwargs):
    bosl2_root = _bosl2_root()
    if not os.path.isdir(bosl2_root):
        raise FileNotFoundError(
            f"BOSL2 repo not found at {bosl2_root}. Clone https://github.com/BelfrySCAD/BOSL2 there first."
        )

    params = copy.deepcopy(kwargs)
    spec = params.get("spec", "M3,12")
    length = params.get("length", params.get("l", 12))
    pos = copy.deepcopy(params.get("pos", [0, 0, 0]))
    rot = copy.deepcopy(params.get("rot", [0, 0, 0]))
    inclusion = params.get("inclusion", params.get("mode", "all"))
    if isinstance(inclusion, list):
        inclusion = "all" if inclusion == ["laser", "3dpr", "true"] else ",".join(str(item) for item in inclusion)

    module_kwargs = {
        "spec": spec,
        "head": params.get("head", "socket"),
        "drive": params.get("drive", "none"),
        "length": length,
        "thread": params.get("thread", "coarse"),
        "blunt_start": params.get("blunt_start", True),
        "details": params.get("details", False),
        "atype": params.get("atype", "screw"),
        "anchor": params.get("anchor", "center"),
    }

    for key in ["drive_size", "thread_len", "tolerance", "undersize", "shaft_undersize", "head_undersize"]:
        value = params.get(key, "")
        if value not in ("", None):
            module_kwargs[key] = value

    return {
        "type": params.get("type", "positive"),
        "shape": "raw_scad",
        "source": _build_wrapper_source(),
        "module": "github_belfryscad_bosl2_screw_raw",
        "module_kwargs": module_kwargs,
        "pos": pos,
        "rot": rot,
        "color": params.get("color", ""),
        "inclusion": inclusion,
        "m": params.get("m", ""),
    }


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
            "preview_rot": [65, 0, 25],
            "kwargs": {
                "pos": [0, 0, 0],
                "type": "positive",
                "spec": "M3,12",
                "head": "socket",
                "drive": "hex",
                "mode": "true",
            },
        },
        {
            "filename": "test_2",
            "preview_rot": [65, 0, 25],
            "kwargs": {
                "pos": [0, 0, 0],
                "type": "positive",
                "spec": "M4,16",
                "head": "flat",
                "drive": "phillips",
                "mode": "true",
            },
        },
    ]

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
