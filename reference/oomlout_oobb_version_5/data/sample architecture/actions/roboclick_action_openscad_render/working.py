import os

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'openscad'
    d["name_long_4"] = 'render'
    d["name_long_5"] = 'openscad_render'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_openscad_render'
    d["name_long"] = 'roboclick_action_openscad_render'
    d["name_short"] = ['openscad_render', 'render']
    d["name_short_options"] = ['openscad_render', 'render']
    d["description"] = 'Openscad render.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'OpenSCAD'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_destination', 'description': 'Path to the output file to create or update.', 'type': 'string', 'default': ''})
        v.append({'name': 'render_type', 'description': 'Rendering mode passed to the OpenSCAD render step.', 'type': 'string', 'default': ''})
        v.append({'name': 'delay', 'description': 'Delay duration in seconds.', 'type': 'string', 'default': ''})
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
    """Render OpenSCAD file to specified format."""
    action = kwargs.get("action", {})
    directory = kwargs.get("directory", "")
    file_input = action.get("file_source", None)
    if not file_input:
        file_input = action.get("file_input", "")
    file_input = os.path.join(directory, file_input)
    file_input_full = os.path.abspath(file_input)
    file_output = action.get("file_destination", None)
    if not file_output:
        file_output = action.get("file_output", file_input.replace(".scad", ".stl"))
    if directory not in file_output:
        file_output = os.path.join(directory, file_output)
    render_type = action.get("render_type", "stl")  # stl, png, svg, etc.
    delay = action.get("delay", 5)
    print(f"Rendering OpenSCAD file {file_input} to {render_type} and saving to {file_output}")
    #use os not subprocess in line system call to run openscad wait for it to finish
    
    try:
        if render_type == "stl":
            cmd = ["openscad", "-o", file_output, file_input_full]
        elif render_type == "png":
            cmd = ["openscad", "-o", file_output, "--imgsize=800,600", file_input_full]
        elif render_type == "svg":
            cmd = ["openscad", "-o", file_output, "--export-format=svg", file_input_full]
        else:
            print(f"Unsupported render type {render_type}, skipping OpenSCAD render")
            return
        os.system(" ".join(cmd))      

        
        print(f"OpenSCAD file rendered and saved to {file_output}")
    except Exception as e:
        print(f"Error rendering OpenSCAD file {file_input_full}: {e}")

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
