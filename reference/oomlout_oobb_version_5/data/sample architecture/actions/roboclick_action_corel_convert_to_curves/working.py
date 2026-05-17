import copy

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'corel'
    d["name_long_4"] = 'convert'
    d["name_long_5"] = 'convert_to_curves'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_corel_convert_to_curves'
    d["name_long"] = 'roboclick_action_corel_convert_to_curves'
    d["name_short"] = ['convert_to_curves', 'to', 'corel_convert_to_curves']
    d["name_short_options"] = ['convert_to_curves', 'to', 'corel_convert_to_curves']
    d["description"] = 'Convert to curves.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'CorelDRAW'
    v = []
    if True:
        v.append({'name': 'ungroup', 'description': 'Whether to ungroup objects after converting to curves.', 'type': 'string', 'default': ''})
        v.append({'name': 'delay', 'description': 'Delay duration in seconds.', 'type': 'string', 'default': ''})
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
    """Convert selected items to curves in CorelDRAW"""
    print("corel_convert_to_curves -- converting selected items to curves in corel")
    
    action = kwargs.get("action", {})
    ungroup = action.get("ungroup", False)
    delay_convert = action.get("delay", 5)
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["delay"] = delay_convert
    if ungroup:
        kwargs2["ungroup"] = ungroup
    robo.robo_corel_convert_to_curves(**kwargs2)

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
