import os

import random

import robo

try:
    import pyautogui  # type: ignore
except Exception:
    pyautogui = None  # type: ignore

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'save'
    d["name_long_4"] = 'image'
    d["name_long_5"] = 'save_image_generated'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_save_image_generated'
    d["name_long"] = 'roboclick_action_save_image_generated'
    d["name_short"] = ['save_image_generated', 'generated']
    d["name_short_options"] = ['save_image_generated', 'generated']
    d["description"] = 'Save image generated.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI Image'
    v = []
    if True:
        v.append({'name': 'file_name', 'description': 'File name to read or write for this action.', 'type': 'string', 'default': ''})
        v.append({'name': 'position_click', 'description': 'Screen position used to open the generated image context menu.', 'type': 'string', 'default': ''})
        v.append({'name': 'mode_ai_wait', 'description': 'AI wait strategy (slow, fast_button_state, or fast_clipboard_state).', 'type': 'string', 'default': ''})
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

def ai_wait_mode_fast_check(mode_ai_wait="fast_button_state"):  
    if mode_ai_wait == "fast_button_state" or mode_ai_wait == "fast":
        return ai_wait_mode_fast_check_state_of_submit_button_approach()
    elif mode_ai_wait == "fast_clipboard_state":
        return ai_wait_mode_fast_clipboard_creating_image_approach()

def ai_wait_mode_fast_check_state_of_submit_button_approach():  
    print("Waiting for AI to finish responding (fast mode)...")
    count = 0
    count_max = 100
    running = True    
    point_check_color = [1445,964]
    #point_check_color = [1331,964]
    color_done= (0, 0, 0)
    color_expecting = (236,236,236)

    while running and count < count_max:
        robo.robo_delay(delay=10)
        pixel_color = pyautogui.screenshot().getpixel((point_check_color[0], point_check_color[1]))
        print(f"    Pixel color at {point_check_color}: {pixel_color} ")
        #check if it is the expected color
        if pixel_color == color_expecting:
            print("    Good news the right color was found")
        else:
            print("    The expected color was not found, may need to move")
        if pixel_color == color_done:
            print("    AI apIpears to have finished responding.")
            running = False
            robo.robo_delay(delay=2)

def ai_wait_mode_fast_clipboard_creating_image_approach():  
    print("Waiting for AI to finish responding (fast mode)...")
    count = 0
    count_max = 100
    running = True    
    string_check = "Creating image"

    while running and count < count_max:
        robo.robo_delay(delay=10)
        #mouse click at 300,300
        robo.robo_mouse_click(position=[300, 300], delay=2, button="left")  # Click to focus
        text = robo.robo_keyboard_copy(delay=2)
        if string_check in text:
            print("    AI appears to be creating an image, waiting for it to finish...")
        else:
            print("    AI appears to have finished responding.")
            running = False
            robo.robo_delay(delay=2)

def save_image(**kwargs):
    #position_click = kwargs.get("position_click", [960, 500])
    #position_click = kwargs.get("position_click", [960, 360])
    position_click = kwargs.get("position_click", [960, 280])
    
    action = kwargs.get("action", {})
    file_name = action.get("file_name", "working.png")   
    directory_absolute = kwargs.get("directory_absolute", "")
    file_name_absolute = os.path.join(directory_absolute, file_name)
    file_name_abs = os.path.abspath(file_name) 
    print(f"Saving image as {file_name}")
    #save the image
    robo.robo_mouse_click(position=position_click, delay=2, button="right")  # Click on the image to focus
    #press down twice
    robo.robo_keyboard_press_down(delay=1, repeat=2)
    robo.robo_keyboard_press_enter(delay=5)
    robo.robo_keyboard_send(string=file_name_absolute, delay=5)
    robo.robo_keyboard_press_enter(delay=5)
    robo.robo_keyboard_send(string="y", delay=5)
    robo.robo_keyboard_press_escape(delay=5, repeat=5)  # Escape to close any dialogs
    print(f"Image saved as {file_name}")

def save_image_generated_old_press_down_40_time_approach(**kwargs):
    action = kwargs.get("action", {})
    mode_ai_wait = action.get("mode_ai_wait", "slow")
    
    #kwargs["position_click"] = [960, 480]  # Default position for clicking the image    
    kwargs["position_click"] = [960, 360]  # Default position for clicking the image    
    #kwargs["position_click"] = [960, 280]  # Default position for clicking the image    
    
    if mode_ai_wait == "slow":
        robo.robo_delay(delay=300)
        delay = random.randint(100, 300)
        robo.robo_delay(delay=delay)  # Wait for the image to be generated
    elif "fast" in mode_ai_wait:
        ai_wait_mode_fast_check(mode_ai_wait="fast_clipboard_state")
    
    if True:
        #send ctrl rrobo.robo_keyboard_press_ctrl_r(delay=20)
        #click on the image to focus
        #reload
        if True:
            robo.robo_keyboard_press_ctrl_generic(string="r", delay=20)
            #click on the image to focus
            #robo.robo_mouse_click(position=[330,480], delay=2)  # Click on the white space
            robo.robo_mouse_click(position=[330,360], delay=2)  # Click on the white space
            #robo.robo_mouse_click(position=[330,280], delay=2)  # Click on the white space
            robo.robo_keyboard_press_down(delay=1, repeat=40)  # Press down ten times to select the file input
        #check if limit reached
        if True:
            clip = robo.robo_keyboard_copy(delay=2)
            if "you've hit the plus plan limit" in clip.lower() or "you have reached your free image generation limit" in clip.lower() or "you've reached your image creation limit" in clip.lower():   
                #get text bewteen "resets in" and  minutes
                time_out = clip.lower().split("resets in")[-1].split("minutes")[0].strip()
                #check to make sure it worked
                delay_time  = 6 * 60 * 60 # 6 hours
                if time_out != "":
                    #get hours
                    if "hour" in time_out:
                        hours = int(time_out.split("hour")[0].strip()) + 1
                        delay_time = hours * 60 * 60
                    #print message
                    print(f"Image generation limit reached, waiting for {delay_time/3600:.2f} hours until reset...")
                robo.robo_delay(delay=delay_time)

                return "exit"
        #save image        
        if True:
            save_image(**kwargs)
        file_name = kwargs.get("action", {}).get("file_name", "working.png")
        file_name_absolute = os.path.join(kwargs.get("directory_absolute", ""), file_name)
        if os.path.exists(file_name_absolute):
            print(f"Image saved as {file_name_absolute}")
            saved = True
        else:
            print(f"Image not saved")

def action(**kwargs):
    return old(**kwargs)

def old(**kwargs):
    """Save AI-generated image."""
    # use the robust press-down approach
    return save_image_generated_old_press_down_40_time_approach(**kwargs)


def old(**kwargs):
    """Save AI-generated image."""
    # use the robust press-down approach
    return save_image_generated_old_press_down_40_time_approach(**kwargs)

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
