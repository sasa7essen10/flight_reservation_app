import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # When running from a PyInstaller bundle
        base_path = sys._MEIPASS
    except Exception:
        # When running from source
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
