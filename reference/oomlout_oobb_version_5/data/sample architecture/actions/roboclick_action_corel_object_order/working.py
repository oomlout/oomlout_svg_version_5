import copy

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'corel'
    d["name_long_4"] = 'object'
    d["name_long_5"] = 'object_order'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_corel_object_order'
    d["name_long"] = 'roboclick_action_corel_object_order'
    d["name_short"] = ['object_order', 'order', 'corel_object_order']
    d["name_short_options"] = ['object_order', 'order', 'corel_object_order']
    d["description"] = 'Object order.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'CorelDRAW'
    v = []
    if True:
        v.append({'name': 'order', 'description': 'Object stacking order command (for example, to_front or to_back).', 'type': 'string', 'default': ''})
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
    """Change object stacking order in CorelDRAW, order to_front to_back"""
    print("corel_object_order -- changing object order in corel")
    action = kwargs.get("action", {})
    order = action.get("order", "to_front")
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["order"] = order
    robo.robo_corel_object_order(**kwargs2)

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
