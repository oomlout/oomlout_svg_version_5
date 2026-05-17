"""Shared shaft helper functions."""

from __future__ import annotations

import copy
from typing import Any

import oobb


def add_oobb_shaft(**kwargs: Any) -> None:
    thing = kwargs.get("thing")
    kwargs.pop("thing", "")
    pos = kwargs.get("pos", [0, 0, 0])
    size = kwargs.get("size", "oobb")
    shaft = kwargs.get("shaft", "m6")
    thickness = kwargs.get("thickness", 3)
    # shaft
    if shaft == "":
        shaft = "m6"
    if shaft.startswith("m6") or shaft.startswith("m3"):
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"{size}_hole"
        p3["radius_name"] = shaft.split("_")[0]
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        oobb_base.append_full(thing, **p3)
    else:
        p3 = copy.deepcopy(kwargs)
        p3.pop("extra", "")
        p3["type"] = "n"
        p3["shape"] = f"oobb_{shaft}"
        p3["part"] = "shaft"
        pos1 = copy.deepcopy(pos)

        if shaft == "motor_servo_standard_01":
            p3["rot"] = [0, 0, 45]
            pos1[2] += 2
            p3["overhang"] = False
        elif shaft == "motor_tt_01":
            pos1[2] += thickness - 1
            p3["depth"] = 50

        p3["pos"] = pos1
        p3["m"] = "#"
        oobb.append_full(thing, **p3)


def get_shaft_center(thing: Any, **kwargs: Any) -> None:
    shaft = kwargs.get("shaft", "")
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    # shaft
    if shaft == "":
        shaft = "m6"
    if shaft.startswith("m6") or shaft.startswith("m3"):
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"{size}_hole"
        p3["radius_name"] = shaft
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        oobb.append_full(thing, **p3)
    else:
        p3 = copy.deepcopy(kwargs)
        p3.pop("extra", "")
        p3["type"] = "n"
        p3["shape"] = f"oobb_{shaft}"
        p3["part"] = "shaft"
        pos1 = copy.deepcopy(pos)

        if shaft == "motor_servo_standard_01":
            p3["rot"] = [0, 0, 45]
            pos1[2] += 2
            p3["overhang"] = False
        p3["pos"] = pos1
        oobb.append_full(thing, **p3)
