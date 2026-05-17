#!/usr/bin/env python3
"""Phase 3: Replace all function bodies in oobb_get_items_base.py with delegation stubs."""

import re
import sys

SOURCE_FILE = "c:\\gh\\oomlout_oobb_version_5\\oobb_get_items_base.py"

REPLACEMENTS = [
    ("get_oobb_circle", "oobb_circle", 7, 42),
    ("get_oobb_coupler_flanged", "oobb_coupler_flanged", 43, 108),
    ("get_oobb_cube", "oobb_cube", 109, 111),
    ("get_oobb_cube_center", "oobb_cube_center", 112, 132),
    ("get_oobb_cube_new", "oobb_cube_new", 133, 197),
    ("get_oobb_cylinder_hollow", "oobb_cylinder_hollow", 198, 254),
    ("get_oobb_rounded_rectangle_hollow", "oobb_rounded_rectangle_hollow", 255, 360),
    ("get_oobb_rounded_rectangle_rounded", "oobb_rounded_rectangle_rounded", 361, 601),
    ("get_oobb_sphere", "oobb_sphere", 602, 631),
    ("get_oobb_cylinder", "oobb_cylinder", 632, 694),
    ("get_oobb_electronic_battery_box_aa_battery_4_cell", "oobb_electronic_battery_box_aa_battery_4_cell", 695, 792),
    ("get_oobb_electronic_button_11_mm_panel_mount", "oobb_electronic_button_11_mm_panel_mount", 793, 833),
    ("get_oobb_electronic_potentiometer_17_mm", "oobb_electronic_potentiometer_17_mm", 834, 916),
    ("get_oobb_electronic_potentiometer_stick_single_axis_16_mm", "oobb_electronic_potentiometer_stick_single_axis_16_mm", 917, 1034),
    ("get_oobb_overhang", "oobb_overhang", 1035, 1088),
    ("get_rot", "oobb_rot", 1089, 1103),
    ("get_oobb_slice", "oobb_slice", 1104, 1143),
    ("get_oobb_hole_new", "oobb_hole_new", 1144, 1216),
    ("get_oobb_motor_servo_standard_01", "oobb_motor_servo_standard_01", 1217, 1451),
    ("get_oobb_motor_stepper_nema_17", "oobb_motor_stepper_nema_17", 1452, 1570),
    ("get_oobb_motor_tt_01", "oobb_motor_tt_01", 1571, 1730),
    ("get_oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible", 
     "oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible", 1731, 1799),
    ("get_oobb_nut", "oobb_nut", 1800, 1948),
    ("get_oobb_pl", "oobb_plate", 1949, 1951),
    ("get_oobb_plate", "oobb_plate", 1952, 2017),
    ("get_oobb_screw_countersunk", "oobb_screw_countersunk", 2018, 2021),
    ("get_oobb_screw_self_tapping", "oobb_screw_self_tapping", 2022, 2025),
    ("get_oobb_screw_socket_cap", "oobb_screw_socket_cap", 2026, 2029),
    ("get_oobb_screw", "oobb_screw", 2030, 2225),
    ("get_oobb_slot", "oobb_slot", 2226, 2304),
    ("get_oobb_tube", "oobb_tube", 2305, 2408),
    ("get_oobb_tube_new", "oobb_tube_new", 2409, 2533),
    ("get_oobb_wire_basic", "oobb_wire_basic", 2534, 2538),
    ("get_oobb_wire_higher_voltage", "oobb_wire_higher_voltage", 2539, 2543),
    ("get_oobb_wire_i2c", "oobb_wire_i2c", 2544, 2548),
    ("get_oobb_wire_motor", "oobb_wire_motor", 2549, 2553),
    ("get_oobb_wire_motor_stepper", "oobb_wire_motor_stepper", 2554, 2558),
    ("get_oobb_wire_spacer", "oobb_wire_spacer", 2559, 2563),
    ("get_oobb_wire_spacer_long", "oobb_wire_spacer_long", 2564, 2568),
    ("get_oobb_wire_spacer_u", "oobb_wire_spacer_u", 2569, 2574),
    ("get_oobb_wire_spacer_base", "oobb_wire_spacer_base", 2575, 2617),
    ("get_oobb_wire_cutout", "oobb_wire_cutout", 2618, 2782),
    ("get_oobb_zip_tie_clearance_small", "oobb_zip_tie_clearance_small", 2783, 2852),
]

def read_file(filename):
    """Read the entire file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, content):
    """Write content to file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_stub(func_name, component_name):
    """Generate a stub function."""
    return f'''def {func_name}(**kwargs):
    """Delegated to components/{component_name}/working.py."""
    from components.{component_name} import working as _m
    return _m.action(**kwargs)'''

def main():
    print("Phase 3: Creating delegation stubs in oobb_get_items_base.py")
    print("=" * 70)
    
    content = read_file(SOURCE_FILE)
    lines = content.split('\n')
    
    # Process replacements in reverse order to preserve line numbers
    replacements_sorted = sorted(REPLACEMENTS, key=lambda x: x[2], reverse=True)
    
    for func_name, component_name, start_line, end_line in replacements_sorted:
        # Convert to 0-indexed
        start_idx = start_line - 1
        end_idx = end_line
        
        # Generate stub
        stub = generate_stub(func_name, component_name)
        
        # Extract context lines
        if start_idx > 0:
            prefix_line = lines[start_idx - 1]
        else:
            prefix_line = ""
            
        # Check if this is a def line
        def_line = lines[start_idx].strip()
        if not def_line.startswith(f"def {func_name}"):
            print(f"WARNING: Line {start_line} doesn't match function {func_name}")
            print(f"  Expected: def {func_name}")
            print(f"  Got: {def_line[:60]}")
            continue
        
        # Replace lines
        new_lines = lines[:start_idx] + stub.split('\n') + [''] + lines[end_idx:]
        lines = new_lines
        
        print(f"✓ Stubbed {func_name} (lines {start_line}-{end_line})")
    
    # Write back
    write_file(SOURCE_FILE, '\n'.join(lines))
    print("\n✓ File updated successfully")

if __name__ == "__main__":
    main()
