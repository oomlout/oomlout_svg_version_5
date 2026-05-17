"""Phase 1: Rename part_calls -> components, flatten objects/sets, merge overlapping.

Run from repo root:
    python scripts/phase1_migrate_folders.py

This script uses shutil (not git mv) for simplicity. Run 'git add -A' after.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PART_CALLS = ROOT / "part_calls"
COMPONENTS = ROOT / "components"

# ── Step 1: Rename part_calls -> components ─────────────────────────────
print("Step 1: Renaming part_calls -> components")
if COMPONENTS.exists():
    print(f"  WARNING: {COMPONENTS} already exists, skipping rename")
else:
    PART_CALLS.rename(COMPONENTS)
    print("  Done")

# ── Step 2: Flatten objects/ (strip oobb_object_ prefix) ───────────────
OBJECTS_DIR = COMPONENTS / "objects"
print(f"\nStep 2: Flattening {OBJECTS_DIR}")
if OBJECTS_DIR.exists():
    for folder in sorted(OBJECTS_DIR.iterdir()):
        if not folder.is_dir():
            continue
        old_name = folder.name
        # Strip "oobb_object_" prefix
        if old_name.startswith("oobb_object_"):
            new_name = old_name[len("oobb_object_"):]
        else:
            new_name = old_name
        dest = COMPONENTS / new_name
        if dest.exists():
            print(f"  SKIP (already exists): {old_name} -> {new_name}")
            continue
        folder.rename(dest)
        print(f"  {old_name} -> {new_name}")
    # Remove objects/ dir if empty
    remaining = list(OBJECTS_DIR.iterdir())
    if not remaining:
        OBJECTS_DIR.rmdir()
        print("  Removed empty objects/ directory")
    else:
        print(f"  WARNING: objects/ not empty, {len(remaining)} items remain")
else:
    print("  objects/ does not exist, skipping")

# ── Step 3: Flatten sets/ ───────────────────────────────────────────────
SETS_DIR = COMPONENTS / "sets"
print(f"\nStep 3: Flattening {SETS_DIR}")
if SETS_DIR.exists():
    for folder in sorted(SETS_DIR.iterdir()):
        if not folder.is_dir():
            continue
        dest = COMPONENTS / folder.name
        if dest.exists():
            # This is expected for overlapping set+object folders
            print(f"  MERGE NEEDED: sets/{folder.name} -> {folder.name} (dest exists)")
            continue
        folder.rename(dest)
        print(f"  sets/{folder.name} -> {folder.name}")
    remaining = list(SETS_DIR.iterdir())
    if not remaining:
        SETS_DIR.rmdir()
        print("  Removed empty sets/ directory")
    else:
        print(f"  WARNING: sets/ not empty, {len(remaining)} items remain")
else:
    print("  sets/ does not exist, skipping")

# ── Step 4: Merge overlapping set + object folders ──────────────────────
# These are cases where a set (plural) and object (singular) both exist.
# We keep the SET (plural) name and merge the object's action() into it.
MERGE_MAP = {
    # "singular_object_name": "plural_set_name"
    "bearing": "bearings",
    "bearing_circle": "bearing_circles",
    "bearing_plate": "bearing_plates",
    "circle": "circles",
    "gear": "gears",
    "holder": "holders",
    "jack": "jacks",
    "jig": "jigs",
    "mounting_plate": "mounting_plates",
    "nut": "nuts",
    "other": "others",
    "plate": "plates",
    "pulley_gt2": "pulleys",
    "shaft": "shafts",
    "shaft_coupler": "shaft_couplers",
    "smd_magazine": "smd_magazines",
    "soldering_jig": "soldering_jigs",
    "test": "tests",
    "tool_holder": "tool_holders",
    "tray": "trays",
    "wheel": "wheels",
    "wire": "wires",
    "ziptie_holder": "ziptie_holders",
    "bunting_alphabet": "buntings",
}

print("\nStep 4: Merging overlapping folders")

# First move the remaining sets that couldn't be moved because dest existed
# (they're still in sets/ dir if it wasn't deleted)
if SETS_DIR.exists():
    for folder in sorted(SETS_DIR.iterdir()):
        if not folder.is_dir():
            continue
        set_name = folder.name
        obj_folder = COMPONENTS / set_name
        if obj_folder.exists():
            # Object already took this name; we need to merge
            # Read both working.py files
            set_working = folder / "working.py"
            obj_working = obj_folder / "working.py"
            if set_working.exists() and obj_working.exists():
                set_code = set_working.read_text(encoding="utf-8")
                obj_code = obj_working.read_text(encoding="utf-8")
                # Merge: keep set's working.py, append object's action() and test()
                merged = set_code.rstrip() + "\n\n\n# === MERGED FROM OBJECT ===\n"
                merged += "# Original object action() and test() below:\n"
                merged += "# " + "=" * 60 + "\n"
                # Extract action and test functions from object
                for line in obj_code.split("\n"):
                    merged += "# OBJECT: " + line + "\n"
                merged += "\n# TODO: Integrate object action() into this file\n"
                # For now, just append the object's action as a second function
                # with a suffix so it doesn't conflict
                if "def action(" in obj_code:
                    merged += "\n" + obj_code[obj_code.index("def action("):]
                obj_working.write_text(merged, encoding="utf-8")
                print(f"  MERGED: sets/{set_name}/working.py into {set_name}/working.py")
            # Copy any other files from set that don't exist in obj
            for f in folder.iterdir():
                dest_f = obj_folder / f.name
                if not dest_f.exists():
                    if f.is_dir():
                        shutil.copytree(f, dest_f)
                    else:
                        shutil.copy2(f, dest_f)
            # Remove the set folder
            shutil.rmtree(folder)
            print(f"  Removed sets/{set_name}/ after merge")

    # Clean up sets dir
    remaining = list(SETS_DIR.iterdir()) if SETS_DIR.exists() else []
    if SETS_DIR.exists() and not remaining:
        SETS_DIR.rmdir()

# Now handle merges for object folders that need renaming to plural
for obj_name, set_name in MERGE_MAP.items():
    obj_folder = COMPONENTS / obj_name
    set_folder = COMPONENTS / set_name
    if obj_folder.exists() and set_folder.exists():
        # Both exist — merge object's working.py into set's
        obj_working = obj_folder / "working.py"
        set_working = set_folder / "working.py"
        if obj_working.exists() and set_working.exists():
            set_code = set_working.read_text(encoding="utf-8")
            obj_code = obj_working.read_text(encoding="utf-8")
            if "def action(" not in set_code and "def action(" in obj_code:
                # Append action() from object to set
                action_start = obj_code.index("def action(")
                set_code = set_code.rstrip() + "\n\n\n" + obj_code[action_start:]
                set_working.write_text(set_code, encoding="utf-8")
                print(f"  Merged action() from {obj_name}/ into {set_name}/working.py")
        # Remove the singular object folder
        shutil.rmtree(obj_folder)
        print(f"  Removed {obj_name}/ (merged into {set_name}/)")
    elif obj_folder.exists() and not set_folder.exists():
        # Only object exists, rename to plural
        obj_folder.rename(set_folder)
        print(f"  Renamed {obj_name}/ -> {set_name}/")

# ── Step 5: Create __init__.py ──────────────────────────────────────────
init_file = COMPONENTS / "__init__.py"
if not init_file.exists():
    init_file.write_text("", encoding="utf-8")
    print(f"\nCreated {init_file}")

# ── Summary ─────────────────────────────────────────────────────────────
folders = sorted(f.name for f in COMPONENTS.iterdir() if f.is_dir() and not f.name.startswith("__"))
print(f"\n=== DONE === {len(folders)} component folders in components/")
for f in folders[:20]:  # Show first 20
    print(f"  {f}/")
if len(folders) > 20:
    print(f"  ... and {len(folders) - 20} more")
