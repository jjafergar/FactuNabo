# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('Plantillas Facturas', 'Plantillas Facturas'), ('Facturas PDF', 'Facturas PDF'), ('resources', 'resources'), ('resources\\icons', 'resources\\icons'), ('resources\\previews', 'resources\\previews'), ('logs', 'logs'), ('responses', 'responses'), ('build', 'build'), ('DOCUMENTACION MACRO', 'DOCUMENTACION MACRO'), ('EsquemaProformas.xsd', '.'), ('factunabo_history.db', '.'), ('users.json', '.'), ('README.md', '.'), ('README_Integracion_Macro.md', '.'), ('styles.qss', '.'), ('Resumen FRAs 2025 aBalados Services_macro.xlsm', '.'), ('FactuNabo.spec', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FactuNabo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources\\logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FactuNabo',
)
