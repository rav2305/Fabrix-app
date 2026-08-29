import subprocess
import sys
import os

def build_executable():
    """Builds a standalone Windows executable (.exe) for Laptop using PyInstaller."""
    print("--- Packaging Fabrix into Standalone Laptop EXE ---")
    
    # 1. Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "pywebview"])

    # 2. PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=Fabrix_Billing_Software",
        "--onefile",
        "--noconsole",
        "--add-data=templates;templates",
        "--add-data=static;static",
        "desktop_app.py"
    ]
    
    print("Running build command:", " ".join(cmd))
    subprocess.check_call(cmd)
    print("--- BUILD COMPLETE! Check dist/Fabrix_Billing_Software.exe ---")

if __name__ == '__main__':
    build_executable()
