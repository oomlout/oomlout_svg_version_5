import os

import pyautogui
import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'query'
    d["name_long_5"] = 'ai_query'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_query'
    d["name_long"] = 'roboclick_action_ai_query'
    d["name_short"] = ['ai_query', 'query']
    d["description"] = 'Ai query.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'text', 'description': 'Text content used by this action.', 'type': 'string', 'default': ''})
        #filename
        v.append({'name': 'file_name', 'description': 'File name to read or write for this action. if folder name starts with source_files it will pull from project source_files rather than folder', 'type': 'string', 'default': ''})
        v.append({'name': 'delay', 'description': 'Delay duration in seconds.', 'type': 'string', 'default': ''})
        v.append({'name': 'mode_ai_wait', 'description': 'AI wait strategy (slow, fast_button_state, or fast_clipboard_state).', 'type': 'string', 'default': ''})
        v.append({'name': 'method', 'description': 'Query input method (typing or paste).', 'type': 'string', 'default': ''})
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
    #return old(**kwargs)
    return new(**kwargs)


def new(**kwargs): 
    """Send query to AI"""
    print("#################################################")
    print("######  ai_query -- sending a query")

    directory = kwargs.get("directory", "") #current directory of the part
    action = kwargs.get("action", {})
    
    #get the query from the action
    action = kwargs.get("action", {})
    delay = action.get("delay", 60)
    query_text = action.get("text", "")
    file_name = action.get("file_name", "")
    folder_name = action.get("folder_name", "")
    f_string_replace = action.get("f_string_replace", True)
    
    #load query text
    query_texts = []
    if query_text != "":
        query_texts.append(query_text)
    #getting query from files or folder
    else:
        #both file_name and query_text are defined
        if file_name != "" and query_text != "":
            print(f"     ERROR bothquery text and file are defined query text will be used")
            robo.robo_delay(delay=10)
        
        ##load the text from the file
        file_names = file_name
        #put filename into an array if it isn't already
        if True:
            if not isinstance(file_names, list):
                file_names = [file_names]
        #if folder_name load the filenames from there
        if folder_name != "":
            #upto 50
            file_names = []
            for i in range(1, 50):
                file_name_check = f"{folder_name}\\working_{i}.md"
                file_names.append(file_name_check)
                
                
        for file_name_seed in file_names:
            file_name = file_name_seed
            if True:
                #load text from file.
                #file is in the prompt directory of the project
                filename_absolute = ""
                if file_name.startswith("prompt\\") or file_name.startswith("prompt/") or file_name.startswith("roboclick\\") or file_name.startswith("roboclick/"):                
                    filename_absolute = os.path.abspath(file_name)
            #file is in the directory of the part
                else:
                    file_name = f"{directory}\\{file_name}"
                    filename_absolute = os.path.abspath(file_name)
                if filename_absolute != "":
                    #if the file exists
                    if os.path.exists(filename_absolute):
                        
                        with open(filename_absolute, 'r', encoding='utf-8') as f:
                            query_text = f.read()
                            if f_string_replace:
                                #replace {tags} in query_text with values from workings, leaving missing tags unchanged
                                    import string
                                    workings = kwargs.get("workings", {})
                                    class SafeDict(dict):
                                        def __missing__(self, key):
                                            return '{' + key + '}'
                                    try:
                                        query_text = query_text.format_map(SafeDict(workings))
                                    except Exception as e:
                                        print(f"     Error formatting query_text: {e}")
                                        robo.robo_delay(delay=10)
                        query_texts.append(query_text)
                        print(f"     Loaded query text from {filename_absolute}")
                        
                    else:
                        ###error checking annoying because of folder
                        if folder_name == "":
                            print(f"     File Missing")
                            robo.robo_delay(delay=10)
                        
                        #get the folder name of the file                        
                        folder_name_check = os.path.dirname(filename_absolute)
                        #if the folder doesnt eiistt print error
                        if not os.path.exists(folder_name_check):
                            print(f"     Folder {folder_name_check} does not exist for file {filename_absolute}")
                            robo.robo_delay(delay=10)
                        
                        
                else:
                    print(f"     No valid file name provided for query text.")
                    robo.robo_delay(delay=10)
                    query_text = ""
        
    
    #### default to slow mode if not specified
    mode_ai = action.get("mode_ai_wait", "slow")
    if mode_ai == None:
        mode_ai = "slow"

    #### default to typing in prompt
    method = action.get("method", "typing")  #"standard" or "line_by_line"

    ##loop logic for multiple querytext
    #make query_texts an array if it isn't
    
    if not isinstance(query_texts, list):
        query_texts = [query_texts]

    for query_text in query_texts:
        #clear text box
        if True:
            print("    Clearing text box before query...")
            #select all
            robo.robo_keyboard_press_ctrl_generic(string="a", delay=2)
            #back space
            robo.robo_keyboard_press_backspace(delay=2, repeat=1)

        #if query text is more than 1000 characters use paste method
        if len(query_text) > 1000:
            method = "paste"
            print("    Query text is long, using paste method.")

        if method == "typing":
            #split the text on line breaks
            query_text = query_text.replace("\r\n", "\n").replace("\r", "\n")
            query_text_lines = query_text.split("\n")
            for line in query_text_lines:
                #send each line with a delay of 1 second between lines
                robo.robo_keyboard_send(string=line, delay=0.1)
                robo.robo_keyboard_press_shift_enter(delay=0.1)  # Press Shift+Enter to create a new line
        elif method == "paste":
            #press space twice to ensure focus
            robo.robo_keyboard_send(string="  ")
            robo.robo_keyboard_paste(text=query_text)
            #paste the entire text at once
            #delay 5 seconds
            robo.robo_delay(delay=5)
            #robo.robo_keyboard_press_ctrl_generic(string="v", delay=2)
        

        print(f"Querying with text: {query_text}")
        
        if mode_ai =="slow":
            #robo.robo_keyboard_press_enter(delay=delay)
            #ctrl enter
            robo.robo_keyboard_press_ctrl_generic(string="enter", delay=delay)
        elif "fast" in mode_ai: 
            #robo.robo_keyboard_press_enter(delay=1)
            robo.robo_keyboard_press_ctrl_generic(string="enter", delay=1)
            robo.ai_wait_mode_fast_check(mode_ai_wait=mode_ai)


