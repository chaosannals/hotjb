import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os"],
    "excludes": ["tkinter"]
}

setup(
    name = "hotjb",
    version = "0.1.0",
    description = "yet a jieba http server",
    options = {"build_exe": build_exe_options},
    executables = [Executable("app.py")]
)