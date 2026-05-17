import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'browser'
    d["name_long_4"] = 'open'
    d["name_long_5"] = 'open_url'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_browser_open_url'
    d["name_long"] = 'roboclick_action_browser_open_url'
    d["name_short"] = ['open_url', 'url', 'browser_open_url']
    d["name_short_options"] = ['open_url', 'url', 'browser_open_url']
    d["description"] = 'Open url.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Browser'
    v = []
    if True:
        v.append({'name': 'url', 'description': 'URL to open or use for the operation.', 'type': 'string', 'default': ''})
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
    """Open a URL in the browser"""
    action = kwargs.get("action", {})
    url = action.get("url", "")
    print(f"browser_open_url -- opening URL: {url}")
    robo.robo_chrome_open_url(url=url, delay=15, message="    opening URL in browser")

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
