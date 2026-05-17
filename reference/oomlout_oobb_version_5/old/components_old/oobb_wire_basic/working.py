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

_wire_cutout_mod = _load_component("oobb_wire_cutout")
get_oobb_wire_cutout = _wire_cutout_mod.action

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_wire_basic'
    d["name_long"] = 'OOBB Wire Cutouts: Basic 3-Pin Wire'
    d["description"] = '3-pin polarized wire cutout; wraps oobb_wire_cutout with num_pins=3 and polarized=True.'
    d["category"] = 'OOBB Wire Cutouts'
    d["shape_aliases"] = ['wire_basic']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'width', "description": 'Wire connector footprint width in grid units.', "type": 'number', "default": 2})
    v.append({"name": 'height', "description": 'Wire connector footprint height in grid units.', "type": 'number', "default": 2})
    v.append({"name": 'through', "description": 'Cutout goes fully through the material.', "type": 'bool', "default": False})
    v.append({"name": 'mode', "description": 'Render modes: laser, 3dpr, true.', "type": 'list', "default": '["laser","3dpr","true"]'})
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
    """Geometry component."""
    def get_oobb_wire_basic(**kwargs):
        kwargs["num_pins"] = 3
        kwargs.update({"polarized": True})
        return get_oobb_wire_cutout(**kwargs)
