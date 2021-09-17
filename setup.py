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
    executables = [
        Executable(
            "app.py",
            copyright="Copyright (C) 2021 ChaosAnnals",
        ),
    ],
    options = {
        "build_exe": build_exe_options
    }
)