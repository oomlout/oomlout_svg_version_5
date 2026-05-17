"""Generate thin geometry-wrapper working.py files in components/oobb_*/."""
import os

COMPONENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "components")

# (folder_name, legacy_function, description, extra_shape_aliases)
WRAPPERS = [
    ("oobb_circle",          "get_oobb_circle",          "Circle geometry primitive (cylinder cutout/solid).", []),
    ("oobb_coupler_flanged", "get_oobb_coupler_flanged",  "Flanged coupler geometry.", []),
    ("oobb_cube",            "get_oobb_cube",             "Cube geometry primitive.", []),
    ("oobb_cube_center",     "get_oobb_cube_center",      "Center-aligned cube geometry primitive.", []),
    ("oobb_cube_new",        "get_oobb_cube_new",         "New cube geometry variant.", []),
    ("oobb_cylinder",        "get_oobb_cylinder",         "Cylinder geometry primitive.", []),
    ("oobb_cylinder_hollow", "get_oobb_cylinder_hollow",  "Hollow cylinder geometry primitive.", []),
    ("oobb_rounded_rectangle_hollow",  "get_oobb_rounded_rectangle_hollow",  "Hollow rounded rectangle geometry.", []),
    ("oobb_rounded_rectangle_rounded", "get_oobb_rounded_rectangle_rounded", "Fully rounded rectangle geometry.", []),
    ("oobb_sphere",          "get_oobb_sphere",           "Sphere geometry primitive.", []),
    ("oobb_overhang",        "get_oobb_overhang",         "Overhang geometry helper.", []),
    ("oobb_slice",           "get_oobb_slice",            "Slice geometry helper.", []),
    ("oobb_hole_new",        "get_oobb_hole_new",         "OOBB hole geometry (new variant).", []),
    ("oobb_nut",             "get_oobb_nut",              "Nut geometry (captive nut pocket / nut solid).", []),
    ("oobb_plate",           "get_oobb_plate",            "OOBB plate geometry primitive.", ["oobb_pl"]),
    ("oobb_screw",           "get_oobb_screw",            "Generic screw geometry.", []),
    ("oobb_screw_countersunk",  "get_oobb_screw_countersunk",  "Countersunk screw geometry.", []),
    ("oobb_screw_self_tapping", "get_oobb_screw_self_tapping", "Self-tapping screw geometry.", []),
    ("oobb_screw_socket_cap",   "get_oobb_screw_socket_cap",   "Socket cap screw geometry.", []),
    ("oobb_slot",            "get_oobb_slot",             "Slot geometry primitive.", []),
    ("oobb_tube",            "get_oobb_tube",             "Tube geometry primitive.", []),
    ("oobb_tube_new",        "get_oobb_tube_new",         "Tube geometry (new variant).", []),
    ("oobb_motor_servo_standard_01",    "get_oobb_motor_servo_standard_01",    "Servo motor geometry reference model.", []),
    ("oobb_motor_stepper_nema_17",      "get_oobb_motor_stepper_nema_17",      "NEMA 17 stepper motor geometry reference model.", []),
    ("oobb_motor_tt_01",                "get_oobb_motor_tt_01",                "TT motor geometry reference model.", []),
    (
        "oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible",
        "get_oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible",
        "Cricut-compatible 30 mm motor with encoder geometry.", [],
    ),
    ("oobb_electronic_battery_box_aa_battery_4_cell",          "get_oobb_electronic_battery_box_aa_battery_4_cell",          "AA battery box (4-cell) geometry.", []),
    ("oobb_electronic_button_11_mm_panel_mount",               "get_oobb_electronic_button_11_mm_panel_mount",               "11 mm panel-mount button geometry.", []),
    ("oobb_electronic_potentiometer_17_mm",                    "get_oobb_electronic_potentiometer_17_mm",                    "17 mm potentiometer geometry.", []),
    ("oobb_electronic_potentiometer_stick_single_axis_16_mm",  "get_oobb_electronic_potentiometer_stick_single_axis_16_mm",  "16 mm single-axis stick potentiometer geometry.", []),
    ("oobb_wire_basic",          "get_oobb_wire_basic",          "Wire basic cutout geometry.", []),
    ("oobb_wire_higher_voltage", "get_oobb_wire_higher_voltage", "Higher-voltage wire cutout geometry.", []),
    ("oobb_wire_i2c",            "get_oobb_wire_i2c",            "I2C wire cutout geometry.", []),
    ("oobb_wire_motor",          "get_oobb_wire_motor",          "Motor wire cutout geometry.", []),
    ("oobb_wire_motor_stepper",  "get_oobb_wire_motor_stepper",  "Stepper motor wire cutout geometry.", []),
    ("oobb_wire_spacer",         "get_oobb_wire_spacer",         "Wire spacer geometry.", []),
    ("oobb_wire_spacer_long",    "get_oobb_wire_spacer_long",    "Long wire spacer geometry.", []),
    ("oobb_wire_spacer_u",       "get_oobb_wire_spacer_u",       "U-shaped wire spacer geometry.", []),
    ("oobb_wire_spacer_base",    "get_oobb_wire_spacer_base",    "Wire spacer base geometry.", []),
    ("oobb_wire_cutout",         "get_oobb_wire_cutout",         "Generic wire cutout geometry.", []),
    ("oobb_zip_tie_clearance_small", "get_oobb_zip_tie_clearance_small", "Small zip-tie clearance geometry.", []),
]

TEMPLATE = """\
d = {{}}


def define():
    global d
    if not d:
        d = {{
            "name": "{name}",
            "name_long": "OOBB Geometry: {name_title}",
            "description": "{description}",
            "category": "OOBB Geometry Primitives",
            "shape_aliases": {aliases},
        }}
    return dict(d)


def action(**kwargs):
    \"\"\"Geometry wrapper -- delegates to oobb_get_items_base.{func_name}.\"\"\"
    import oobb_get_items_base
    return oobb_get_items_base.{func_name}(**kwargs)
"""


def main():
    created = 0
    skipped = 0
    for folder, func, desc, aliases in WRAPPERS:
        folder_path = os.path.join(COMPONENTS_DIR, folder)
        working_path = os.path.join(folder_path, "working.py")
        if os.path.exists(working_path):
            skipped += 1
            continue
        os.makedirs(folder_path, exist_ok=True)
        name_title = folder.replace("_", " ").title()
        content = TEMPLATE.format(
            name=folder,
            name_title=name_title,
            description=desc,
            aliases=repr(aliases),
            func_name=func,
        )
        with open(working_path, "w") as f:
            f.write(content)
        created += 1
        print(f"  created {folder}/working.py")

    print(f"\nDone: created={created}, skipped={skipped}")


if __name__ == "__main__":
    main()
