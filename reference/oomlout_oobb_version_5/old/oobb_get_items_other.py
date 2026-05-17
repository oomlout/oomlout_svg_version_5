from oobb_get_items_base import *
import oobb_base as ob


def get_bolt(**kwargs):
    from components.bolt.working import action

    return action(**kwargs)


def get_nut_m3():
    nut = get_nut(radius_name="m3", type="nut")
    return nut


def get_nut(**kwargs):
    from components.nuts.working import action

    return action(**kwargs)


def get_screw_countersunk(**kwargs):
    from components.screw_countersunk.working import action

    return action(**kwargs)

def get_screw_self_tapping(**kwargs):
    from components.screw_self_tapping.working import action

    return action(**kwargs)

def get_screw_socket_cap(**kwargs):
    from components.screw_socket_cap.working import action

    return action(**kwargs)


def get_standoff(**kwargs):
    from components.standoff.working import action

    return action(**kwargs)


def get_threaded_insert(**kwargs):
    from components.threaded_insert.working import action

    return action(**kwargs)


def get_bearing(**kwargs):
    from components.bearings.working import action

    return action(**kwargs)
