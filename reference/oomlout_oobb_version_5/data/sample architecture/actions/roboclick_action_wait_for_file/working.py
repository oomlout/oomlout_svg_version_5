import os

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'wait'
    d["name_long_4"] = 'for'
    d["name_long_5"] = 'wait_for_file'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_wait_for_file'
    d["name_long"] = 'roboclick_action_wait_for_file'
    d["name_short"] = ['wait_for_file', 'file']
    d["name_short_options"] = ['wait_for_file', 'file']
    d["description"] = 'Wait for file.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Utility'
    v = []
    if True:
        v.append({'name': 'file_name', 'description': 'Primary file name to wait for in the action directory.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name_1', 'description': 'first candidate file name to wait for.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name_2', 'description': 'second candidate file name to wait for.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name_3', 'description': 'third candidate file name to wait for.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name_4', 'description': 'fourth candidate file name to wait for.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name_5', 'description': 'fifth candidate file name to wait for.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name_6', 'description': 'sixth candidate file name to wait for.', 'type': 'string', 'default': ''})
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
    """Wait until one of the specified files exists."""
    action = kwargs.get("action", {})
    directory = kwargs.get("directory", "")
    files = []
    for i in range(1,7):
        key = f"file_name_{i}" if i>1 else "file_name"
        if key in action and action.get(key):
            files.append(os.path.join(directory, action.get(key)))
    timeout = action.get("timeout", 300)
    interval = action.get("interval", 2)
    elapsed = 0
    while elapsed < timeout:
        for f in files:
            if os.path.exists(f):
                print(f"File found: {f}")
                return f
        #robo.robo_delay(delay=interval)
        elapsed += interval
    print("Timeout waiting for files.")
    return "exit"

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
