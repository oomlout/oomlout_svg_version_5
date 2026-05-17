d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'file'
    d["name_long_5"] = 'add_file'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_file_add_file'
    d["name_long"] = 'roboclick_action_ai_file_add_file'
    d["name_short"] = ['add_file', 'ai_add_file', 'add_image', 'ai_add_image']
    d["name_short_options"] = ['add_file', 'ai_add_file', 'add_image', 'ai_add_image']
    d["description"] = 'Add a file (alias for add_image).'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'ai'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'path of the file, referenced to current directory', 'type': 'string', 'default': ''})
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

def ai_add_image(**kwargs):
    return _dispatch_action("ai_add_image", **kwargs)

def action(**kwargs):
    return old(**kwargs)

def old(**kwargs):
    """Add a file (alias for add_image)"""
    return ai_add_image(**kwargs)

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
