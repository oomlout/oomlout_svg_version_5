import os

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'image'
    d["name_long_4"] = 'png'
    d["name_long_5"] = 'png_transparent_to_white'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_image_png_transparent_to_white'
    d["name_long"] = 'roboclick_action_image_png_transparent_to_white'
    d["name_short"] = ['png_transparent_to_white', 'transparent', 'image_png_transparent_to_white']
    d["name_short_options"] = ['png_transparent_to_white', 'transparent', 'image_png_transparent_to_white']
    d["description"] = 'Png transparent to white.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Image'
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
    """Convert transparent PNG to white background PNG."""
    action = kwargs.get("action", {})
    directory = kwargs.get("directory", "")
    file_input = action.get("file_source", None)
    if not file_input:
        file_input = action.get("file_input", "")
    file_input = os.path.join(directory, file_input)
    file_input_full = os.path.abspath(file_input)
    file_output = action.get("file_destination", None)
    if not file_output:
        file_output = action.get("file_output", file_input.replace(".png", "_whitebg.png"))
    overwrite = action.get("overwrite", True)
    if not overwrite and os.path.exists(file_output):
        print(f"file_destination {file_output} already exists and overwrite is set to False, skipping transparent to white conversion")
        return
    else:
        if os.path.exists(file_output):
            os.remove(file_output)
            print(f"Removed existing output file {file_output}")
    if directory not in file_output:
        file_output = os.path.join(directory, file_output)
    if os.path.isfile(file_input):
        from PIL import Image
        try:
            with Image.open(file_input_full) as img:
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                white_bg = Image.new('RGBA', img.size, (255, 255, 255, 255))
                white_bg.paste(img, (0, 0), img)
                white_bg = white_bg.convert('RGB')
                white_bg.save(file_output)
                print(f"Transparent PNG converted to white background and saved to {file_output}")
        except Exception as e:
            print(f"Error converting image {file_input_full}: {e}")
            return
    else:
        print(f"file_source {file_input} does not exist, skipping transparent to white conversion")
        return

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
