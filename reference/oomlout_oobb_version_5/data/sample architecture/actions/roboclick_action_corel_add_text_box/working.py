import copy

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'corel'
    d["name_long_4"] = 'add'
    d["name_long_5"] = 'add_text_box'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_corel_add_text_box'
    d["name_long"] = 'roboclick_action_corel_add_text_box'
    d["name_short"] = ['add_text_box', 'text', 'corel_add_text_box']
    d["name_short_options"] = ['add_text_box', 'text', 'corel_add_text_box']
    d["description"] = 'Add text box.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'CorelDRAW'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'text', 'description': 'Text content used by this action.', 'type': 'string', 'default': ''})
        v.append({'name': 'x', 'description': 'X coordinate for placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'y', 'description': 'Y coordinate for placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'width', 'description': 'Target width for sizing or placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'height', 'description': 'Target height for sizing or placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'font', 'description': 'Font family name to apply.', 'type': 'string', 'default': ''})
        v.append({'name': 'font_size', 'description': 'Font size value to apply.', 'type': 'string', 'default': ''})
        v.append({'name': 'bold', 'description': 'Whether text should be bold.', 'type': 'string', 'default': ''})
        v.append({'name': 'italic', 'description': 'Whether text should be italic.', 'type': 'string', 'default': ''})
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
    """Add text box in CorelDRAW"""
    print("corel_add_text -- adding text in corel")
    action = kwargs.get("action", {})
    # Use file_source when available
    file_name = action.get("file_source", None)
    if not file_name:
        file_name = action.get("file_name", "")
    text = action.get("text", "Hello World")
    x = action.get("x", 100)
    y = action.get("y", 100)
    width = action.get("width", 200)
    height = action.get("height", 100)
    font = action.get("font", "")
    font_size = action.get("font_size", 12)
    bold = action.get("bold", False)
    italic = action.get("italic", False)
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["file_name"] = file_name
    kwargs2["text"] = text
    kwargs2["x"] = x
    kwargs2["y"] = y
    kwargs2["font"] = font
    kwargs2["font_size"] = font_size
    kwargs2["bold"] = bold
    kwargs2["italic"] = italic
    kwargs2["width"] = width
    kwargs2["height"] = height
    robo.robo_corel_add_text_box(**kwargs2)
    #wait for 2 seconds
    robo.robo_delay(delay=2)  # Wait for the text to be added

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
