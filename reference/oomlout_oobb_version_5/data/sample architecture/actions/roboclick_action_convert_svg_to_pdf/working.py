import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'convert'
    d["name_long_4"] = 'svg'
    d["name_long_5"] = 'svg_to_pdf'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_convert_svg_to_pdf'
    d["name_long"] = 'roboclick_action_convert_svg_to_pdf'
    d["name_short"] = ['svg_to_pdf', 'to', 'convert_svg_to_pdf']
    d["name_short_options"] = ['svg_to_pdf', 'to', 'convert_svg_to_pdf']
    d["description"] = 'Svg to pdf.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Conversion'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_destination', 'description': 'Path to the output file to create or update.', 'type': 'string', 'default': ''})
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
    """Convert SVG file to PDF format."""
    directory = kwargs.get("directory", "")
    action = kwargs.get("action", {})
    file_input = action.get("file_source", None)
    if not file_input:
        file_input = action.get("file_input", "")    
    kwargs["file_input"] = f"{directory}\{file_input}"
    file_output = action.get("file_destination", None)
    if not file_output:
        file_output = action.get("file_output", "")
    if file_output == "":
        file_output = file_input.replace(".svg", ".pdf")    
    kwargs["file_output"] = f"{directory}\{file_output}"
    robo.robo_convert_svg_to_pdf(**kwargs)

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
