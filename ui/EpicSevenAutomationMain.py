import threading
import customtkinter as tk
from automation.DailyArena import DailyArena
from automation.ShopRefresh import ShopRefresh
from automation.Utilities import Utilities
import ui.UIHelper as UIHelper
from ui.UIComponentEnum import *

tk.set_appearance_mode("System")


class MainWindow(tk.CTk):
    thread: threading.Thread()
    thread_shutdown = threading.Event()
    shop_refresh: ShopRefresh = None
    utilities: Utilities = None
    daily_arena: DailyArena = None

    def __init__(self, utilities: Utilities):
        super().__init__()
        self.log_frame = None
        self.refresh_shop_count_entry = None
        self.arena_count = None
        self.top_label = None
        self.mystic_count_label = None
        self.covenant_count_label = None
        self.title("E7 Secret Shop Auto")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.geometry("500x500")
        self.shop_refresh = ShopRefresh(utilities, Listener(self))
        self.daily_arena = DailyArena(utilities)
        self.create_main_widgets()
        utilities.save_image()

    def create_main_widgets(self):
        # Main frame setup
        main_frame = tk.CTkFrame(self)
        main_frame.grid(pady=15, padx=15, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)

        # Top frame with counters
        top_count_frame = tk.CTkFrame(main_frame)
        top_count_frame.grid(pady=(10, 5), padx=10, sticky="ew")
        top_count_frame.grid_columnconfigure((0, 1), weight=1)  # Equal spacing for labels

        # Covenant and Mystic count labels
        self.covenant_count_label = tk.CTkLabel(top_count_frame, text="Total Covenant: 0", anchor="w")
        self.covenant_count_label.grid(pady=5, padx=(10, 5), column=0, row=0, sticky="ew")
        self.mystic_count_label = tk.CTkLabel(top_count_frame, text="Total Mystic: 0", anchor="e")
        self.mystic_count_label.grid(pady=5, padx=(5, 10), column=1, row=0, sticky="ew")

        # Label and input for iterations
        self.top_label = tk.CTkLabel(main_frame, text="Enter Total Iterations", anchor="w")
        self.top_label.grid(pady=(10, 5), padx=10, sticky="ew")
        self.refresh_shop_count_entry = tk.CTkEntry(main_frame, placeholder_text="Refresh Count")
        self.refresh_shop_count_entry.grid(pady=5, padx=10, sticky="ew")

        # Start button
        self.start_shop_refresh_button = tk.CTkButton(main_frame, text="Start Shop Refresh",
                                                      command=self.run_shop_refresh_process)
        self.start_shop_refresh_button.grid(pady=(5, 15), padx=10, sticky="ew")

        # Arena options
        arena_label = tk.CTkLabel(main_frame, text="Arena Settings", anchor="w", font=("Arial", 12, "bold"))
        arena_label.grid(pady=(10, 5), padx=10, sticky="w")

        self.arena_count = tk.CTkEntry(main_frame, placeholder_text="Arena Count")
        self.arena_count.grid(pady=5, padx=10, sticky="ew")
        self.arena_with_extra = tk.BooleanVar(value=False)
        self.arena_checkbox = tk.CTkCheckBox(
            main_frame,
            text="Arena with Extra",
            variable=self.arena_with_extra,
            onvalue=True,
            offvalue=False
        )
        self.arena_checkbox.grid(pady=5, padx=10, sticky="w")

        # Arena start button
        self.start_arena_button = tk.CTkButton(main_frame, text="Start Arena", command=self.run_arena_process)
        self.start_arena_button.grid(pady=(5, 15), padx=10, sticky="ew")

        # Logger frame to track log (Unchanged as per request)
        self.log_frame = tk.CTkScrollableFrame(master=main_frame, height=200, width=400)
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(0, weight=1)
        self.log_frame.grid(pady=(10, 10), padx=10, sticky="nsew")

    # Function to change button state and run or terminate process in thread
    def run_shop_refresh_process(self):
        if self.start_shop_refresh_button.cget("text") == "Start Shop Refresh":
            self.start_shop_refresh_button.configure(text="Stop Shop Refresh")
            self.shop_refresh.start_shop_refresh_with_thread()
        else:
            self.start_shop_refresh_button.configure(state="disabled")
            UIHelper.add_label_to_frame(frame=self.log_frame, text="####### Process Stopping, Please Wait #######")
            self.shop_refresh.stop_shop_refresh()

    def run_arena_process(self):
        if self.start_arena_button.cget("text") == "Start Arena":
            self.thread_shutdown.clear()
            self.thread = threading.Thread(target=self.start_arena_process, daemon=True)
            self.thread.start()
        else:
            self.start_arena_button.configure(state="disabled")
            UIHelper.add_label_to_frame(frame=self.log_frame, text="####### Process Stopping, Please Wait #######")
            self.thread_shutdown.set()
            self.check_shutdown_flag_in_thread()

    def start_arena_process(self):
        UIHelper.reset_frame(self.log_frame)
        UIHelper.add_label_to_frame(frame=self.log_frame, text="####### Process Starting #######")
        total_arena_run = int(self.arena_count.get())
        arena_with_extra = bool(self.arena_checkbox.get())
        self.top_label.configure(text="Iteration started")
        self.start_shop_refresh_button.configure(text="Stop")
        self.start_arena_automation_iteration(total_arena_run, arena_with_extra)

    def start_arena_automation_iteration(self, total_arena_run, arena_with_extra):
        self.daily_arena.arena_automation(total_arena_run, arena_with_extra)

    # Use for unlocking the button from disabled state
    # REMOVE THIS FUNCTION AFTER ARENA THREAD REFACTOR !!!!!!!!!!
    def check_shutdown_flag_in_thread(self):
        if self.thread.is_alive():
            self.after(100, self.check_shutdown_flag_in_thread)
        else:
            self.reset_widgets()

    # REMOVE THIS FUNCTION AFTER ARENA THREAD REFACTOR !!!!!!!!!!
    def reset_widgets(self):
        self.start_shop_refresh_button.configure(state="normal")
        self.start_shop_refresh_button.configure(text="Start")
        self.top_label.configure(text="Please enter the total iterations you want to run")

    def launch(self):
        self.mainloop()


class Listener:
    def __init__(self, parent: MainWindow):
        self.parent = parent

    def add_label_to_log_frame(self, text: str):
        UIHelper.add_label_to_frame(frame=self.parent.log_frame, text=text)

    def reset_log_frame(self):
        UIHelper.reset_frame(frame=self.parent.log_frame)

    def set_label_text(self, label_enum: LabelEnum, text: str):
        self.parent.__getattribute__(label_enum.value).configure(text=text)

    def set_button_text(self, button_enum: ButtonEnum, text: str):
        self.parent.__getattribute__(button_enum.value).configure(text=text)

    def reset_ui_component(self, ui_component: UIComponent):
        match ui_component:
            case UIComponent.SHOP_REFRESH:
                self.parent.start_shop_refresh_button.configure(state="normal")
                self.parent.start_shop_refresh_button.configure(text="Start Shop Refresh")
            case UIComponent.ARENA:
                self.parent.start_arena_button.configure(state="normal")
                self.parent.start_arena_button.configure(text="Start Arena")
            case _:
                print("No Valid UIComponent Found")

    def get_entry_count(self, entry_enum: EntryEnum) -> int:
        return int(self.parent.__getattribute__(entry_enum.value).get())
