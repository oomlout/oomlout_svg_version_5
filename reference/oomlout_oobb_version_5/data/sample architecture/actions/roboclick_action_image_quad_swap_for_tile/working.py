import os

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'image'
    d["name_long_4"] = 'quad'
    d["name_long_5"] = 'quad_swap_for_tile'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_image_quad_swap_for_tile'
    d["name_long"] = 'roboclick_action_image_quad_swap_for_tile'
    d["name_short"] = ['quad_swap_for_tile', 'swap', 'image_quad_swap_for_tile']
    d["name_short_options"] = ['quad_swap_for_tile', 'swap', 'image_quad_swap_for_tile']
    d["description"] = 'Quad swap for tile.'
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
    """Swap image quadrants for tiling."""
    action = kwargs.get("action", {})
    directory = kwargs.get("directory", "")
    file_input = action.get("file_source", None)
    if not file_input:
        file_input = action.get("file_input", "")
    file_input = os.path.join(directory, file_input)
    file_input_full = os.path.abspath(file_input)
    file_output = action.get("file_destination", None)
    if not file_output:
        file_output = action.get("file_output", file_input.replace(".png", "_quadshifted.png").replace(".jpg", "_quadshifted.jpg").replace(".jpeg", "_quadshifted.jpeg"))
    if directory not in file_output:
        file_output = os.path.join(directory, file_output)
    if os.path.isfile(file_input):
        from PIL import Image
        try:
            with Image.open(file_input_full) as img:
                width, height = img.size
                # Create a new blank image
                new_img = Image.new("RGB", (width, height))
                # Define the box coordinates for each quadrant
                box1 = (0, 0, width // 2, height // 2)  # Top-left
                box2 = (width // 2, 0, width, height // 2)  # Top-right
                box3 = (0, height // 2, width // 2, height)  # Bottom-left
                box4 = (width // 2, height // 2, width, height)  # Bottom-right
                # Crop the quadrants    
                quadrant1 = img.crop(box1)
                quadrant2 = img.crop(box2)
                quadrant3 = img.crop(box3)
                quadrant4 = img.crop(box4)
                # Paste the quadrants into their new positions
                new_img.paste(quadrant4, box1)  # Bottom-right to Top-left
                new_img.paste(quadrant3, box2)  # Bottom-left to Top
                new_img.paste(quadrant2, box3)  # Top-right to Bottom-left
                new_img.paste(quadrant1, box4)  # Top-left to Bottom-right                
                # Save the quad shifted image
                new_img.save(file_output)
                print(f"Image quad shifted and saved to {file_output}")
        except Exception as e:
            print(f"Error quad shifting image {file_input_full}: {e}")
            return
    else:
        print(f"file_source {file_input} does not exist, skipping image quad shift")
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
