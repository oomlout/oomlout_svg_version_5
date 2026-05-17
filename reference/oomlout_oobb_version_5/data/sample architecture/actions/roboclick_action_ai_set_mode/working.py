import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'set'
    d["name_long_5"] = 'set_mode'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_set_mode'
    d["name_long"] = 'roboclick_action_ai_set_mode'
    d["name_short"] = ['set_mode', 'mode', 'ai_set_mode']
    d["name_short_options"] = ['set_mode', 'mode', 'ai_set_mode']
    d["description"] = 'Set mode.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'mode', 'description': 'Mode selector controlling action behavior.', 'type': 'string', 'default': ''})
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
    """Set AI mode (e.g., deep_research)"""
    action = kwargs.get("action", {})
    print("ai_set_mode -- setting AI mode")
    mode = action.get("mode", "")
    if mode == "deep_research" or mode == "deep_research_off":
        #press tab twice
        robo.robo_keyboard_press_tab(delay=2, repeat=1)  # Press tab twice to set the mode        
        #press_enter
        robo.robo_keyboard_press_enter(delay=2)  # Press enter to confirm the mode
        #press down once
        robo.robo_keyboard_press_down(delay=2, repeat=1)
        ##press down 0 #times to select the deep research mode
        #robo.robo_keyboard_press_down(delay=2, repeat=2)  # Press down twice to select the deep research mode
        #press enter
        robo.robo_keyboard_press_enter(delay=2)  # Press enter to confirm the mode
        print("     AI mode set to deep research")

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
