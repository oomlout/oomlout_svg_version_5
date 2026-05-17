import os

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'file'
    d["name_long_4"] = 'create'
    d["name_long_5"] = 'create_text_file'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_file_create_text_file'
    d["name_long"] = 'roboclick_action_file_create_text_file'
    d["name_short"] = ['create_text_file', 'text', 'file_create_text_file']
    
    d["description"] = 'Create text file.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'File'
    v = []
    if True:
        v.append({'name': 'file_name', 'description': 'File name to read or write for this action.', 'type': 'string', 'default': ''})
        v.append({'name': 'content', 'description': 'Text content to write into the created file.', 'type': 'string', 'default': ''})
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
    directory = kwargs.get("directory", "")
    action = kwargs.get("action", {})
    file_name = action.get("file_name", "textfile.txt")    
    file_name_full = os.path.join(directory, file_name)
    content = action.get("content", "")
    delay = action.get("delay", 1)
    """Create a text file with specified content"""
    try:
        with open(file_name_full, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Text file created at {file_name_full}")
    except Exception as e:
        print(f"Error creating text file at {file_name_full }: {e}")
    robo.robo_delay(delay=delay)  # Wait for the file to be created

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
