import subprocess
import adbutils
import customtkinter as tk

import PathConverter
from automation.Utilities import Utilities
from ui import UIHelper
from ui.EpicSevenAutomationMain import MainWindow
import PIL.Image as Image

tk.set_appearance_mode("System")

default_image = Image.open(PathConverter.get_current_path("image", "No_Image_Available.png"))
serial_and_image_dict: dict[str, Image.Image] = {}


class DeviceSelectionUI(tk.CTkToplevel):
    """
    Initial selection window to select desired emulator.
    """
    def __init__(self, root):
        super().__init__(root)
        self.device_refresh_button = None
        self.startup_button = None
        self.adb_connection_menu = None
        self.startup_label = None
        self.title("E7 Secret Shop Auto")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.geometry("500x500")
        self.create_startup_widgets()
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.master.destroy)
        UIHelper.set_window_icon(self)

    def create_startup_widgets(self):
        self.startup_label = tk.CTkLabel(self, text="default text")
        self.startup_label.grid(pady=10, sticky="nsew")
        self.device_screenshot_image = tk.CTkImage(light_image=default_image, size=(450, 250))
        self.device_screenshot_label_holder = tk.CTkLabel(self, width=200, height=200, text="",
                                                          image=self.device_screenshot_image)
        self.device_screenshot_label_holder.grid(pady=10, sticky="nsew")
        self.startup_label.grid(pady=10, sticky="nsew")
        self.adb_connection_menu = tk.CTkOptionMenu(self, command=self.show_current_screenshot)
        self.adb_connection_menu.grid(pady=10, sticky="nsew")
        self.device_refresh_button = tk.CTkButton(self, text="Refresh Device List", command=self.refresh_device_ui)
        self.device_refresh_button.grid(pady=10, sticky="nsew")
        self.startup_button = tk.CTkButton(self, text="Start Application", command=self.launch_main_window)
        self.startup_button.grid(pady=10, sticky="nsew")
        # Get active devices and refresh UI element
        self.refresh_device_ui()

    def refresh_device_ui(self):
        self.refresh_adb_device_list()
        if serial_and_image_dict:
            serial_name_list = list(serial_and_image_dict.keys())
            self.startup_label.configure(text="Please select device")
            self.adb_connection_menu.configure(values=serial_name_list)
            self.adb_connection_menu.set(serial_name_list[0])
            self.startup_button.configure(state="normal")
            self.show_current_screenshot(serial_name_list[0])
        else:
            self.startup_label.configure(text="No device found, please click refresh button to fetch device again")
            self.adb_connection_menu.configure(values=list())
            self.adb_connection_menu.set(" ")
            self.startup_button.configure(state="disabled")
            self.device_screenshot_image.configure(light_image=default_image)

    def refresh_adb_device_list(self):
        serial_and_image_dict.clear()
        adb_command = PathConverter.get_current_path("platform-tools", "adb devices -l")
        adb_device_result_list = subprocess.run(adb_command, capture_output=True, text=True).stdout.splitlines()
        adb_device_result_list.pop(0)
        adb_device_result_list.pop()
        for adb_device_info in adb_device_result_list:
            lst = adb_device_info.split(" ")  # lst[0] is the serial number
            serial_name = lst[0]
            current_model_device = adbutils.device(lst[0])
            current_device_image: Image = current_model_device.screenshot()
            serial_and_image_dict[serial_name] = current_device_image

    def show_current_screenshot(self, choice):
        choice_image = serial_and_image_dict[choice]
        self.device_screenshot_image.configure(light_image=choice_image)

    def launch_main_window(self):
        self.withdraw()
        MainWindow(root=self.master, utilities=Utilities(self.adb_connection_menu.get()))

