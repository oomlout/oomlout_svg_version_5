import os

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'save'
    d["name_long_5"] = 'save_text'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_save_text'
    d["name_long"] = 'roboclick_action_ai_save_text'
    d["name_short"] = ['save_text', 'text', 'ai_save_text']
    d["name_short_options"] = ['save_text', 'text', 'ai_save_text']
    d["description"] = 'Save text.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'file_name_full', 'description': 'Full file path to save captured content.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name_clip', 'description': 'File path used to store clipboard text.', 'type': 'string', 'default': ''})
        v.append({'name': 'clip', 'description': 'Clipboard text payload to save. default:&&&tag for copy&&&', 'type': 'string', 'default': '&&&tag for copy&&&'})
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
    """Save text content from AI default between &&&tag for copy&&&"""
    action = kwargs.get("action", {})
    remove_double_line_breaks = action.get("remove_double_line_breaks", True)
    file_name_full = action.get("file_name_full", "text.txt")
    file_name_clip = action.get("file_name_clip", "")
    if file_name_clip == "":
        file_name_full = action.get("file_name", "")
        if file_name_full == "":
            file_name_full = action.get("file_destination", "clip.txt")
    
    
    clip = action.get("clip", "&&&tag for copy&&&")
    directory = kwargs.get("directory", "")

    robo.robo_mouse_click(position=[300, 300], delay=2, button="left")  # Click to focus
    text = robo.robo_keyboard_copy(delay=2)  # Copy the selected text

    if file_name_full != "":
        file_name_full_full = os.path.join(directory, file_name_full)
        with open(file_name_full_full, 'w', encoding='utf-8') as f:
            f.write(text)
            print(f"Text saved to {file_name_full_full}")
    if file_name_clip != "":
        file_name_clip_full = os.path.join(directory, file_name_clip)
        with open(file_name_clip_full, 'w', encoding='utf-8') as f:
            #text between two clip tages
            clipping = text.split(clip)
            if len(clipping) > 1:
                clipping = clipping[len(clipping)-2]
            else:
                clipping = text
            if remove_double_line_breaks:
                clipping = clipping.replace("\n\n", "\n")
                clipping = clipping.replace("\n\n", "\n")
            f.write(clipping)
            print(f"Clip text saved to {file_name_clip_full}")

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
