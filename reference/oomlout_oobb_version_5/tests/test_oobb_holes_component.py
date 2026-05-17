import importlib
import sys
import unittest
from types import ModuleType
from unittest import mock


def _fake_opsc():
    return ModuleType("opsc")


def _fake_oobb():
    fake = ModuleType("oobb")

    def gv(name, mode=None):
        if name == "osp":
            return 15
        if name == "hole_radius_m3":
            return 1.5
        if name == "hole_radius_m6":
            return 3
        raise KeyError(name)

    def oobb_easy(**kwargs):
        return [kwargs]

    def oobb_easy_array(**kwargs):
        repeats = list(kwargs.get("repeats", []))
        pos_start = list(kwargs.get("pos_start", []))
        shift_arr = list(kwargs.get("shift_arr", []))
        while len(repeats) < 3:
            repeats.append(1)
        while len(pos_start) < 3:
            pos_start.append(0)
        while len(shift_arr) < 3:
            shift_arr.append(0)

        items = []
        for x in range(int(repeats[0])):
            for y in range(int(repeats[1])):
                for z in range(int(repeats[2])):
                    item = dict(kwargs)
                    item["pos"] = [
                        pos_start[0] + x * shift_arr[0],
                        pos_start[1] + y * shift_arr[1],
                        pos_start[2] + z * shift_arr[2],
                    ]
                    items.append(item)
        return items

    fake.gv = gv
    fake.oobb_easy = oobb_easy
    fake.oobb_easy_array = oobb_easy_array
    return fake


class OobbHolesComponentTests(unittest.TestCase):
    def _load_module(self):
        sys.modules.pop("components.oobb_holes.working", None)
        return importlib.import_module("components.oobb_holes.working")

    def test_both_holes_adds_expanded_all_grid(self):
        with mock.patch.dict("sys.modules", {"oobb": _fake_oobb(), "opsc": _fake_opsc()}):
            module = self._load_module()
            base = module.action(
                holes=["all"],
                width=3,
                height=2,
                pos=[0, 0, 0],
                depth=6,
                radius_name="m6",
                both_holes=False,
            )
            result = module.action(
                holes=["all"],
                width=3,
                height=2,
                pos=[0, 0, 0],
                depth=6,
                radius_name="m6",
                both_holes=True,
            )

        self.assertEqual(len(base), 18)
        self.assertEqual(len(result), 63)
        self.assertEqual(sum(1 for item in result if item.get("r") == 1.5), 45)

    def test_both_holes_reuses_perimeter_pattern_for_m3_holes(self):
        with mock.patch.dict("sys.modules", {"oobb": _fake_oobb(), "opsc": _fake_opsc()}):
            module = self._load_module()
            base = module.action(
                holes=["perimeter"],
                width=3,
                height=2,
                pos=[0, 0, 0],
                depth=6,
                radius_name="m6",
                both_holes=False,
            )
            result = module.action(
                holes=["perimeter"],
                width=3,
                height=2,
                pos=[0, 0, 0],
                depth=6,
                radius_name="m6",
                both_holes=True,
            )

        self.assertEqual(len(base), 6)
        self.assertEqual(len(result), 18)
        self.assertEqual(sum(1 for item in result if item.get("radius_name") == "m3"), 12)


if __name__ == "__main__":
    unittest.main()