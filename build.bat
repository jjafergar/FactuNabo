@echo off

echo "This script builds the application into a one-directory bundle."
echo "Make sure you have PyInstaller installed:"
echo "pip install pyinstaller"

pyinstaller --onedir --noconsole ^
    --icon="resources/logo.ico" ^
    --add-data "resources;resources" ^
    --add-data "styles.qss;." ^
    --add-data "EsquemaProformas.xsd;." ^
    --add-data "users.json;." ^
    --add-data "factunabo_history.db;." ^
    --add-data "Plantillas Facturas;Plantillas Facturas" ^
    --add-data "Facturas PDF;Facturas PDF" ^
    main.py
