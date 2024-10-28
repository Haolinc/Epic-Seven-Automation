import threading
import AdbConnector
import time
import customtkinter as tk

from Utils import Utils
from automation.Utilities import Utilities
from automation.DailyArena import DailyArena

tk.set_appearance_mode("System")


class MainWindow(tk.CTk):
    covenant_count: int = 0
    mystic_count: int = 0
    thread: threading.Thread()
    thread_shutdown = threading.Event()
    utils: Utils = None
    utilities: Utilities = None
    daily_arena: DailyArena = None

    def __init__(self, utils: Utils, utilities: Utilities):
        super().__init__()
        self.log_frame = None
        self.iteration_entry = None
        self.top_label = None
        self.mystic_count_label = None
        self.covenant_count_label = None
        self.title("E7 Secret Shop Auto")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.geometry("500x500")
        self.utils = utils
        self.daily_arena = DailyArena(utilities)
        self.create_main_widgets()
        utilities.save_image()

    def create_main_widgets(self):
        main_frame = tk.CTkFrame(self)
        main_frame.grid(pady=10, padx=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Top frame that contains bookmark count labels
        top_count_frame = tk.CTkFrame(main_frame)
        top_count_frame.grid(pady=10, padx=10)
        top_count_frame.grid_columnconfigure(1, weight=1)
        top_count_frame.grid_rowconfigure(0, weight=1)
        self.covenant_count_label = tk.CTkLabel(top_count_frame, text=f"Total Covenant: 0")
        self.covenant_count_label.grid(pady=10, padx=30, column=0, row=0, sticky="nsew")
        self.mystic_count_label = tk.CTkLabel(top_count_frame, text=f"Total Mystic: 0")
        self.mystic_count_label.grid(pady=10, padx=30, column=1, row=0, sticky="nsew")

        self.top_label = tk.CTkLabel(main_frame, text="Please enter the total iterations you want to run")
        self.top_label.grid(pady=10, padx=10, sticky="nsew")
        self.iteration_entry = tk.CTkEntry(main_frame, placeholder_text="Refresh Count")
        self.iteration_entry.grid(pady=10, padx=10)
        self.start_button = tk.CTkButton(main_frame, text="Start", command=self.run_main_process)
        self.start_button.grid(pady=10, padx=10)

        # new Arena automation start
        self.start_arena_button = tk.CTkButton(main_frame, text="Arena_Start", command=self.run_arena_process)
        self.start_arena_button.grid(pady=10, padx=10)

        # Logger frame to track log
        self.log_frame = tk.CTkScrollableFrame(master=main_frame, height=200, width=400)
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(0, weight=1)
        self.log_frame.grid(pady=10, padx=10)

    # Function to change button state and run or terminate process in thread
    def run_main_process(self):
        if self.start_button.cget("text") == "Start":
            self.thread_shutdown.clear()
            self.thread = threading.Thread(target=self.start_process, daemon=True)
            self.thread.start()
        else:
            self.start_button.configure(state="disabled")
            self.create_log_label("####### Process Stopping, Please Wait #######")
            self.thread_shutdown.set()
            self.check_shutdown_flag_in_thread()

    def run_arena_process(self):
        if self.start_arena_button.cget("text") == "Arena_Start":
            self.thread_shutdown.clear()
            self.thread = threading.Thread(target=self.start_arena_process(), daemon=True)
            self.thread.start()
        else:
            self.start_button.configure(state="disabled")
            self.create_log_label("####### Process Stopping, Please Wait #######")
            self.thread_shutdown.set()
            self.check_shutdown_flag_in_thread()

    def start_arena_process(self):
        self.reset_frame(self.log_frame)
        self.create_log_label("####### Process Starting #######")
        # total_iteration = int(self.iteration_entry.get())
        self.top_label.configure(text="Iteration started")
        self.start_button.configure(text="Stop")
        self.start_arena_automation_iteration()

    def start_arena_automation_iteration(self):
        self.daily_arena.arena_automation()

    # Use for unlocking the button from disabled state
    def check_shutdown_flag_in_thread(self):
        if self.thread.is_alive():
            self.after(100, self.check_shutdown_flag_in_thread)
        else:
            self.reset_widgets()

    def reset_widgets(self):
        self.start_button.configure(state="normal")
        self.start_button.configure(text="Start")
        self.top_label.configure(text="Please enter the total iterations you want to run")

    # Starts the process,
    def start_process(self):
        self.reset_frame(self.log_frame)
        self.create_log_label("####### Process Starting #######")
        total_iteration = int(self.iteration_entry.get())
        self.top_label.configure(text="Iteration started")
        self.start_button.configure(text="Stop")
        self.start_store_fresh_iteration(total_iteration)

    def create_log_label(self, text: str):
        test_label = tk.CTkLabel(self.log_frame, text=text)
        test_label.grid(sticky="nsew")
        self.log_frame._parent_canvas.yview_moveto(1.0)

    def reset_frame(self, frame: tk.CTkScrollableFrame | tk.CTkFrame):
        for widget in list(frame.children.values()):
            widget.destroy()
        frame.update()

    def check_bookmark_and_update_log(self):
        if self.utils.check_covenant():
            if self.utils.buy_covenant():
                self.create_log_label("Found Covenant Bookmark!")
                self.covenant_count += 5
                self.covenant_count_label.configure(text="Total Covenant: " + str(self.covenant_count))
            # This only happens when multiple retry attempt fails
            else:
                self.create_log_label("Covenant Purchase Fail, Stopping the application")
                self.thread_shutdown.set()
                self.check_shutdown_flag_in_thread()
                return
        if self.utils.check_mystic():
            if self.utils.buy_mystic():
                self.create_log_label("Found Mystic Bookmark!")
                self.mystic_count += 50
                self.mystic_count_label.configure(text="Total Mystic: " + str(self.mystic_count))
            # This only happens when multiple retry attempt fails
            else:
                self.create_log_label("Mystic Purchase Fail, Stopping the application")
                self.thread_shutdown.set()
                self.check_shutdown_flag_in_thread()

    def start_store_fresh_iteration(self, total_iteration: int):
        for current_iteration in range(0, total_iteration):
            self.create_log_label(f"--------Iteration: {current_iteration + 1}--------")
            self.check_bookmark_and_update_log()
            self.utils.swipe_down()
            time.sleep(0.5)
            self.check_bookmark_and_update_log()
            if self.thread_shutdown.is_set():
                self.create_log_label("####### Process Stopped #######")
                return
            # When refresh failed, Stop the application
            if not self.utils.refresh_shop():
                self.create_log_label("Refresh Shop Fail, Stopping the application")
                self.thread_shutdown.set()
                self.check_shutdown_flag_in_thread()
                return
        # Check again for last refresh
        self.check_bookmark_and_update_log()
        self.create_log_label("####### Process Stopped #######")
        self.thread_shutdown.set()
        self.check_shutdown_flag_in_thread()

    def launch(self):
        self.mainloop()
