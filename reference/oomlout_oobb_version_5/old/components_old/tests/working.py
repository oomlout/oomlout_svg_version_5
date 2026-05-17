d = {}


def describe():
    global d
    d = {}
    d["name"] = 'tests'
    d["name_long"] = 'Part Sets: Tests'
    d["description"] = 'Dispatches to get_test_<extra> in oobb_get_items_test; requires a non-empty extra field.'
    d["category"] = 'Part Sets'
    d["shape_aliases"] = []
    d["returns"] = 'List of part definition dicts.'
    v = []
    v.append({"name": 'extra', "description": 'Selects which get_test_* function to call.', "type": 'string', "default": '(required)'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable
def items(size="oobb", **kwargs):
    import oobb_make_sets

    getter = getattr(oobb_make_sets, "get_tests")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import copy

    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    p3.pop("extra")
    p3["type"] = f"test_{extra}"
    if extra != "":
        current_module = __import__("oobb_get_items_test")
        function_name = "get_test_" + extra
        function_to_call = getattr(current_module, function_name)
        return function_to_call(**kwargs)
    else:
        raise Exception("No extra")


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="test", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
