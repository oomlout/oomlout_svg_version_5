"""Fix part_calls.objects.oobb_object_* → components.* imports in dispatch files."""
import re
from pathlib import Path

# Merge map from migration script
MERGE_MAP = {
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

ROOT = Path(".")

def map_import(old_import):
    """Convert part_calls.objects.oobb_object_XXX.working to components.YYY.working"""
    # Extract the object name after oobb_object_
    m = re.search(r'part_calls\.objects\.oobb_object_([a-z0-9_]+)\.working', old_import)
    if not m:
        return old_import
    obj_name = m.group(1)
    # Check merge map first
    new_name = MERGE_MAP.get(obj_name, obj_name)
    # Verify folder exists
    if not (ROOT / "components" / new_name / "working.py").exists():
        print(f"  WARNING: components/{new_name}/working.py does not exist for {obj_name}")
        return old_import
    new_import = old_import.replace(f"part_calls.objects.oobb_object_{obj_name}.working", 
                                     f"components.{new_name}.working")
    return new_import

files_to_fix = [
    "oobb_get_items_oobb.py",
    "oobb_get_items_other.py", 
    "oobb_get_items_test.py",
]

for fname in files_to_fix:
    fpath = ROOT / fname
    text = fpath.read_text(encoding="utf-8")
    # Find all part_calls imports
    pattern = r'from\s+part_calls\.objects\.oobb_object_[a-z0-9_]+\.working\s+import\s+action'
    matches = re.findall(pattern, text)
    if not matches:
        print(f"{fname}: no part_calls imports found")
        continue
    
    new_text = text
    for match in matches:
        new_import = map_import(match)
        if new_import != match:
            new_text = new_text.replace(match, new_import)
            print(f"  {fname}: {match[:60]}... -> ...{new_import.split('from ')[1][:50] if 'from ' in new_import else new_import[:50]}")
    
    # Also fix comment references
    new_text = re.sub(r'part_calls/objects/oobb_object_(\w+)/', 
                       lambda m: f"components/{MERGE_MAP.get(m.group(1), m.group(1))}/",
                       new_text)
    
    if new_text != text:
        fpath.write_text(new_text, encoding="utf-8")
        count = len(matches)
        print(f"  {fname}: Updated {count} imports")
    else:
        print(f"  {fname}: No changes needed")
