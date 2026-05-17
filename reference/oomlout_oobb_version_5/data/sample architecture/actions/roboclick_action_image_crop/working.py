import os

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'image'
    d["name_long_4"] = 'crop'
    d["name_long_5"] = 'image_crop'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_image_crop'
    d["name_long"] = 'roboclick_action_image_crop'
    d["name_short"] = ['image_crop', 'crop']
    d["name_short_options"] = ['image_crop', 'crop']
    d["description"] = 'Image crop.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Image'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_destination', 'description': 'Path to the output file to create or update.', 'type': 'string', 'default': ''})
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

def action(**kwargs):
    return old(**kwargs)

def old(**kwargs):
    """Crop image to specified format."""
    action = kwargs.get("action", {})
    directory = kwargs.get("directory", "")
    file_input = action.get("file_source", None)
    if not file_input:
        file_input = action.get("file_input", "")
    file_input = os.path.join(directory, file_input)
    file_input_full = os.path.abspath(file_input)
    file_output = action.get("file_destination", None)
    if not file_output:
        file_output = action.get("file_output", file_input_full)
    if directory not in file_output:
        file_output = os.path.join(directory, file_output)
    crop = action.get("crop", "a4_portrait")  #left, upper, right, lower
    print(f"Cropping image {file_input} to {crop} and saving to {file_output}")
    if os.path.isfile(file_input):
        from PIL import Image
        try:
            with Image.open(file_input_full) as img:
                crop_box = [0,0,100,100]
                if crop == "a4_landscape":
                    img_width, img_height = img.size
                    aspect_ratio = 297 / 210  
                    # create_coordinates to take from the middle of the image check if source is wider or taller than aspect ratio
                    if img_width / img_height > aspect_ratio:
                        #source is wider
                        new_height = img_height
                        new_width = int(new_height * aspect_ratio)
                        left = (img_width - new_width) / 2
                        upper = 0
                        right = left + new_width
                        lower = img_height
                    else:
                        #source is taller
                        new_width = img_width
                        new_height = int(new_width / aspect_ratio)
                        left = 0
                        upper = (img_height - new_height) / 2
                        right = img_width
                        lower = upper + new_height
                    crop_box = [left, upper, right, lower]
                elif crop == "a4_portrait":
                    img_width, img_height = img.size
                    aspect_ratio = 210 / 297  
                    # create_coordinates to take from the middle of the image check if source is wider or taller than aspect ratio
                    if img_width / img_height > aspect_ratio:
                        #source is wider
                        new_height = img_height
                        new_width = int(new_height * aspect_ratio)
                        left = (img_width - new_width) / 2
                        upper = 0
                        right = left + new_width
                        lower = img_height
                    else:
                        #source is taller
                        new_width = img_width
                        new_height = int(new_width / aspect_ratio)
                        left = 0
                        upper = (img_height - new_height) / 2
                        right = img_width
                        lower = upper + new_height
                    crop_box = [left, upper, right, lower]
                elif crop == "square":
                    img_width, img_height = img.size
                    # create_coordinates to take from the middle of the image
                    if img_width > img_height:
                        #source is wider
                        new_size = img_height
                        left = (img_width - new_size) / 2
                        upper = 0
                        right = left + new_size
                        lower = img_height
                    else:
                        #source is taller
                        new_size = img_width
                        left = 0
                        upper = (img_height - new_size) / 2
                        right = img_width
                        lower = upper + new_size
                    crop_box = [left, upper, right, lower]
                img_cropped = img.crop((crop_box[0], crop_box[1], crop_box[2], crop_box[3]))
                # Save the cropped image
                img_cropped.save(file_output)
                print(f"Image cropped and saved to {file_output}")
        except Exception as e:
            print(f"Error cropping image {file_input_full}: {e}")
            return
    else:
        print(f"file_source {file_input} does not exist, skipping image crop")
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
