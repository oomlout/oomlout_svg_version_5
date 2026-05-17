"""Shared component-dict helper functions for holder/wire builders."""

from __future__ import annotations

import copy
from typing import Any


def get_plate_cutout_dict(**kwargs: Any) -> dict[str, Any]:
    pos_plate = kwargs.get("pos_plate", [0, 0, 0])
    plate_thickness = kwargs.get("plate_thickness", 1.5)
    thickness = kwargs.get("thickness", 3)

    pos1 = copy.deepcopy(pos_plate)
    pos1[0] = pos1[0] + plate_thickness
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = "rounded_rectangle"
    p3["size"] = [23, 22, thickness - plate_thickness]
    p3["pos"] = pos1
    return p3


def get_plate_screw_dict(**kwargs: Any) -> dict[str, Any]:
    thickness = kwargs.get("thickness", 3)

    poss = []
    poss.append([7.5, -15, 0])
    poss.append([7.5, 15, 0])

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = "oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = thickness
    p3["nut"] = False
    p3["pos"] = poss

    return p3


def get_plate_nut_dict(**kwargs: Any) -> dict[str, Any]:
    pos_plate = kwargs.get("pos_plate", [0, 0, 0])
    thickness = kwargs.get("thickness", 3)
    width = kwargs.get("width", 1)

    poss = []
    dep = 3 if thickness == 9 else -thickness
    if width == 3:
        poss.append([7.5, -15, dep])
        poss.append([7.5, 15, dep])
    elif width == 2:
        poss.append([0, -15, dep])
        poss.append([0, 15, dep])

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = "oobb_nut"
    p3["radius_name"] = "m3"
    if thickness == 9:
        p3["zz"] = "top"
    else:
        p3["zz"] = "bottom"
    p3["overhang"] = True
    p3["rot"] = [0, 0, 0]
    p3["nut"] = False
    p3["hole"] = True
    p3["pos"] = poss
    p3.pop("extra", "")

    return p3
