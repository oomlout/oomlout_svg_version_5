import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


# Uncomment if you need cross-component helpers:
# import importlib.util
# def _load_component(folder_name):
#     path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
#     spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
#     mod = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(mod)
#     return mod
# _rot_mod = _load_component("oobb_rot")
# get_rot = _rot_mod.action

d = {}


def describe():
    global d
    d = {}
    d["name"] = '_example_shell'
    d["name_long"] = 'Category: Short human name'
    d["description"] = 'One sentence describing what this component produces.'
    d["category"] = 'OOBB Geometry Primitives'   # e.g. Fasteners / OOBB Geometry Helpers / Gridfinity
    d["shape_aliases"] = ['example_shell']        # strings callers can pass as shape=
    d["returns"] = 'List of geometry component dicts.'
    v = []
    # Add one entry per variable the action() accepts:
    v.append({"name": 'pos',    "description": '3-element [x,y,z] position.',       "type": 'list',   "default": '[0,0,0]'})
    v.append({"name": 'depth',  "description": 'Depth / height of the shape (mm).',  "type": 'number', "default": 10})
    v.append({"name": 'mode',   "description": 'Render modes: laser, 3dpr, true.',   "type": 'list',   "default": '["laser","3dpr","true"]'})
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
    """Replace this docstring with a one-liner description."""
    pos   = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    depth = kwargs.get("depth", 10)
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if isinstance(modes, str):
        modes = [modes]

    return_value = []
    for mode in modes:
        p = copy.deepcopy(kwargs)
        p["inclusion"] = mode
        p["pos"]       = pos
        # --- replace with your actual shape construction ---
        p["shape"] = "cylinder"
        p["r"]     = 5
        p["h"]     = depth
        # ---------------------------------------------------
        return_value.append(opsc.opsc_easy(**p))

    return return_value
