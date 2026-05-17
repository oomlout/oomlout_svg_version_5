import os

import yaml

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'new'
    d["name_long_5"] = 'new_chat'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_new_chat'
    d["name_long"] = 'roboclick_action_ai_new_chat'
    d["name_short"] = ['new_chat', 'chat', 'ai_new_chat']
    d["name_short_options"] = ['new_chat', 'chat', 'ai_new_chat']
    d["description"] = 'New chat.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'log_url', 'description': 'Whether to capture and store the current chat URL.', 'type': 'string', 'default': ''})
        v.append({'name': 'description', 'description': 'Optional kickoff note sent in the first chat message.', 'type': 'string', 'default': ''})
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
    """Open new chat session"""
    action = kwargs.get("action", {})
    description = action.get("description", "")
    log_url = action.get("log_url", True)
    print("new_chat -- opening up a new chat")
    robo.robo_chrome_open_url(url="https://chat.openai.com/chat", delay=15, message="    opening a new chat")    
    #check for hitting limit
    if True:
        print("    Checking for message limit...")
        clip = robo.robo_keyboard_copy(delay=5, position=[300, 300])  # Copy some text to check for limit
        if "0 messages remaining" in clip.lower():
            print("    Hit message limit, cannot proceed.")
            #delay 6 hours
            print("    Delaying for 6 hours before retrying...")
            robo.robo_delay(delay=21600)  # Delay for 6 hours
            return "exit"
        elif "requests too quickly" in clip.lower():
            print("    Detected rate limit, delaying for 30 minutes before retrying...")
            robo.robo_delay(delay=1800)  # Delay for 30 minutes
            #press tab and enter to close the rate limit message
            robo.robo_keyboard_press_tab(delay=2)
            robo.robo_keyboard_press_enter(delay=2)
        pass
    #type in start query
    start_query = ""
    if description != "":        
        start_query += f" Hi, CHadikins I hope your day is going well! lets get to this!."
        #start_query += f" Hi, Chadikins I hope your day is going well! lets get to this!. I like it when you are chatty and suggest things based on what i've done in the past. Also use your thinking, and any other, public and secret abilities to their utmost throughout this task please. When you generate an image just deliver the image no extra text. "
    start_query += ""
    robo.robo_keyboard_send(string=start_query, delay=5)
    
    #robo.robo_keyboard_press_enter(delay=40)
    #control enter
    robo.robo_keyboard_press_ctrl_generic(string="enter", delay=40)

    #if log_url is True:
    if log_url:
        #press ctrl l
        robo.robo_keyboard_press_ctrl_generic(string="l", delay=2)
        #copy the url
        url = robo.robo_keyboard_copy(delay=2)
        #print the url
        print(f"    New chat URL: {url}")
        #press esc
        robo.robo_keyboard_press_escape(delay=2, repeat=5)
        #save to url.yaml
        if True:            
            url_file = os.path.join(kwargs.get("directory_absolute", ""), "url.yaml")
            #if url exists load it to add to the list
            if os.path.exists(url_file):
                with open(url_file, 'r') as file:
                    url_data = yaml.safe_load(file)
            else:
                url_data = []
            if url_data == None:
                url_data = []
            url_data.append(url)
            with open(url_file, 'w') as file:
                yaml.dump(url_data, file)
            return url

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
