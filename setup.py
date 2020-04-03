import cx_Freeze
from cx_Freeze import *

setup(
    name = "Stone Detector",
    version="1.0",
    options = {"build_exe":{"packages":["numpy", "PIL", "matplotlib","tkinter"]}},
    executables= [
        Executable(
            "Stone_Detector.py",
            )
        ]
    )
