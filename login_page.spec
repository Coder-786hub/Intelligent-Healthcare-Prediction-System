# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Include all necessary data files from sklearn and numpy
sklearn_data = collect_data_files('sklearn')
numpy_data = collect_data_files('numpy')
numpy_modules = collect_submodules('numpy')

a = Analysis(
    ['login_page.py'],
    pathex=[],
    binaries=[
        (r"C:\Program Files\Python312\DLLs\tcl86t.dll", 'tcl'),
        (r"C:\Program Files\Python312\DLLs\tk86t.dll", 'tk'),
    ],
    datas=[
        (r"E:\Desktop\Project_folder\Dataset\description.csv", 'Dataset/'),
        (r"E:\Desktop\Project_folder\Dataset\diets.csv", 'Dataset/'),
        (r"E:\Desktop\Project_folder\Dataset\medications.csv", 'Dataset/'),
        (r"E:\Desktop\Project_folder\Dataset\precautions_df.csv", 'Dataset/'),
        (r"E:\Desktop\Project_folder\Dataset\symtoms_df.csv", 'Dataset/'),
        (r"E:\Desktop\Project_folder\Dataset\Training.csv", 'Dataset/'),
        (r"E:\Desktop\Project_folder\Dataset\workout_df.csv", 'Dataset/'),
        (r"E:\Desktop\Project_folder\Images\OIP2.jpg", "Image/"),
        (r"E:\Desktop\Project_folder\Images\thapar.jpeg", "Image/"),
        *sklearn_data,
        *numpy_data,
    ],
    hiddenimports=[
        "sklearn.ensemble._forest",
        "sklearn.utils._weight_vector",
        "numpy._core",
        "numpy._core._dtype_ctypes",
        *numpy_modules,
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='login_page',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
