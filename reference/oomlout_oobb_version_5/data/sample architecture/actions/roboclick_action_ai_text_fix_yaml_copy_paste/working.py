import os

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'text'
    d["name_long_5"] = 'yaml_copy_paste'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_text_fix_yaml_copy_paste'
    d["name_long"] = 'roboclick_action_ai_text_fix_yaml_copy_paste'
    d["name_short"] = ['yaml_copy_paste', 'ai_fix_yaml_copy_paste', 'fix_yaml_copy_paste']
    d["name_short_options"] = ['yaml_copy_paste', 'ai_fix_yaml_copy_paste', 'fix_yaml_copy_paste']
    d["description"] = 'Fix YAML formatting from copy-pasted content.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'ai'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'path of the file, referenced to current directory', 'type': 'string', 'default': ''})
        v.append({'name': 'file_destination', 'description': 'path of the output file, referenced to current directory', 'type': 'string', 'default': ''})
        v.append({'name': 'remove_top_level', 'description': 'list of top-level keys to remove from the YAML', 'type': 'string', 'default': ''})
        v.append({'name': 'new_item_name', 'description': 'name of the new item to add to the YAML', 'type': 'string', 'default': ''})
        v.append({'name': 'search_and_replace', 'description': 'list of search and replace operations to perform on the YAML', 'type': 'string', 'default': ''})
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
    """Fix YAML formatting from copy-pasted content."""
    action = kwargs.get("action", {})
    file_input = action.get("file_source", None)
    if not file_input:
        file_input = action.get("file_input", "working.yaml")
    file_output = action.get("file_destination", None)
    if not file_output:
        file_output = action.get("file_output", "working_fixed.yaml")
    directory = kwargs.get("directory", "")
    remove_top_level = action.get("remove_top_level", ["data"])
    new_item_name = action.get("new_item_name", "")
    search_and_replace = action.get("search_and_replace", [])
    #load input file
    with open(os.path.join(directory, file_input), 'r', encoding='utf-8') as f:
        text = f.read()
    #replace all double line breaks with singles
    if True:
        text = text.replace("\n\n", "\n")
    #remvoe_top_level
    if True:
        #if remove_top_level is a string make it an array
        if isinstance(remove_top_level, str):
            remove_top_level = [remove_top_level]
        for tag in remove_top_level:
            lines = text.split("\n")
            new_lines = []
            skip = False
            for line in lines:
                if line.strip().startswith(f"{tag}:"):
                    skip = True
                    continue
                if skip:
                    if line.startswith(" "):
                        continue
                    else:
                        skip = False
                new_lines.append(line)
            text = "\n".join(new_lines)
    #new_item_name
    if True:
        #if the line starts new_item name : then add "- "
        #if it has text add two spaces
        if new_item_name != "":
            lines = text.split("\n")
            new_lines = []
            for line in lines:
                if line.strip().startswith(f"{new_item_name}:"):
                    new_lines.append(f"- {line}")
                    continue
                else:
                    new_lines.append(f"  {line}")
            text = "\n".join(new_lines)
    #remove any lines that are all whitespace
    if True:
        lines = text.split("\n")
        new_lines = []
        for line in lines:
            if line.strip() == "":
                continue
            new_lines.append(line)
        text = "\n".join(new_lines)
    #search_and_replace
    if search_and_replace != []:
        for item in search_and_replace:
            search = item[0]
            replace = item[1]
            if search != "":
                text = text.replace(search, replace)
    
    
    #save output file
    with open(os.path.join(directory, file_output), 'w', encoding='utf-8') as f:
        f.write(text)
    pass

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
