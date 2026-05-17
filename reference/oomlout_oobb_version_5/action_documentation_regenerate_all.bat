@echo off
python components\documentation.py ^
    --json "components\documentation_data.json" ^
    --html-template "templates\oobb_documentation_template.html" ^
    --html-output "components\documentation.html" ^
    --objects-root "components" ^
    --markdown
python components\generate_all_component_tests.py --objects-root "components" --skip-existing-images
python components\documentation.py ^
    --json "components\documentation_data.json" ^
    --html-template "templates\oobb_documentation_template.html" ^
    --html-output "components\documentation.html" ^
    --objects-root "components" ^
    --markdown
echo Done. Open components\documentation.html to view.
