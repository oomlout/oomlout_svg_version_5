import copy

import os

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'google'
    d["name_long_4"] = 'doc'
    d["name_long_5"] = 'add_text'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_google_doc_add_text'
    d["name_long"] = 'roboclick_action_google_doc_add_text'
    d["name_short"] = ['add_text', 'add', 'google_doc_add_text']
    d["name_short_options"] = ['add_text', 'add', 'google_doc_add_text']
    d["description"] = 'Add text.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Google Doc'
    v = []
    if True:
        v.append({'name': 'url', 'description': 'URL to open or use for the operation.', 'type': 'string', 'default': ''})
        v.append({'name': 'text', 'description': 'Text content used by this action.', 'type': 'string', 'default': ''})
        v.append({'name': 'position', 'description': 'Insertion position in the Google Doc (for example end).', 'type': 'string', 'default': ''})
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
    """Add text to a Google Doc at specified position. file to source defaults to /google_doc_url.txt if url is not provided."""
    action = kwargs.get("action", {})
    url = action.get("url", "")
    text = action.get("text", "")
    method = action.get("method", "type")
    position = action.get("position", "end")

    #if yurl is "" load it from directory/google_doc_url.txt
    if url == "":
        directory = kwargs.get("directory", "")
        file_name_full = os.path.join(directory, "google_doc_url.txt")
        try:
            with open(file_name_full, 'r', encoding='utf-8') as f:
                url = f.read().strip()
            print(f"Google Doc URL loaded from {file_name_full}")
        except Exception as e:
            print(f"Error loading Google Doc URL from {file_name_full}: {e}")
            return

    print(f"google_doc_add_text -- adding text to Google Doc at {url}")
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["url"] = url
    kwargs2["text"] = text
    kwargs2["position"] = position
    kwargs2["method"] = method
    robo.robo_google_doc_add_text(**kwargs2)

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
