from collections.abc import Callable
from typing import Any


BuilderCallable = Callable[..., Any]


class BuilderRegistry:
    """Explicit registry for mapping part type -> builder function.

    Phase 1 scope: standalone utility; no runtime wiring yet.
    """

    def __init__(self):
        self._builders: dict[str, BuilderCallable] = {}

    def register(self, part_type: str, builder: BuilderCallable) -> None:
        self._builders[part_type] = builder

    def has(self, part_type: str) -> bool:
        return part_type in self._builders

    def resolve(self, part_type: str) -> BuilderCallable:
        if part_type not in self._builders:
            raise KeyError(f"No builder registered for part type: {part_type}")
        return self._builders[part_type]

    def items(self):
        return self._builders.items()