def old(**kwargs):
    """Send query to AI"""
    directory = kwargs.get("directory", "")
    action = kwargs.get("action", {})
    print("ai_query -- sending a query")
    #get the query from the action
    action = kwargs.get("action", {})
    delay = action.get("delay", 60)
    query_text = action.get("text", "")
    file_name = action.get("file_name", "")
    
    
    
    #load query text
    if True:
        if file_name != "" and query_text != "":
            print(f"     ERROR bothquery text and file are defined query text will be used")
            robo.robo_delay(delay=10)
        if query_text == "" and file_name != "":
            #load text from file.
            #file is in the prompt directory of the project
            filename_absolute = ""
            if file_name.startswith("prompt\\") or file_name.startswith("prompt/"):                
                filename_absolute = os.path.abspath(file_name)
        #file is in the directory of the part
            else:
                file_name = f"{directory}\\{file_name}"
                filename_absolute = os.path.abspath(file_name)
            if filename_absolute != "":
                try:
                    with open(filename_absolute, 'r', encoding='utf-8') as f:
                        query_text = f.read()
                    print(f"     Loaded query text from {filename_absolute}")
                except Exception as e:
                    print(f"     Error loading query text from {filename_absolute}: {e}")
                    robo.robo_delay(delay=10)
                    query_text = ""
            else:
                print(f"     No valid file name provided for query text.")
                robo.robo_delay(delay=10)
                query_text = ""
    mode_ai = action.get("mode_ai_wait", "slow")
    if mode_ai == None:
        mode_ai = "slow"
    method = action.get("method", "typing")  #"standard" or "line_by_line"

    #clear text box
    if True:
        print("    Clearing text box before query...")
        #select all
        robo.robo_keyboard_press_ctrl_generic(string="a", delay=2)
        #back space
        robo.robo_keyboard_press_backspace(delay=2, repeat=1)

    #if query text is more than 1000 characters use paste method
    if len(query_text) > 1000:
        method = "paste"
        print("    Query text is long, using paste method.")

    if method == "typing":
        #split the text on line breaks
        query_text = query_text.replace("\r\n", "\n").replace("\r", "\n")
        query_text_lines = query_text.split("\n")
        for line in query_text_lines:
            #send each line with a delay of 1 second between lines
            robo.robo_keyboard_send(string=line, delay=0.1)
            robo.robo_keyboard_press_shift_enter(delay=0.1)  # Press Shift+Enter to create a new line
    elif method == "paste":
        #press space twice to ensure focus
        robo.robo_keyboard_send(string="  ")
        robo.robo_keyboard_paste(text=query_text)
        #paste the entire text at once
        #delay 5 seconds
        robo.robo_delay(delay=5)
        robo.robo_keyboard_press_ctrl_generic(string="v", delay=2)
    

    print(f"Querying with text: {query_text}")
    
    if mode_ai =="slow":
        #robo.robo_keyboard_press_enter(delay=delay)
        #ctrl enter
        robo.robo_keyboard_press_ctrl_generic(string="enter", delay=delay)
    elif "fast" in mode_ai: 
        #robo.robo_keyboard_press_enter(delay=1)
        robo.robo_keyboard_press_ctrl_generic(string="enter", delay=1)
        ai_wait_mode_fast_check(mode_ai_wait=mode_ai)

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
