import oomlout_roboclick
import copy

d = {}


def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'skill'
    d["name_long_5"] = 'image_laser_cut_logo_full'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_skill_image_laser_cut_logo_full'
    d["name_long"] = 'roboclick_action_ai_skill_image_laser_cut_logo_full'
    d["name_short"] = ['image_laser_cut_logo_full', 'image', 'ai_skill_image_laser_cut_logo_full']
    d["name_short_options"] = ['image_laser_cut_logo_full', 'image', 'ai_skill_image_laser_cut_logo_full']
    d["description"] = 'Image laser cut logo full.'
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
    """ make a laser cut logo image using AI."""
    action = kwargs.get("action", "")
    mode_ai_wait = action.get("mode_ai_wait", None)
    image_detail = action.get("image_detail", "colorful bubble letters")
    file_destination = action.get("file_destination", "")
    if file_destination == "":
        #try file_name
        file_destination = action.get("file_name", "")
        if file_destination == "":
            #try filename
            file_destination = action.get("filename", "initial_generated_test.png")
    

    action = {}
    kwargs2 = copy.deepcopy(kwargs)
    action["command"] = "ai_new_chat"
    action["description"] = f"making a icon logo for {image_detail} using AI"
    kwargs2["action"] = copy.deepcopy(action)
    oomlout_roboclick.run_single_action(**kwargs2)

    action = {}
    action["command"] = "ai_query"
    prompt = f"""
Create a prompt for generating a 1-colour (black on white) chibi-style
mascot illustration designed for a 40x40 mm thermal label that visually
represents a given recipe name (recipe_name). The artwork should feature
one central cute anthropomorphic mascot themed to the recipe (for example
a smiling sausage, happy bowl of curry, or cheerful casserole pot) with
up to two simple surrounding icons that fit the meal's personality (such
as a heart puff, herb sprig, spoon, bowl, or local motif). Use pure black
on white only with no grey, shading, gradients, or text. Keep bold linework
(outer 3.5-4.5 pt, inner 2-2.5 pt at 300 dpi), centered composition with
3-4 mm margins and no border. Style should be kawaii, playful, sticker-like,
minimal detail, high contrast, screen-print inspired, with composition
filling about 70-80 % of the square and background icons arranged loosely
for balance. The output should be a ready-to-paste image-generation prompt
with (recipe_name) as a placeholder variable. Take all the time you need
"""    
    action["text"] = prompt
    action["method"] = "paste"
    action["delay"] = 120
    if mode_ai_wait != "":
        action["mode_ai_wait"] = mode_ai_wait
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["action"] = copy.deepcopy(action)
    oomlout_roboclick.run_single_action(**kwargs2)
    
    action = {}
    action["command"] = "ai_query"
    prompt = f"""
That is so so great! please do it for {image_detail}.
Take all the time you need
"""
    action["text"] = prompt
    action["method"] = "paste"
    action["delay"] = 240
    
    if mode_ai_wait != "":
        action["mode_ai_wait"] = mode_ai_wait
    kwargs2["action"] = copy.deepcopy(action)
    oomlout_roboclick.run_single_action(**kwargs2)

    action = {}
    action["command"] = "ai_query"
    prompt = f"""
You are a star that's perfect! now pelase geenrate the image remember
square proportions and take as much time as you need
"""
    action["text"] = prompt
    action["method"] = "paste"
    action["delay"] = 240
    if mode_ai_wait != "":
        action["mode_ai_wait"] = mode_ai_wait
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["action"] = copy.deepcopy(action)
    oomlout_roboclick.run_single_action (**kwargs2)


    action = {}
    #- command: 'save_image'
    action["command"] = "ai_save_image"
    action["file_name"] = f"initial_generated.png"
    if mode_ai_wait != "":
        action["mode_ai_wait"] = mode_ai_wait
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["action"] = copy.deepcopy(action)
    oomlout_roboclick.run_single_action(**kwargs2)

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
