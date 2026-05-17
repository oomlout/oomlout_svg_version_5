@echo off
setlocal

set "ROOT_DIR=%~dp0"
pushd "%ROOT_DIR%" >nul

set "DOCS_TEMPLATE=templates\documentation_template.html"
set "DOCS_JSON=documentation_data.json"
set "DOCS_HTML=documentation.html"

if not exist "%DOCS_TEMPLATE%" (
    echo [ERROR] Documentation template not found: %DOCS_TEMPLATE%
    popd >nul
    exit /b 1
)

python oomlout_roboclick.py ^
    --docs-json "%DOCS_JSON%" ^
    --docs-html-template "%DOCS_TEMPLATE%" ^
    --docs-html-output "%DOCS_HTML%" ^
    --docs-only

if errorlevel 1 (
    echo [ERROR] Documentation generation failed.
    popd >nul
    exit /b 1
)

echo [OK] Documentation regenerated.
echo      %DOCS_JSON%
echo      %DOCS_HTML%

popd >nul
exit /b 0
