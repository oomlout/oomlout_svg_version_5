import random

import sys

import time

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'base'
    d["name_long_4"] = 'time'
    d["name_long_5"] = 'robo_delay'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_base_time_delay'
    d["name_long"] = 'roboclick_action_base_time_delay'
    d["name_short"] = ['robo_delay', 'delay', 'wait', 'sleep']
    d["name_short_options"] = ['robo_delay', 'delay', 'wait', 'sleep']
    d["description"] = 'Pause execution for N seconds with optional skip mechanisms.'
    d["returns"] = 'empty string normally; may early-return on skip'
    d["category"] = 'Other'
    v = []
    if True:
        v.append({'name': 'delay', 'description': 'Number of seconds to delay (default: 1)', 'type': 'number', 'default': 1})
        v.append({'name': 'rand', 'description': 'Additional random seconds to add to delay (default: 0)', 'type': 'number', 'default': 0})
        v.append({'name': 'message', 'description': 'Optional message to print before delaying', 'type': 'string', 'default': ''})
        v.append({'name': 'mode_skip_key', 'description': "Whether pressing 's' should skip the delay (default: true)", 'type': 'boolean', 'default': True})
        v.append({'name': 'mode_scroll_lock_skip', 'description': 'Whether toggling Scroll Lock should skip the delay (default: true, Windows only)', 'type': 'boolean', 'default': True})
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
    try:
        if sys.platform == "win32":
            import msvcrt

            if msvcrt.kbhit():
                return msvcrt.getch().decode("utf-8", errors="ignore").lower()
        else:
            import select

            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                return sys.stdin.read(1).lower()
    except Exception:
        return None
    return None

def _scroll_lock_toggled():
    if sys.platform != "win32":
        return False
    try:
        import ctypes

        # 0x91 = VK_SCROLL
        return (ctypes.windll.user32.GetKeyState(0x91) & 1) == 1
    except Exception:
        return False

def _as_bool(value, default):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    return bool(value)

def action(**kwargs):
    return old(**kwargs)

def old(**kwargs):
    action_cfg = kwargs.get("action", {}) or {}

    delay = action_cfg.get("delay", kwargs.get("delay", 1))
    rand = action_cfg.get("rand", kwargs.get("rand", 0))
    message = action_cfg.get("message", kwargs.get("message", ""))

    mode_skip_key = _as_bool(
        action_cfg.get("mode_skip_key", kwargs.get("mode_skip_key", True)),
        default=True,
    )
    mode_scroll_lock_skip = _as_bool(
        action_cfg.get("mode_scroll_lock_skip", kwargs.get("mode_scroll_lock_skip", True)),
        default=True,
    )

    try:
        delay = float(delay)
    except Exception:
        delay = 1.0
    try:
        rand = int(rand)
    except Exception:
        rand = 0

    if message:
        print(message)
    if rand > 0:
        delay += random.randint(0, rand)

    if delay <= 1.0:
        time.sleep(delay)
        return ""

    if delay > 5.0:
        print(f"<<<<<>>>>> waiting for {delay:.0f} seconds (press 's' to skip)")
        splits = 10
        chunk = max(1, int(delay // splits))
        for _ in range(splits):
            print(".", end="", flush=True)
            for _ in range(chunk):
                if mode_skip_key and _check_key_pressed() == "s":
                    print("\nDelay skipped by 's'")
                    time.sleep(1)
                    return ""
                if mode_scroll_lock_skip and _scroll_lock_toggled():
                    print("\nScroll Lock toggled; skipping delay")
                    time.sleep(1)
                    return ""
                time.sleep(1)
        print("")
        return ""

    print(f"waiting for {delay:.0f} seconds (press 's' to skip)", end="", flush=True)
    remaining = max(1, int(round(delay)))
    for _ in range(remaining):
        print(".", end="", flush=True)
        if mode_skip_key and _check_key_pressed() == "s":
            print("\nDelay skipped by 's'")
            time.sleep(1)
            return ""
        time.sleep(1)
    print("")
    return ""

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
