import cx_Freeze
import sys
import os
from pathlib import Path

base = "Win32GUI" if sys.platform == "win32" else None
sys.setrecursionlimit(10000)

# Adjust paths for TCL and TK
os.environ['TCL_LIBRARY'] = r"C:\Program Files\Python312\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Program Files\Python312\tcl\tk8.6"

base_path = Path(__file__).parent

executables = [
    cx_Freeze.Executable(
        script=str(base_path / "login_page.py"),
        base=base,
        target_name="MHC_System.exe",
        icon=None,  # Update this with the path to your .ico file if needed
    )
]

include_files = [
    str(base_path / "tcl86t.dll"),
    str(base_path / "tk86t.dll"),
    str(base_path / "vcomp140.dll"),
    str(base_path / "breast_cancer.py"),
    str(base_path / "Cervical_cancer.py"),
    str(base_path / "classifiers_menu.py"),
    str(base_path / "medicine_recommendation_system.py"),
    str(base_path / "models/breast_cancermodel.joblib"),
    str(base_path / "models/cervical_cancermodel.joblib"),
    str(base_path / "models/SVC_Model.joblib"),
    str(base_path / "Dataset/description.csv"),
    str(base_path / "Dataset/diets.csv"),
    str(base_path / "Dataset/medications.csv"),
    str(base_path / "Dataset/precautions_df.csv"),
    str(base_path / "Dataset/symtoms_df.csv"),
    str(base_path / "Dataset/Training.csv"),
    str(base_path / "Dataset/workout_df.csv"),
    str(base_path / "OIP2.jpg"),
]

packages = [
    "tkinter",
    "os",
    "joblib",
    "pandas",
    "numpy",
    "lime",
    "customtkinter",
    "PIL",
    "threading",
    "matplotlib",
]

includes = [
    "sklearn",
    "sklearn.utils._cython_blas",
    "sklearn.utils._openmp_helpers",
    "sklearn.utils.sparsefuncs_fast",
    "sklearn.neighbors._quad_tree",
    "sklearn.tree._utils",
]

cx_Freeze.setup(
    name="MHC System",
    version="0.1",
    description="Medical Health Care System using Tkinter",
    options={
        "build_exe": {
            "packages": packages,
            "includes": includes,
            "include_files": include_files,
            "optimize": 2,
        }
    },
    executables=executables,
)
    