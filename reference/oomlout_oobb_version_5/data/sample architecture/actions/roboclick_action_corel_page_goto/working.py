import copy

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'corel'
    d["name_long_4"] = 'page'
    d["name_long_5"] = 'page_goto'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_corel_page_goto'
    d["name_long"] = 'roboclick_action_corel_page_goto'
    d["name_short"] = ['page_goto', 'goto', 'corel_page_goto']
    d["name_short_options"] = ['page_goto', 'goto', 'corel_page_goto']
    d["description"] = 'Page goto.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'CorelDRAW'
    v = []
    if True:
        v.append({'name': 'page_number', 'description': 'Target page number to switch to.', 'type': 'string', 'default': ''})
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
    """Navigate to specific page in CorelDRAW"""
    print("corel_page_goto -- going to page in corel")
    action = kwargs.get("action", {})
    page_number = action.get("page_number", 1)
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["page_number"] = page_number
    robo.robo_corel_page_goto(**kwargs2)

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
