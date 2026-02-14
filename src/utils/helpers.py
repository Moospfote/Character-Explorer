import os
import sys

def get_resource_path(self, relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # In development, use the current directory as base path
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
