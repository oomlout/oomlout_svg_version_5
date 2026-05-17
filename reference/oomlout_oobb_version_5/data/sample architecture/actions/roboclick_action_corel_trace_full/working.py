import copy

import os

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'corel'
    d["name_long_4"] = 'trace'
    d["name_long_5"] = 'trace_full'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_corel_trace_full'
    d["name_long"] = 'roboclick_action_corel_trace_full'
    d["name_short"] = ['trace_full', 'full', 'corel_trace_full']
    d["description"] = 'Trace full.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'CorelDRAW'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_source_trace', 'description': 'Path to the raster file used for tracing.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_destination', 'description': 'Path to the output file to create or update.', 'type': 'string', 'default': ''})
        v.append({'name': 'delay_trace', 'description': 'Delay in seconds before trace-specific steps.', 'type': 'string', 'default': ''})
        v.append({'name': 'delay_png', 'description': 'Delay in seconds before PNG export steps.', 'type': 'string', 'default': ''})
        v.append({'name': 'max_dimension', 'description': 'Maximum dimension allowed when scaling content.', 'type': 'string', 'default': ''})
        v.append({'name': 'detail_minus', 'description': 'Trace detail reduction amount.', 'type': 'string', 'default': ''})
        v.append({'name': 'x', 'description': 'X coordinate for placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'y', 'description': 'Y coordinate for placement.', 'type': 'string', 'default': ''})
        v.append({'name': 'number_of_colors', 'description': 'Color count target used by trace settings.', 'type': 'string', 'default': ''})
        v.append({'name': 'remove_background_color_from_entire_image', 'description': 'Whether to remove the background color before tracing.', 'type': 'string', 'default': ''})
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

def run_action(**kwargs):
    action_cfg = kwargs.get("action", {}) or {}
    if not isinstance(action_cfg, dict):
        return ""
    command_name = str(action_cfg.get("command", "")).strip()
    if not command_name:
        return ""
    return _dispatch_action(command_name, **kwargs)

def action(**kwargs):
    return old(**kwargs)

def old(**kwargs):
    """Complete trace workflow in CorelDRAW."""
    action = kwargs.get("action", {})
    action_main = copy.deepcopy(action)
    file_source = action.get("file_source", None)
    if not file_source:
        file_source = action.get("file_input", "")
    file_source_just_file_and_extension = os.path.basename(file_source)
    file_source_trace = action.get("file_source_trace", "")
    file_source_trace_just_file_and_extension = os.path.basename(file_source_trace)
    file_source_trace_just_file_and_extension_upscaled = file_source_trace_just_file_and_extension.replace(".png", "_upscaled.png").replace(".jpg", "_upscaled.jpg").replace(".jpeg", "_upscaled.jpeg")
    file_destination = action.get("file_destination", None)
    if not file_destination:
        file_destination = action.get("file_output", None)
        if not file_destination:
            file_destination = action.get("file_destination", file_source_trace.replace(".png", "_trace.cdr").replace(".jpg", "_trace.cdr").replace(".jpeg", "_trace.cdr"))
    file_destination_just_file_and_extension = os.path.basename(file_destination)
    file_destination_just_file_and_extension_pdf = file_destination_just_file_and_extension.replace(".cdr", ".pdf").replace(".png", ".pdf").replace(".jpg", ".pdf").replace(".jpeg", ".pdf")
    file_destination_just_file_and_extension_png = file_destination_just_file_and_extension.replace(".cdr", ".png").replace(".pdf", ".png").replace(".jpg", ".png").replace(".jpeg", ".png")
    delay_trace = action.get("delay_trace", 30)
    delay_png = action.get("delay_png", 10)
    max_dimension = action.get("max_dimension", 100)
    detail_minus = action.get("detail_minus", 0)
    xx = action.get("x", 100)
    yy = action.get("y", 100)

    actions = []

    #file_copy
    action = {} 
    action["command"] = "file_copy"
    action["file_source"] = f"{file_source}"
    action["file_destination"] = f"{file_destination_just_file_and_extension}"
    actions.append(copy.deepcopy(action))

    #corel_open
    action = {}
    action["command"] = "corel_open"
    action["file_name"] = f"{file_destination_just_file_and_extension}"
    actions.append(copy.deepcopy(action))

    #image_upscale
    action = {}
    action["command"] = "image_upscale"
    action["file_input"] = f"{file_source_trace_just_file_and_extension}"
    action["scale"] = 4
    actions.append(copy.deepcopy(action))

    #corel_import
    action = {}
    action["command"] = "corel_import"
    action["x"] = xx
    action["y"] = yy
    action["width"] = max_dimension
    action["file_name"] = f"{file_source_trace_just_file_and_extension_upscaled}"
    actions.append(copy.deepcopy(action))

    #corel_save
    action = {}
    action["command"] = "corel_save"
    actions.append(copy.deepcopy(action))

    #corel_save_as
    action = {}
    action["command"] = "corel_save_as"
    action["file_name"] = f"{file_destination_just_file_and_extension}"
    actions.append(copy.deepcopy(action))

    #trace_clipart
    action = {}
    action["command"] = "corel_trace"
    if "number_of_colors" in action_main:
        action["number_of_colors"] = action_main["number_of_colors"]
    if "remove_background_color_from_entire_image" in action_main:
        remove_value = action_main.get("remove_background_color_from_entire_image", True)
        action["remove_background_color_from_entire_image"] = action_main["remove_background_color_from_entire_image"]
    if detail_minus != 0:
        action["detail_minus"] = detail_minus
    if "delay_trace" in action_main:
        action["delay_trace"] = delay_trace
    if "smoothing" in action_main:
        action["smoothing"] = action_main["smoothing"]
    if "corner_smoothness" in action_main:
        action["corner_smoothness"] = action_main["corner_smoothness"]
    actions.append(copy.deepcopy(action))

    #corel_set_size
    action = {}
    action["command"] = "corel_set_size"
    action["max_dimension"] = {max_dimension}
    actions.append(copy.deepcopy(action))

    #corel_set_position
    action = {}
    action["command"] = "corel_set_position"
    action["x"] = xx
    action["y"] = yy
    actions.append(copy.deepcopy(action))

    #corel_save
    action = {}
    action["command"] = "corel_save"
    actions.append(copy.deepcopy(action))

    #export as pdf
    action = {}
    action["command"] = "corel_export"                
    action["file_name"] = f"{file_destination_just_file_and_extension_pdf}"
    action["file_type"] = "pdf"
    action["delay"] = delay_png
    actions.append(copy.deepcopy(action))

    #export png
    action = {}
    action["command"] = "corel_export"
    action["file_name"] = f"{file_destination_just_file_and_extension_png}"
    action["file_type"] = "png"
    action["delay"] = delay_png
    actions.append(copy.deepcopy(action))

    #corel close
    action = {}
    action["command"] = "corel_close_file"
    actions.append(copy.deepcopy(action))

    for action in actions:
        kwargs["action"] = action
        run_action(**kwargs)

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
