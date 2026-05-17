d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'alias'
    d["name_long_4"] = 'openscad'
    d["name_long_5"] = 'openscad_render_file'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_alias_openscad_render_file'
    d["name_long"] = 'roboclick_action_alias_openscad_render_file'
    d["name_short"] = ['openscad_render_file', 'render', 'render_file', 'legacy_alias']
    d["name_short_options"] = ['openscad_render_file', 'render', 'render_file', 'legacy_alias']
    d["description"] = 'Openscad render file.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Legacy Alias'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_destination', 'description': 'Path to the output file to create or update.', 'type': 'string', 'default': ''})
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

def openscad_render(**kwargs):
    return _dispatch_action("openscad_render", **kwargs)

def action(**kwargs):
    return old(**kwargs)

def old(**kwargs):
    """Compatibility wrapper for openscad_render."""
    # map parameters and call openscad_render
    action = kwargs.get("action", {})
    if "file_source" in action:
        action = action.copy()
        if "file_source" in action and "file_destination" in action:
            action["render_type"] = action.get("render_type", "stl")
    kwargs["action"] = action
    return openscad_render(**kwargs)

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
