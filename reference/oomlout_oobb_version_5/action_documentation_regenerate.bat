@echo off
python components\documentation.py ^
    --json "components\documentation_data.json" ^
    --html-template "templates\oobb_documentation_template.html" ^
    --html-output "components\documentation.html" ^
    --objects-root "components" ^
    --markdown
echo Done. Open components\documentation.html to view.
