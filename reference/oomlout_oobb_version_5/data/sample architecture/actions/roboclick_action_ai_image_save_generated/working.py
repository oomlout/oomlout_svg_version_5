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

def action(**kwargs):
    return new(**kwargs)

def new(**kwargs):
    action = kwargs.get("action", {})
    mode_ai_wait = action.get("mode_ai_wait", "slow")
    
    if mode_ai_wait == "slow":
        robo.robo_delay(delay=300)
        delay = random.randint(100, 300)
        robo.robo_delay(delay=delay)  # Wait for the image to be generated
    elif "fast" in mode_ai_wait:
        robo.ai_wait_mode_fast_check(mode_ai_wait="fast_clipboard_state")
    
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
            robo.ai_save_image(**kwargs)
        file_name = kwargs.get("action", {}).get("file_name", "working.png")
        file_name_absolute = os.path.join(kwargs.get("directory_absolute", ""), file_name)
        if os.path.exists(file_name_absolute):
            print(f"Image saved as {file_name_absolute}")
            saved = True
        else:
            print(f"Image not saved")


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
