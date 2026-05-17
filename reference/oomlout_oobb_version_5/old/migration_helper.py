#!/usr/bin/env python3
"""Helper script to complete the geometry code migration for Phase 2."""

import os
import sys

# Component migrations with their source line ranges and dependencies
MIGRATIONS = {
    "2.05_oobb_cube_new": {"start": 133, "end": 197, "deps": ["get_rot", "opsc"]},
    "2.06_oobb_cylinder": {"start": 632, "end": 694, "deps": ["oobb", "opsc"]},
    "2.07_oobb_cylinder_hollow": {"start": 198, "end": 254, "deps": ["get_rot", "opsc"]},
    "2.08_oobb_rounded_rectangle_hollow": {"start": 255, "end": 360, "deps": ["get_rot", "opsc"]},
    "2.09_oobb_rounded_rectangle_rounded": {"start": 361, "end": 601, "deps": ["get_rot", "oobb", "opsc"]},
    "2.10_oobb_sphere": {"start": 602, "end": 631, "deps": ["copy", "opsc"]},
    "2.11_oobb_overhang": {"start": 1035, "end": 1088, "deps": ["copy", "oobb", "opsc"]},
    "2.12_oobb_slice": {"start": 1104, "end": 1143, "deps": ["copy", "oobb", "opsc"]},
    "2.13_oobb_hole_new": {"start": 1144, "end": 1216, "deps": ["get_rot", "copy", "oobb", "opsc"]},
    "2.14_oobb_nut": {"start": 1800, "end": 1948, "deps": ["get_rot", "copy", "math", "oobb", "opsc"]},
    "2.15_oobb_plate": {"start": 1952, "end": 2017, "deps": ["get_rot", "copy", "oobb", "opsc", "get_oobb_holes_old"]},
    "2.16_oobb_screw": {"start": 2030, "end": 2225, "deps": ["get_rot", "copy", "oobb", "opsc"]},
    "2.17_oobb_screw_countersunk": {"start": 2018, "end": 2021, "deps": ["get_oobb_screw"]},
    "2.18_oobb_screw_self_tapping": {"start": 2022, "end": 2025, "deps": ["get_oobb_screw"]},
    "2.19_oobb_screw_socket_cap": {"start": 2026, "end": 2029, "deps": ["get_oobb_screw"]},
    "2.20_oobb_slot": {"start": 2226, "end": 2304, "deps": ["get_rot", "copy", "oobb", "opsc"]},
    "2.21_oobb_tube": {"start": 2305, "end": 2408, "deps": ["get_rot", "copy", "oobb", "opsc"]},
    "2.22_oobb_tube_new": {"start": 2409, "end": 2533, "deps": ["get_rot", "copy", "oobb", "opsc"]},
    "2.23_oobb_motor_servo_standard_01": {"start": 1217, "end": 1451, "deps": ["get_rot", "get_oobb_overhang", "copy", "oobb", "opsc"]},
    "2.24_oobb_motor_stepper_nema_17": {"start": 1452, "end": 1570, "deps": ["get_rot", "copy", "oobb", "opsc"]},
    "2.25_oobb_motor_tt_01": {"start": 1571, "end": 1730, "deps": ["get_rot", "copy", "oobb", "opsc"]},
    "2.26_oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible": {"start": 1731, "end": 1799, "deps": ["get_rot", "copy", "oobb", "opsc"]},
    "2.27_oobb_electronic_battery_box_aa_battery_4_cell": {"start": 695, "end": 792, "deps": ["get_rot", "copy", "oobb"]},
    "2.28_oobb_electronic_button_11_mm_panel_mount": {"start": 793, "end": 833, "deps": ["get_rot", "copy", "oobb"]},
    "2.29_oobb_electronic_potentiometer_17_mm": {"start": 834, "end": 916, "deps": ["get_rot", "get_oobb_cube_center", "copy", "oobb"]},
    "2.30_oobb_electronic_potentiometer_stick_single_axis_16_mm": {"start": 917, "end": 1034, "deps": ["get_rot", "copy", "oobb"]},
    "2.31_oobb_wire_cutout": {"start": 2618, "end": 2782, "deps": ["get_rot", "copy", "oobb", "opsc"]},
    "2.32_oobb_wire_spacer_base": {"start": 2575, "end": 2617, "deps": ["get_rot", "copy", "oobb", "opsc"]},
    "2.33_oobb_wire_basic": {"start": 2534, "end": 2538, "deps": ["get_oobb_wire_cutout"]},
    "2.34_oobb_wire_higher_voltage": {"start": 2539, "end": 2543, "deps": ["get_oobb_wire_cutout"]},
    "2.35_oobb_wire_i2c": {"start": 2544, "end": 2548, "deps": ["get_oobb_wire_cutout"]},
    "2.36_oobb_wire_motor": {"start": 2549, "end": 2553, "deps": ["get_oobb_wire_cutout"]},
    "2.37_oobb_wire_motor_stepper": {"start": 2554, "end": 2558, "deps": ["get_oobb_wire_cutout"]},
    "2.38_oobb_wire_spacer": {"start": 2559, "end": 2563, "deps": ["get_oobb_wire_spacer_base"]},
    "2.39_oobb_wire_spacer_long": {"start": 2564, "end": 2568, "deps": ["get_oobb_wire_spacer_base"]},
    "2.40_oobb_wire_spacer_u": {"start": 2569, "end": 2574, "deps": ["get_oobb_wire_spacer_base"]},
    "2.41_oobb_zip_tie_clearance_small": {"start": 2783, "end": 2852, "deps": ["get_rot", "copy", "oobb", "opsc"]},
}

def extract_function_body(source_file, start_line, end_line):
    """Extract function body from source file between given lines (1-indexed)."""
    with open(source_file, 'r') as f:
        lines = f.readlines()
    # Convert to 0-indexed
    body_lines = lines[start_line:end_line+1]
    return ''.join(body_lines).rstrip()

def generate_template(component_name, function_name, deps, body_code):
    """Generate the template for a working.py file."""
    template = f'''import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# ---------- imports ----------
'''
    
    # Add standard imports
    if "copy" in deps or "copy" in body_code:
        pass  # already imported
    if "oobb" in deps or "oobb" in body_code:
        template += "import oobb\n"
    if "opsc" in deps or "opsc" in body_code:
        template += "import opsc\n"
    if "math" in deps:
        template += "import math\n"
    
    # Add cross-component imports (simplified)
    template += "\n# cross-component helper imports\n"
    if "get_rot" in deps or "get_rot" in body_code:
        template += """import importlib.util
def _load_component(folder_name):
    path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
    spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_rot_mod = _load_component("oobb_rot")
get_rot = _rot_mod.action
"""
    
    template += f'''
d = {{}}


def define():
    global d
    if not d:
        d = {{
            "name": "{component_name.replace('_', '_')}",
            "name_long": "OOBB Geometry: {component_name.replace('_', ' ').title()}",
            "description": "OOBB geometry component.",
            "category": "OOBB Geometry Primitives",
            "shape_aliases": [],
        }}
    return dict(d)


def action(**kwargs):
    """Geometry component action."""
{body_code}
'''
    
    return template

# Main
if __name__ == "__main__":
    print("Migration helper loaded. Not meant to be run directly.")
    print(f"Defined {len(MIGRATIONS)} components to migrate.")
