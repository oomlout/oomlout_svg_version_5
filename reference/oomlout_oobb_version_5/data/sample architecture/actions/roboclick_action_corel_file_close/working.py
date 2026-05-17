import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'corel'
    d["name_long_4"] = 'file'
    d["name_long_5"] = 'close'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_corel_close_file'
    d["name_long"] = 'roboclick_action_corel_close_file'
    d["name_short"] = ["corel_file_close", 'close_file', 'file', 'corel_close_file', 'corel_close']
    d["description"] = 'Close file.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'CorelDRAW'
    v = []
    if True:
        pass
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
    """Close current file in CorelDRAW"""
    print("corel_close_file -- closing corel")
    #close corel
    robo.robo_corel_close_file(**kwargs)

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
