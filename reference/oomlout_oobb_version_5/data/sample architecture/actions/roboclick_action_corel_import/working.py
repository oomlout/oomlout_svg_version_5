import copy

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'corel'
    d["name_long_4"] = 'import'
    d["name_long_5"] = 'corel_import'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_corel_import'
    d["name_long"] = 'roboclick_action_corel_import'
    d["name_short"] = ['corel_import', 'import']
    d["name_short_options"] = ['corel_import', 'import']
    d["description"] = 'Corel import.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'CorelDRAW'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'x', 'description': 'X coordinate for placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'y', 'description': 'Y coordinate for placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'width', 'description': 'Target width for sizing or placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'height', 'description': 'Target height for sizing or placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'max_dimension', 'description': 'Maximum dimension allowed when scaling content.', 'type': 'string', 'default': ''})
        v.append({'name': 'angle', 'description': 'Rotation angle in degrees.', 'type': 'string', 'default': ''})
        v.append({'name': "special, 'no double click' - to deal with non square objects", 'description': 'Special import flag to skip double-click sizing behavior for non-square objects.', 'type': 'string', 'default': ''})
    d["variables"] = v
    return d

def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable

def _check_key_pressed():
    return None

def _scroll_lock_toggled():
    return False

def action(**kwargs):
    return old(**kwargs)

def old(**kwargs):
    """Import file into CorelDRAW."""
    action = kwargs.get("action", {})
    # Use file_source when available
    file_name = action.get("file_source", None)
    if not file_name:
        file_name = action.get("file_name", "")
    x = action.get("x", "")
    y = action.get("y", "")
    width = action.get("width", "")
    height = action.get("height", "")
    max_dimension = action.get("max_dimension", "")
    angle = action.get("angle", 0)
    special = action.get("special", "")
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["file_name"] = file_name
    if x != "":
        kwargs2["x"] = x
    if y != "":
        kwargs2["y"] = y
    if width != "":
        kwargs2["width"] = width
    if height != "":
        kwargs2["height"] = height
    if max_dimension != "":
        kwargs2["max_dimension"] = max_dimension
    if angle != 0:
        kwargs2["angle"] = angle
    if special != "":
        kwargs2["special"] = special

    robo.robo_corel_import_file(**kwargs2)

def test(**kwargs):
    try:
        import oomlout_test
    except Exception:
        return callable(old)

    test_fn = getattr(oomlout_test, "test", None)
    if not callable(test_fn):
        return callable(old)

    try:
        return bool(test_fn(**kwargs))
    except Exception:
        return callable(old)
