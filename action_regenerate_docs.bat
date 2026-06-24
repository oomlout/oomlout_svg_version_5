@echo off
setlocal

echo.
echo ============================================================
echo  SVG Pipeline -- Regenerate Documentation
echo ============================================================
echo.

:: Move to the folder this batch file lives in, regardless of where it was launched from
cd /d "%~dp0"

:: 1. Render sample SVGs for every component (overwrites existing)
echo [1/2] Generating component sample SVGs...
python generate_samples.py --force
if errorlevel 1 (
    echo ERROR: generate_samples.py failed.
    pause
    exit /b 1
)

echo.

:: 2. Build documentation.html + documentation_data.json
echo [2/2] Building documentation...
python svg_documentation.py
if errorlevel 1 (
    echo ERROR: svg_documentation.py failed.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  Done.  Open documentation.html in a browser to review.
echo ============================================================
echo.

endlocal
