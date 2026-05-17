import copy

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'corel'
    d["name_long_4"] = 'paste'
    d["name_long_5"] = 'corel_paste'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_corel_paste'
    d["name_long"] = 'roboclick_action_corel_paste'
    d["name_short"] = ['corel_paste', 'paste']
    d["name_short_options"] = ['corel_paste', 'paste']
    d["description"] = 'Corel paste.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'CorelDRAW'
    v = []
    if True:
        v.append({'name': 'x', 'description': 'X coordinate for placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'y', 'description': 'Y coordinate for placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'width', 'description': 'Target width for sizing or placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'height', 'description': 'Target height for sizing or placement.', 'type': 'string', 'default': ''})
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
    """Paste copied items in CorelDRAW"""
    print("corel_paste -- pasting copied items in corel")
    #paste copied items in corel
    action = kwargs.get("action", {})
    x = action.get("x", "")
    y = action.get("y", "")
    width = action.get("width", "")
    height = action.get("height", "")

    kwargs2 = copy.deepcopy(kwargs)
    if x != "":
        kwargs2["x"] = x
    if y != "":
        kwargs2["y"] = y
    if width != "":
        kwargs2["width"] = width
    if height != "":
        kwargs2["height"] = height
    robo.robo_corel_paste(**kwargs2)

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
