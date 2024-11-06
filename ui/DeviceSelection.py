import customtkinter as tk

import AdbConnector
from automation.Utilities import Utilities
from ui.EpicSevenAutomationMain import MainWindow

tk.set_appearance_mode("System")


class DeviceSelectionUI(tk.CTk):
    def __init__(self):
        super().__init__()
        self.device_refresh_button = None
        self.startup_button = None
        self.adb_connection_menu = None
        self.startup_label = None
        self.title("E7 Secret Shop Auto")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.geometry("500x500")
        self.create_startup_widgets()

    def create_startup_widgets(self):
        self.startup_label = tk.CTkLabel(self, text="default text")
        self.startup_label.grid(pady=10, sticky="nsew")
        self.adb_connection_menu = tk.CTkOptionMenu(self)
        self.adb_connection_menu.grid(pady=10, sticky="nsew")
        self.device_refresh_button = tk.CTkButton(self, text="Refresh Device List", command=self.refresh_device_ui)
        self.device_refresh_button.grid(pady=10, sticky="nsew")
        self.startup_button = tk.CTkButton(self, text="Start Application", command=self.launch_main_window)
        self.startup_button.grid(pady=10, sticky="nsew")
        # Get active devices and refresh UI element
        self.refresh_device_ui()

    def refresh_device_ui(self):
        AdbConnector.refresh_adb_device_list()
        if AdbConnector.serial_and_model_dict:
            self.startup_label.configure(text="Please select device")
            self.adb_connection_menu.configure(values=list(AdbConnector.serial_and_model_dict.keys()))
            self.adb_connection_menu.set(list(AdbConnector.serial_and_model_dict.keys())[0])
            self.startup_button.configure(state="normal")
        else:
            self.startup_label.configure(text="No device found, please click refresh button to fetch device again")
            self.adb_connection_menu.configure(values=list())
            self.adb_connection_menu.set(" ")
            self.startup_button.configure(state="disabled")

    def launch(self):
        self.mainloop()

    def launch_main_window(self):
        print("DeviceSelectionUI dying")
        self.destroy()
        MainWindow(utilities=Utilities(AdbConnector.serial_and_model_dict[self.adb_connection_menu.get()])).launch()
