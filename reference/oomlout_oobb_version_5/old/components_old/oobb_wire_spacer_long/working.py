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

_wire_spacer_base_mod = _load_component("oobb_wire_spacer_base")
get_oobb_wire_spacer_base = _wire_spacer_base_mod.action

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_wire_spacer_long'
    d["name_long"] = 'OOBB Wire Cutouts: Wire Spacer Long'
    d["description"] = 'Longer wire spacer plate (length=29 mm).'
    d["category"] = 'OOBB Wire Cutouts'
    d["shape_aliases"] = ['wire_spacer_long']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'thickness', "description": 'Plate thickness used to offset z position.', "type": 'number', "default": 1})
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
    def get_oobb_wire_spacer_long(**kwargs):
        kwargs["length_spacer"] = 29
        kwargs["pos_spacer"] = [-4.5,0,0]
        return get_oobb_wire_spacer_base(**kwargs)
