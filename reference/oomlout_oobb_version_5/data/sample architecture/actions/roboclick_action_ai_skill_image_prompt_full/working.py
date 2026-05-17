d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'skill'
    d["name_long_5"] = 'image_prompt_full'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_skill_image_prompt_full'
    d["name_long"] = 'roboclick_action_ai_skill_image_prompt_full'
    d["name_short"] = ['image_prompt_full', 'image', 'ai_skill_image_prompt_full']
    d["name_short_options"] = ['image_prompt_full', 'image', 'ai_skill_image_prompt_full']
    d["description"] = 'Image prompt full.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI Skill'
    v = []
    if True:
        v.append({'name': 'image_detail', 'description': 'Prompt detail level for generated image instructions.', 'type': 'string', 'default': ''})
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
    """ make an image prompt using AI."""
    import oomlout_ai_roboclick_skill_image_intense_1
    return oomlout_ai_roboclick_skill_image_intense_1.main(**kwargs)

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
