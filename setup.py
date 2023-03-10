import sys
from cx_Freeze import setup, Executable

setup(
    name = "dxf2bmp",
    version = "0.1",
    description = "Convert dxf files into bmp images",
    executables = [Executable("dxf2bmp_ui.py", base = "Win32GUI")])