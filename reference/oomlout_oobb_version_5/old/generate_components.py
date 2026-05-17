#!/usr/bin/env python3
"""Generate all remaining Phase 2 component working.py files."""

import os
import re

# Get the project root
project_root = os.path.dirname(os.path.abspath(__file__))

def read_source_lines(filename, start_line, end_line):
    """Read lines from file (1-indexed, inclusive)."""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Convert to 0-indexed
    body_lines = lines[start_line-1:end_line]
    
    # Indent all lines by 4 spaces for the function body
    body = ''.join(body_lines).rstrip()
    # Find first non-whitespace to determine current indentation
    first_line = body.split('\n')[0] if body else ""
    indent_match = re.match(r'^(\s*)', first_line)
    current_indent = len(indent_match.group(1)) if indent_match else 0
    
    # Re-indent to be inside action()
    lines_list = body.split('\n')
    indented_lines = []
    for line in lines_list:
        if line.strip():  # Non-empty lines
            # Remove original indentation and add 4 spaces
            if line.startswith(' ' * current_indent):
                line = line[current_indent:]
            indented_lines.append('    ' + line)
        else:
            indented_lines.append('')
    
    return '\n'.join(indented_lines)

def create_component_working_py(component_folder, function_name, source_start, source_end, 
                                 description, imports_list, cross_deps_list):
    """Create or update a working.py file for a component."""
    working_py_path = os.path.join(project_root, "components", component_folder, "working.py")
    
    # Read the function body from oobb_get_items_base.py
    source_file = os.path.join(project_root, "oobb_get_items_base.py")
    body_code = read_source_lines(source_file, source_start, source_end)
    
    # Prepare imports section
    import_lines = []
    if "math" in imports_list:
        import_lines.append("import math")
    if "copy" in imports_list or "copy" in ''.join(imports_list):
        if "import copy" not in import_lines:
            import_lines.insert(0, "import copy")
    if "oobb" in imports_list:
        import_lines.append("import oobb")
    if "opsc" in imports_list:
        import_lines.append("import opsc")
    
    import_section = '\n'.join(import_lines) if import_lines else ""
    if import_section:
        import_section += "\n"
    
    # Prepare cross-component imports
    cross_imports = ""
    if cross_deps_list:
        cross_imports += "\n# ---------- cross-component helper imports ----------\n"
        
        # Check if we need the loader function
        needs_loader = any(d in cross_deps_list for d in ["get_rot", "get_oobb_overhang", "get_oobb_cube_center", "get_oobb_wire_cutout", "get_oobb_wire_spacer_base", "get_oobb_screw"])
        
        if needs_loader:
            cross_imports += """import importlib.util
def _load_component(folder_name):
    path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
    spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

"""
        
        for dep in cross_deps_list:
            if dep == "get_rot":
                cross_imports += "_rot_mod = _load_component(\"oobb_rot\")\nget_rot = _rot_mod.action\n"
            elif dep == "get_oobb_overhang":
                cross_imports += "_overhang_mod = _load_component(\"oobb_overhang\")\nget_oobb_overhang = _overhang_mod.action\n"
            elif dep == "get_oobb_cube_center":
                cross_imports += "_cube_center_mod = _load_component(\"oobb_cube_center\")\nget_oobb_cube_center = _cube_center_mod.action\n"
            elif dep == "get_oobb_wire_cutout":
                cross_imports += "_wire_cutout_mod = _load_component(\"oobb_wire_cutout\")\nget_oobb_wire_cutout = _wire_cutout_mod.action\n"
            elif dep == "get_oobb_wire_spacer_base":
                cross_imports += "_wire_spacer_base_mod = _load_component(\"oobb_wire_spacer_base\")\nget_oobb_wire_spacer_base = _wire_spacer_base_mod.action\n"
            elif dep == "get_oobb_screw":
                cross_imports += "_screw_mod = _load_component(\"oobb_screw\")\nget_oobb_screw = _screw_mod.action\n"
            elif dep == "get_oobb_holes_old":
                cross_imports += "from oobb_get_items_base_old import get_oobb_holes\n"
    
    # Generate template
    template = f'''import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

{import_section}{cross_imports}
d = {{}}


def define():
    global d
    if not d:
        d = {{
            "name": "{component_folder}",
            "name_long": "OOBB Geometry: {component_folder}",
            "description": "{description}",
            "category": "OOBB Geometry Primitives",
            "shape_aliases": [],
        }}
    return dict(d)


def action(**kwargs):
    """Geometry component."""
{body_code}
'''
    
    # Write the file
    os.makedirs(os.path.dirname(working_py_path), exist_ok=True)
    with open(working_py_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    return True

# Task definitions
TASKS = [
    ("oobb_cube_new", "get_oobb_cube_new", 133, 197, "Cube with rotation support", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_cylinder", "get_oobb_cylinder", 632, 694, "Cylinder geometry", ["oobb", "opsc"], []),
    ("oobb_cylinder_hollow", "get_oobb_cylinder_hollow", 198, 254, "Hollow cylinder", ["copy", "opsc"], ["get_rot"]),
    ("oobb_rounded_rectangle_hollow", "get_oobb_rounded_rectangle_hollow", 255, 360, "Rounded rectangle hollow", ["copy", "opsc"], ["get_rot"]),
    ("oobb_rounded_rectangle_rounded", "get_oobb_rounded_rectangle_rounded", 361, 601, "Rounded rectangle with rounded edges", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_sphere", "get_oobb_sphere", 602, 631, "Sphere geometry", ["copy", "opsc"], []),
    ("oobb_overhang", "get_oobb_overhang", 1035, 1088, "Overhang support geometry", ["copy", "oobb", "opsc"], []),
    ("oobb_slice", "get_oobb_slice", 1104, 1143, "Slice geometry", ["copy", "oobb", "opsc"], []),
    ("oobb_hole_new", "get_oobb_hole_new", 1144, 1216, "Hole with rotation", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_nut", "get_oobb_nut", 1800, 1948, "Hexagonal nut", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_plate", "get_oobb_plate", 1952, 2017, "Plate geometry", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_screw", "get_oobb_screw", 2030, 2225, "Screw with various styles", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_screw_countersunk", "get_oobb_screw_countersunk", 2018, 2021, "Countersunk screw", [], ["get_oobb_screw"]),
    ("oobb_screw_self_tapping", "get_oobb_screw_self_tapping", 2022, 2025, "Self-tapping screw", [], ["get_oobb_screw"]),
    ("oobb_screw_socket_cap", "get_oobb_screw_socket_cap", 2026, 2029, "Socket cap screw", [], ["get_oobb_screw"]),
    ("oobb_slot", "get_oobb_slot", 2226, 2304, "Slot geometry", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_tube", "get_oobb_tube", 2305, 2408, "Tube geometry", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_tube_new", "get_oobb_tube_new", 2409, 2533, "Tube with new rendering", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_motor_servo_standard_01", "get_oobb_motor_servo_standard_01", 1217, 1451, "Servo motor", ["copy", "oobb", "opsc"], ["get_rot", "get_oobb_overhang"]),
    ("oobb_motor_stepper_nema_17", "get_oobb_motor_stepper_nema_17", 1452, 1570, "Stepper motor NEMA-17", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_motor_tt_01", "get_oobb_motor_tt_01", 1571, 1730, "TT motor", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible", "get_oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible", 1731, 1799, "Motor with encoder", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_electronic_battery_box_aa_battery_4_cell", "get_oobb_electronic_battery_box_aa_battery_4_cell", 695, 792, "Battery box 4x AA", ["copy", "oobb"], ["get_rot"]),
    ("oobb_electronic_button_11_mm_panel_mount", "get_oobb_electronic_button_11_mm_panel_mount", 793, 833, "11mm panel mount button", ["copy", "oobb"], ["get_rot"]),
    ("oobb_electronic_potentiometer_17_mm", "get_oobb_electronic_potentiometer_17_mm", 834, 916, "17mm potentiometer", ["copy", "oobb"], ["get_rot", "get_oobb_cube_center"]),
    ("oobb_electronic_potentiometer_stick_single_axis_16_mm", "get_oobb_electronic_potentiometer_stick_single_axis_16_mm", 917, 1034, "Joystick 16mm", ["copy", "oobb"], ["get_rot"]),
    ("oobb_wire_cutout", "get_oobb_wire_cutout", 2618, 2782, "Wire cutout", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_wire_spacer_base", "get_oobb_wire_spacer_base", 2575, 2617, "Wire spacer base", ["copy", "oobb", "opsc"], ["get_rot"]),
    ("oobb_wire_basic", "get_oobb_wire_basic", 2534, 2538, "Basic wire", [], ["get_oobb_wire_cutout"]),
    ("oobb_wire_higher_voltage", "get_oobb_wire_higher_voltage", 2539, 2543, "Higher voltage wire", [], ["get_oobb_wire_cutout"]),
    ("oobb_wire_i2c", "get_oobb_wire_i2c", 2544, 2548, "I2C wire", [], ["get_oobb_wire_cutout"]),
    ("oobb_wire_motor", "get_oobb_wire_motor", 2549, 2553, "Motor wire", [], ["get_oobb_wire_cutout"]),
    ("oobb_wire_motor_stepper", "get_oobb_wire_motor_stepper", 2554, 2558, "Stepper motor wire", [], ["get_oobb_wire_cutout"]),
    ("oobb_wire_spacer", "get_oobb_wire_spacer", 2559, 2563, "Wire spacer", [], ["get_oobb_wire_spacer_base"]),
    ("oobb_wire_spacer_long", "get_oobb_wire_spacer_long", 2564, 2568, "Long wire spacer", [], ["get_oobb_wire_spacer_base"]),
    ("oobb_wire_spacer_u", "get_oobb_wire_spacer_u", 2569, 2574, "U-shaped wire spacer", [], ["get_oobb_wire_spacer_base"]),
    ("oobb_zip_tie_clearance_small", "get_oobb_zip_tie_clearance_small", 2783, 2852, "Zip tie clearance hole", ["copy", "oobb", "opsc"], ["get_rot"]),
]

if __name__ == "__main__":
    completed = 0
    for task in TASKS:
        try:
            create_component_working_py(*task)
            completed += 1
            print(f"✓ Created {task[0]}/working.py")
        except Exception as e:
            print(f"✗ Failed {task[0]}: {e}")
            import traceback
            traceback.print_exc()
    print(f"\nCompleted {completed}/{len(TASKS)} components")
