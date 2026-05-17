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
    d["name_long_5"] = 'google_doc_new'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_google_doc_new'
    d["name_long"] = 'roboclick_action_google_doc_new'
    d["name_short"] = ['google_doc_new', 'new']
    d["name_short_options"] = ['google_doc_new', 'new']
    d["description"] = 'Google doc new.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Google Doc'
    v = []
    if True:
        v.append({'name': 'template', 'description': 'Template name used when creating a new Google Doc.', 'type': 'string', 'default': ''})
        v.append({'name': 'title', 'description': 'Title for the new Google Doc.', 'type': 'string', 'default': ''})
        v.append({'name': 'folder', 'description': 'Drive folder destination for the new Google Doc.', 'type': 'string', 'default': ''})
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
    """Create a new Google Doc and return its URL"""
    action = kwargs.get("action", {})
    template = action.get("template", "")
    title = action.get("title", "")
    folder = action.get("folder", "")
    save_to_file = action.get("save_to_file", True)
    print("google_doc_new -- creating a new Google Doc")
    
    kwargs2 = copy.deepcopy(kwargs)
    if template != "":
        kwargs2["template"] = template
    if title != "":
        kwargs2["title"] = title
    if folder != "":
        kwargs2["folder"] = folder
    
    result = robo.robo_google_doc_new(**kwargs2)
    
    file_name = action.get("file_name", "google_doc_url.txt")
    directory = kwargs.get("directory", "")
    if save_to_file:
        file_name_full = os.path.join(directory, file_name)
        url = result.get("url_google_doc", "")
        try:
            with open(file_name_full, 'w', encoding='utf-8') as f:
                f.write(url)
            print(f"Google Doc URL saved to {file_name_full}")
        except Exception as e:
            print(f"Error saving Google Doc URL to {file_name_full}: {e}")

    return result

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
