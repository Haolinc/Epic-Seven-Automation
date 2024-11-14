import aircv as ac
import PathConverter
import time
import threading

from automation.Utilities import Utilities
from ui.UIComponentEnum import *

arena_icon = ac.imread(PathConverter.get_current_path("image\\arena_asset", "Arena_Icon.png"))
arena = ac.imread(PathConverter.get_current_path("image\\arena_asset", "Arena.png"))
NPC_challenge = ac.imread((PathConverter.get_current_path("image\\arena_asset", "NPC_Challenge.png")))
arena_flag_icon = ac.imread((PathConverter.get_current_path("image\\arena_asset", "Arena_flag_icon.png")))
friendship_point = ac.imread((PathConverter.get_current_path("image\\arena_asset", "Friendship_Point.png")))
flag_buy_button = ac.imread((PathConverter.get_current_path("image\\arena_asset","Flag_Buy_Button.png")))
NPC_icon = ac.imread((PathConverter.get_current_path("image\\arena_asset", "NPC_ICON.png")))
challenge_button = ac.imread((PathConverter.get_current_path("image\\arena_asset", "Challenge_Button.png")))
start_button = ac.imread((PathConverter.get_current_path("image\\arena_asset", "Start_Button.png")))
do_not_display = ac.imread((PathConverter.get_current_path("image\\arena_asset", "Do_Not_Display_Button.png")))
auto_battle_button = ac.imread((PathConverter.get_current_path("image\\arena_asset", "Auto_Battle_Button.png")))
confirm_Button = ac.imread((PathConverter.get_current_path("image\\arena_asset", "Confirm_Button.png")))

class DailyArena:
    thread_shutdown = threading.Event()

    def __init__(self, utilities: Utilities, listener):
        self.utilities = utilities
        self.ui_listener = listener

    def select_arena(self):
        if not self.utilities.wait_for_button_and_click_bool(arena,"find arena"):
            self.ui_listener.add_label_to_log_frame("failed to find find arena, trying for next button")
            if not self.utilities.wait_for_button_and_click_bool(NPC_challenge, "find npc challenge"):
                self.ui_listener.add_label_to_log_frame("failed to find npc challenge, iteration stop")

    def challenge_opponent(self):
        self.utilities.wait_for_button_and_click(NPC_icon, "find NPC_icon")
        self.utilities.wait_for_button_and_click(challenge_button, "find challenge_button")
        self.utilities.wait_for_button_and_click(start_button, "find start button")
        self.gear_check_notification()
        self.utilities.wait_for_button_and_click(auto_battle_button, "find auto_battle_button", 10, False)
        self.utilities.wait_for_button_and_click(confirm_Button, "find confirm_Button",60)

    def buy_extra_flag(self):
        self.utilities.wait_for_button_and_click(arena_flag_icon, "find arena_flag_icon")
        self.utilities.wait_for_button_and_click(friendship_point, "find friendship_point")
        self.utilities.wait_for_button_and_click(flag_buy_button, "find flag_buy_button")

    def gear_check_notification(self):
        if self.utilities.find_image(self.utilities.get_numpy_screenshot(), do_not_display) is not None:
            self.utilities.wait_for_button_and_click(do_not_display, "Do_Not_Display_Button")

    def arena_automation (self):
        total_iteration: int = self.ui_listener.get_entry_count(EntryEnum.ARENA_COUNT_ENTRY)
        run_with_friendship_flag: bool = self.ui_listener.get_checkbox_bool(CheckBoxEnum.ARENA_WITH_FRIENDSHIP)
        self.select_arena()
        if run_with_friendship_flag:
            total_iteration += 5
            self.buy_extra_flag()
        self.ui_listener.add_label_to_log_frame(text=f"--------Starting {total_iteration} npc challenge--------")
        for current_iteration in range(total_iteration):

            if self.thread_shutdown.is_set():
                break

            self.challenge_opponent()
            self.ui_listener.add_label_to_log_frame(text=f"--------Iteration: {current_iteration+1}--------")
            time.sleep(3)
        self.stop_daily_arena()

    def daily_arena_with_thread(self):
        self.thread_shutdown.clear()
        self.thread = threading.Thread(target=self.arena_automation, daemon=True).start()

    def stop_daily_arena(self):
        self.thread_shutdown.set()
        if self.thread.is_alive():
            self.thread.join()
        self.ui_listener.add_label_to_log_frame(text="####### Process Stopping #######")