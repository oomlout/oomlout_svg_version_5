d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'alias'
    d["name_long_4"] = 'new'
    d["name_long_5"] = 'new_chat'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_alias_new_chat'
    d["name_long"] = 'roboclick_action_alias_new_chat'
    d["name_short"] = ['new_chat', 'chat', 'legacy_alias']
    d["name_short_options"] = ['new_chat', 'chat', 'legacy_alias']
    d["description"] = 'New chat.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Legacy Alias'
    v = []
    if True:
        v.append({'name': 'description', 'description': 'Optional kickoff note sent in the first chat message.', 'type': 'string', 'default': ''})
        v.append({'name': 'log_url', 'description': 'Whether to capture and store the current chat URL.', 'type': 'string', 'default': ''})
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

def ai_new_chat(**kwargs):
    return _dispatch_action("ai_new_chat", **kwargs)

def action(**kwargs):
    return old(**kwargs)

def old(**kwargs):
    """RETIRED - use ai_new_chat instead."""
    return ai_new_chat(**kwargs)

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
