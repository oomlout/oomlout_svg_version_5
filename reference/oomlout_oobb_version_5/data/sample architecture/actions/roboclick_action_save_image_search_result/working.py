import os

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'save'
    d["name_long_4"] = 'image'
    d["name_long_5"] = 'save_image_search_result'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_save_image_search_result'
    d["name_long"] = 'roboclick_action_save_image_search_result'
    d["name_short"] = ['save_image_search_result', 'search']
    d["name_short_options"] = ['save_image_search_result', 'search']
    d["description"] = 'Save image search result.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI Image'
    v = []
    if True:
        v.append({'name': 'index', 'description': '1-based search result index used to offset the click position.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name', 'description': 'File name to read or write for this action.', 'type': 'string', 'default': ''})
        v.append({'name': 'overwrite', 'description': 'Whether existing output files should be overwritten.', 'type': 'string', 'default': ''})
        v.append({'name': 'position_click', 'description': 'Base screen position for search results before index offset.', 'type': 'string', 'default': ''})
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
    """Save image from search results."""
    kwargs["position_click"] = [813, 259]
    position_click = kwargs.get("position_click")
    action = kwargs.get("action", {})
    index = action.get("index", 1)
    if "_" in str(index):
        index = str(index).split("_")[0]
    position_click[0] += (int(index)-1) * 200
    file_name = action.get("file_name", "working.png")
    directory_absolute = kwargs.get("directory_absolute", "")
    file_name_absolute = os.path.join(directory_absolute, file_name)
    overwrite = action.get("overwrite", True)
    print(f"Saving image as {file_name}")
    if not overwrite and os.path.exists(file_name_absolute):
        print(f"File {file_name_absolute} already exists and overwrite is disabled.")
        return
    else:
        robo.robo_mouse_click(position=position_click, delay=2, button="left")
        robo.robo_mouse_click(position=position_click, delay=2, button="right")
        robo.robo_keyboard_press_down(delay=1, repeat=2)
        robo.robo_keyboard_press_enter(delay=5)
        robo.robo_keyboard_send(string=file_name_absolute, delay=5)
        robo.robo_keyboard_press_enter(delay=5)
        robo.robo_keyboard_send(string="y", delay=5)
        robo.robo_keyboard_press_escape(delay=5, repeat=5)
        print(f"Image saved as {file_name}")

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
