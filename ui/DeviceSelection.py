import customtkinter as tk

import AdbConnector
from automation.Utilities import Utilities
from ui.EpicSevenAutomationMain import MainWindow
import PIL.Image as Image

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
        self.resizable(width=False, height=False)

    def create_startup_widgets(self):
        self.startup_label = tk.CTkLabel(self, text="default text")
        self.startup_label.grid(pady=10, sticky="nsew")
        self.device_screenshot_image = tk.CTkImage(light_image=Image.open("some.png"),
                                                   size=(450, 250))
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
        AdbConnector.refresh_adb_device_list()
        if AdbConnector.serial_and_model_dict:
            mode_name_list = list(AdbConnector.serial_and_model_dict.keys())
            self.startup_label.configure(text="Please select device")
            for serial_number, image in AdbConnector.serial_and_model_dict.values():
                print(f"serial_number: {serial_number}, image: {image}")
            self.adb_connection_menu.configure(values=mode_name_list)
            self.adb_connection_menu.set(mode_name_list[0])
            self.startup_button.configure(state="normal")
            self.show_current_screenshot(mode_name_list[0])
        else:
            self.startup_label.configure(text="No device found, please click refresh button to fetch device again")
            self.adb_connection_menu.configure(values=list())
            self.adb_connection_menu.set(" ")
            self.startup_button.configure(state="disabled")

    def show_current_screenshot(self, choice):
        choice_image = AdbConnector.serial_and_model_dict[choice][1]
        self.device_screenshot_image.configure(light_image=choice_image)
        print(f"choice: {choice}, image: {AdbConnector.serial_and_model_dict[choice][1]}")

    def launch(self):
        self.mainloop()

    def launch_main_window(self):
        print("DeviceSelectionUI dying")
        self.destroy()
        MainWindow(
            utilities=Utilities(AdbConnector.serial_and_model_dict[self.adb_connection_menu.get()][0])).launch()
