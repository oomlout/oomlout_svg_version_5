from pathlib import Path


def openscad_available_hint() -> list[Path]:
    """Known OpenSCAD install locations used in this repository."""

    return [
        Path(r"C:\Program Files\OpenSCAD\openscad.com"),
        Path(r"C:\Program Files\OpenSCAD\openscad.exe"),
        Path(r"C:\Program Files (x86)\OpenSCAD\openscad.com"),
        Path(r"C:\Program Files (x86)\OpenSCAD\openscad.exe"),
    ]
