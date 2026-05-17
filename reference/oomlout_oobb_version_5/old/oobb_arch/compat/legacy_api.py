"""Thin compatibility wrappers.

Phase 1 behavior: simply delegates to existing `oobb_base` API.
"""


def get_thing_from_dict(*args, **kwargs):
    import oobb

    return oobb.get_thing_from_dict(*args, **kwargs)


def build_thing(*args, **kwargs):
    import oobb

    return oobb.build_thing(*args, **kwargs)


def build_things(*args, **kwargs):
    import oobb

    return oobb.build_things(*args, **kwargs)
