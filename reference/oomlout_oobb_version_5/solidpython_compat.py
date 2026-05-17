from solid2 import background, debug, disable, root


_MODIFIER_MAP = {
    "#": debug,
    "%": background,
    "!": root,
    "*": disable,
    "debug": debug,
    "background": background,
    "root": root,
    "disable": disable,
}


def apply_modifier(obj, modifier):
    if not modifier:
        return obj
    modifier_fn = _MODIFIER_MAP.get(str(modifier).strip().lower())
    if modifier_fn is None:
        return obj
    return modifier_fn()(obj)
