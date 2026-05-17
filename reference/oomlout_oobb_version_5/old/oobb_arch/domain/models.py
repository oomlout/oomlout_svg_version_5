from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PartSpec:
    """Normalized part definition used by internal architecture layers."""

    identifier: str
    part_type: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class BuildRequest:
    """Build inputs independent of legacy script entrypoints."""

    part: PartSpec
    modes: tuple[str, ...] = ("3dpr", "laser", "true")
    overwrite: bool = True
    save_type: str = "none"


@dataclass(frozen=True)
class BuildArtifact:
    """A single generated artifact and metadata."""

    mode: str
    extension: str
    path: Path


@dataclass
class BuildResult:
    """Result object produced by internal engine execution."""

    part_id: str
    artifacts: list[BuildArtifact] = field(default_factory=list)


@dataclass(frozen=True)
class BuildPlan:
    """Internal plan used by engine for deterministic execution."""

    request: BuildRequest
