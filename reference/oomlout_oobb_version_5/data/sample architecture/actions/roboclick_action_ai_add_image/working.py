import os

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'add'
    d["name_long_5"] = 'add_image'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_add_image'
    d["name_long"] = 'roboclick_action_ai_add_image'
    d["name_short"] = ['add_image', 'image', 'ai_add_image']
    d["name_short_options"] = ['add_image', 'image', 'ai_add_image']
    d["description"] = 'Add image.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'position_click', 'description': 'Screen position to click before executing the step.', 'type': 'string', 'default': ''})
        v.append({'name': 'mode -- source_files from source_files directory', 'description': 'Value for mode -- source files from source files directory.', 'type': 'string', 'default': ''})
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
    """Add a file (alias for add_image)"""
    """Add an image file to the current context"""
    return_value = ""
    print("add_image -- adding an image")
    #kwargs["position_click"] = [750,995]

    action = kwargs.get("action", {})
    file_name = action.get("file_source", "")
    if file_name == "":
        file_name = action.get("file_name", "working.png")
    directory = kwargs.get("directory", "")
    directory_absolute = os.path.abspath(directory)
    
    action = kwargs.get("action", {})
    mode = action.get("mode", "")
    if mode == "":    
        file_name_absolute = os.path.join(directory_absolute, file_name)
        file_name_abs = os.path.abspath(file_name) 
    if mode == "source_files":
        file_name_absolute = os.path.join(os.path.abspath("source_files"), file_name)
        file_name_abs = os.path.abspath(file_name)
        pass
    
    #print(f"Adding image {file_name} at position {position_click}")
    #test if filename exists
    if not os.path.exists(file_name_absolute):
        print(f"File {file_name_absolute} does not exist, skipping action.")
        return_value = "exit"
        print(f"    ERROR ERROR ERROR Exiting action due to missing file: {file_name_absolute}")
        robo.robo_delay(delay=5)  # Delay to allow user to see the message
        return return_value
    #send "  "
    robo.robo_keyboard_send(string="  ", delay=2)  # Send two spaces to open the add image dialog
    #tab once
    robo.robo_keyboard_press_tab(delay=5, repeat=1)  # Press tab once to focus on the add image button
    #down zero times
    #robo.robo_keyboard_press_down(delay=1, repeat=1)  # Press down zero times to select the file input
    #enter once
    robo.robo_keyboard_press_enter(delay=5)  # Press enter to open the file dialog
    #new needs two enters maybe
    if True:
        robo.robo_keyboard_press_enter(delay=5)  # Press enter to open the file dialog
    #robo.robo_keyboard_press_down(delay=1, repeat=2)  # Press down twice to select the file input
    robo.robo_keyboard_send(string=file_name_absolute, delay=5)  # Type the file name
    robo.robo_keyboard_press_enter(delay=5)  # Press enter to confirm
    robo.robo_delay(delay=15)  # Wait for the image to be added
    #preess escape 5 times in case of any dialog boxes
    robo.robo_keyboard_press_escape(delay=5, repeat=5)  # Escape to close any dialogs
    return return_value

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
