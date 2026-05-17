import copy

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'corel'
    d["name_long_4"] = 'trace'
    d["name_long_5"] = 'corel_trace'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_corel_trace'
    d["name_long"] = 'roboclick_action_corel_trace'
    d["name_short"] = ['corel_trace', 'trace']
    d["name_short_options"] = ['corel_trace', 'trace']
    d["description"] = 'Corel trace.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'CorelDRAW'
    v = []
    if True:
        v.append({'name': 'file_name', 'description': 'File name to read or write for this action.', 'type': 'string', 'default': ''})
        v.append({'name': 'remove_background_color_from_entire_image', 'description': 'Whether to remove the background color before tracing.', 'type': 'string', 'default': ''})
        v.append({'name': 'delay_trace', 'description': 'Delay in seconds before trace-specific steps.', 'type': 'string', 'default': ''})
        v.append({'name': 'number_of_colors', 'description': 'Color count target used by trace settings.', 'type': 'string', 'default': ''})
        v.append({'name': 'detail_minus', 'description': 'Trace detail reduction amount.', 'type': 'string', 'default': ''})
        v.append({'name': 'smoothing', 'description': 'Trace smoothing level.', 'type': 'string', 'default': ''})
        v.append({'name': 'corner_smoothness', 'description': 'Corner smoothing level for trace output.', 'type': 'string', 'default': ''})
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
    """Trace bitmap image in CorelDRAW"""
    print("corel_trace -- tracing")
    action = kwargs.get("action", {})
    kwargs2 = copy.deepcopy(kwargs)    
    file_name = action.get("file_name", "")
    kwargs2["file_name"] = file_name
    remove_background_color_from_entire_image = action.get("remove_background_color_from_entire_image", False)
    if remove_background_color_from_entire_image == "":
        remove_background_color_from_entire_image = False
    kwargs2["remove_background_color_from_entire_image"] = remove_background_color_from_entire_image    
    
    delay_trace = action.get("delay_trace", None)
    number_of_colors = action.get("number_of_colors", None)
    if number_of_colors is not None and number_of_colors != "":
        kwargs2["number_of_colors"] = number_of_colors
    detail_minus = action.get("detail_minus", None)
    if detail_minus is not None:
        kwargs2["detail_minus"] = detail_minus
    smoothing = action.get("smoothing", None)
    if smoothing is not None:
        kwargs2["smoothing"] = smoothing
    corner_smoothness = action.get("corner_smoothness", None)
    if corner_smoothness is not None:
        kwargs2["corner_smoothness"] = corner_smoothness
    
    
    delay_trace = action.get("delay_trace", 30)
    kwargs2["delay_trace"] = delay_trace

    robo.robo_corel_trace(**kwargs2)
    pass

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
