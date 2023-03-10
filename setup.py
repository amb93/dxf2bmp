import sys
import cx_Freeze

build_exe_options = {"packages":["pyat5","numpy","ezdxf","cv2","math","PIL","datetime"]}

base = None
print(sys.platform)
if sys.platform == "win32":
    base = "Win32GUI"

cx_Freeze.setup(name = "dxf2bmp",version ="1.0",description = "Alpha build",options = {"build.exe": build_exe_options}, executables = [cx_Freeze.Executable("dxf2bmp_ui.py",base = base)])