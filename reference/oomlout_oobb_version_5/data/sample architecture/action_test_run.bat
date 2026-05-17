@echo off
setlocal

set "ROOT_DIR=%~dp0"
pushd "%ROOT_DIR%" >nul

python run_tests.py
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
    echo [ERROR] Tests failed with exit code %EXIT_CODE%.
    echo         See test_result\results.md for details.
    popd >nul
    exit /b %EXIT_CODE%
)

echo [OK] Tests passed.
echo      test_result\results.md

popd >nul
exit /b 0

