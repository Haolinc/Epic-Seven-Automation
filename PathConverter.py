import os
import sys


def get_current_path(folder_name: str, file_name: str):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, folder_name, file_name)
    else:
        return os.path.join(os.path.abspath(os.getcwd()), folder_name, file_name)
