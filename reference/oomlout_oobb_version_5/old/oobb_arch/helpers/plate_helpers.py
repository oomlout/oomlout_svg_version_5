"""Shared plate component helper functions."""

from __future__ import annotations

import copy
from typing import Any


def get_plate_dict(**kwargs: Any) -> dict[str, Any]:
    size = kwargs.get("size", "oobb")
    thickness = kwargs.get("thickness", 3)
    pos_plate = kwargs.get("pos_plate", [0, 0, 0])

    pos1 = copy.deepcopy(pos_plate)
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"{size}_plate"
    p3["depth"] = thickness
    p3["pos"] = pos1
    return p3


def get_plate_hole_dict(**kwargs: Any) -> dict[str, Any]:
    pos_plate = kwargs.get("pos_plate", [0, 0, 0])
    size = kwargs.get("size", "oobb")
    hole_sides = kwargs.get("hole_sides", ["left", "right", "top"])

    pos1 = copy.deepcopy(pos_plate)
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"{size}_holes"
    p3["holes"] = hole_sides
    p3["both_holes"] = True
    p3["pos"] = pos1

    return p3
