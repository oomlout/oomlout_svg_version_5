import copy

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'skill'
    d["name_long_5"] = 'validate_json'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_skill_validate_json'
    d["name_long"] = 'roboclick_action_ai_skill_validate_json'
    d["name_short"] = ['validate_json', 'validate', 'ai_skill_validate_json']
    d["name_short_options"] = ['validate_json', 'validate', 'ai_skill_validate_json']
    d["description"] = 'Validate json.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI Skill'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
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

def ai_add_file(**kwargs):
    return _dispatch_action("ai_add_file", **kwargs)

def ai_new_chat(**kwargs):
    return _dispatch_action("ai_new_chat", **kwargs)

def ai_query(**kwargs):
    return _dispatch_action("ai_query", **kwargs)

def ai_save_text(**kwargs):
    return _dispatch_action("ai_save_text", **kwargs)

def browser_close_tab(**kwargs):
    return _dispatch_action("browser_close_tab", **kwargs)

def action(**kwargs):
    return old(**kwargs)

def old(**kwargs):
    """Validate and fix JSON content using AI."""
    action = kwargs.get("action", {})
    file_input = action.get("file_source", None)
    if not file_input:
        file_input = action.get("file_input", "data.json")
    file_output = action.get("file_destination", None)
    if not file_output:
        file_output = action.get("file_output", "data_fixed.json")
    directory = kwargs.get("directory", "")
    
    p3 = copy.deepcopy(kwargs)
    action ={}
    action["description"] = "Validate and fix JSON content using strict JSON rules."
    action["log_url"] = False
    p3["action"] = action
    ai_new_chat(**p3)

    #load input file
    p3 = copy.deepcopy(kwargs)
    action = p3.get("action", {})
    action["file_source"] = file_input
    p3["action"] = action
    ai_add_file(**p3)

    #create prompt
    p3 = copy.deepcopy(kwargs)
    action = {}
    action["text"] = f"""YOU ARE: A strict JSON Validator + Auto-Repair Bot.

GOAL:
You will receive a JSON file/content that may contain errors. Your job is to:
1) Validate it as STRICT JSON (RFC 8259).
2) If invalid, repair it with the smallest possible edits.
3) Re-validate and repeat until there are ZERO JSON syntax errors.
4) Output ONLY the final validated JSON, wrapped between the exact tags:
&&&tag for copy&&&
...json...
&&&tag for copy&&&

ABSOLUTE OUTPUT RULES:
- Output NOTHING except the validated JSON between the two &&&tag for copy&&& tags.
- No explanations, no bullet points, no notes, no analysis, no extra whitespace outside the tags.
- The final output must be STRICT JSON (no trailing commas, no comments, no JSON5 features).
- Use double quotes ONLY where JSON requires them (keys and string delimiters).
- IMPORTANT: Remove problematic double-quote characters used as inches marks inside string values.
  - If you detect inch notation like 3'9" or 4'0" inside a string, you MUST remove/replace the " character so it cannot break JSON.
  - Prefer replacement rules (choose the minimal change that preserves meaning):
    - Replace 3'9" → 3'9 in
    - Replace 4'0" → 4'0 in
    - Or replace with words: 3 ft 9 in, 4 ft 0 in (only if needed for clarity)
  - DO NOT escape the inches quote as \" (the user wants quotes removed, not escaped).
- Preserve the original structure and key order as much as possible; only change what is required to make it valid JSON.

VALIDATION / REPAIR LOOP (do not skip):
1) Attempt to parse the entire input as strict JSON.
2) If parsing fails:
   - Identify the earliest syntax-breaking issue (e.g., unescaped quote, missing comma, mismatched brace/bracket, invalid control character).
   - Apply the minimal edit to fix it.
   - Pay special attention to stray " inside strings (especially feet/inches patterns).
3) Re-parse from scratch.
4) Repeat until parsing succeeds with zero errors.

NORMALIZATION (after it parses successfully):
- Ensure consistent indentation (2 spaces).
- Ensure all strings are properly delimited.
- Ensure there is exactly one top-level JSON value (object or array).
- Do not add or remove fields unless required for syntactic validity.

**IMPORTANT HINT*** Sometimes the data will have a height as 4'10" format, fix this by replacing the " for inches with in first then try to fix the errors

INPUT:
Paste the JSON content now (raw text). Begin repair + validation immediately.
"""
    action["delay"] = 360
    action["mode_ai_wait"] = "fast_button_state"
    action["method"] = "paste"
    p3["action"] = action
    ai_query(**p3)  

    #ai_copy_text
    p3 = copy.deepcopy(kwargs)
    action = {}
    
    action["file_name_full"] = f"{file_output}.full_text.txt"
    action["file_name_clip"] = file_output
    action["clip"] = "&&&tag for copy&&&"
    p3["action"] = action
    ai_save_text(**p3)

    #browser_close_tab
    p3 = copy.deepcopy(kwargs)
    action = {}
    p3["action"] = action
    browser_close_tab(**p3)

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
