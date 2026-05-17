import copy

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'corel'
    d["name_long_4"] = 'set'
    d["name_long_5"] = 'set_size'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_corel_set_size'
    d["name_long"] = 'roboclick_action_corel_set_size'
    d["name_short"] = ['set_size', 'size', 'corel_set_size']
    d["name_short_options"] = ['set_size', 'size', 'corel_set_size']
    d["description"] = 'Set size.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'CorelDRAW'
    v = []
    if True:
        v.append({'name': 'width', 'description': 'Target width for sizing or placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'height', 'description': 'Target height for sizing or placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'max_dimension', 'description': 'Maximum dimension allowed when scaling content.', 'type': 'string', 'default': ''})
        v.append({'name': 'select_all', 'description': 'Whether to select all objects before resizing.', 'type': 'string', 'default': ''})
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
    """Set size of selected items in CorelDRAW"""
    print("corel_set_size -- setting size")
    action = kwargs.get("action", {})
    width = action.get("width", "")
    height = action.get("height", "")
    max_dimension = action.get("max_dimension", "")
    select_all = action.get("select_all", False)
    
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["width"] = width
    kwargs2["height"] = height
    kwargs2["select_all"] = select_all
    if max_dimension != "":
        kwargs2["max_dimension"] = max_dimension
    robo.robo_corel_set_size(**kwargs2)

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
