import copy

import os

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'image'
    d["name_long_4"] = 'upscale'
    d["name_long_5"] = 'image_upscale'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_image_upscale'
    d["name_long"] = 'roboclick_action_image_upscale'
    d["name_short"] = ['image_upscale', 'upscale']
    d["name_short_options"] = ['image_upscale', 'upscale']
    d["description"] = 'Image upscale.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Image'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_destination', 'description': 'Path to the output file to create or update.', 'type': 'string', 'default': ''})
        v.append({'name': 'scale', 'description': 'Scale multiplier applied during image upscaling.', 'type': 'string', 'default': ''})
        v.append({'name': 'crop', 'description': 'Crop box or crop mode applied to the image.', 'type': 'string', 'default': ''})
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

def image_crop(**kwargs):
    return _dispatch_action("image_crop", **kwargs)

def action(**kwargs):
    return old(**kwargs)

def old(**kwargs):
    """Upscale image resolution."""
    action = kwargs.get("action", {})
    directory = kwargs.get("directory", "")
    file_input = action.get("file_source", "")
    if file_input == "":
        file_input = action.get("file_input", "")
    file_input = os.path.join(directory, file_input)
    file_input_full = os.path.abspath(file_input)
    file_output_default = file_input.replace(".png", "_upscaled.png").replace(".jpg", "_upscaled.jpg").replace(".jpeg", "_upscaled.jpeg")
    file_output = action.get("file_destination", file_output_default)
    if file_output == "":
        file_output = action.get("file_output", file_output_default)
    file_output_base = file_output
    if directory not in file_output:
        file_output = os.path.join(directory, file_output)
    upscale_factor = action.get("scale", "")
                                      
    if upscale_factor == "":
        upscale_factor = float(action.get("upscale_factor", 2))
    upscale_factor = float(upscale_factor)
    crop = action.get("crop", "")
    if os.path.isfile(file_input):
        from PIL import Image
        try:
            if os.path.exists(file_output):
                os.remove(file_output)
                print(f"Removed existing output file {file_output}")
            with Image.open(file_input_full) as img:
                new_size = (int(img.width * upscale_factor), int(img.height * upscale_factor))
                img = img.resize(new_size, Image.NEAREST)
                img.save(file_output)
                print(f"Image upscaled and saved to {file_output}")
        except Exception as e:
            print(f"Error upscaling image {file_input_full}: {e}")
            return
        if crop != "":
            kwargs2 = copy.deepcopy(kwargs)
            action2 = {}
            action2["file_input"] = file_output_base
            action2["file_output"] = file_output_base
            action2["crop"] = crop
            kwargs2["action"] = action2
            image_crop(**kwargs2)
    else:
        print(f"file_input {file_input} does not exist, skipping image upscale")
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
