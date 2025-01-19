import threading
import time

import PathConverter
from automation.Utilities import Utilities
from ui.UIComponentEnum import *


class DailyArena:
    thread_shutdown = threading.Event()

    def __init__(self, utilities: Utilities, listener):
        self.utilities = utilities
        self.ui_listener = listener
        self.arena_icon = utilities.process_image_from_disk(PathConverter.get_current_path("image\\arena_asset", "Arena_Icon.png"))
        self.arena = utilities.process_image_from_disk(PathConverter.get_current_path("image\\arena_asset", "Arena.png"))
        self.NPC_challenge = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset", "NPC_Challenge.png")))
        self.arena_flag_icon = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset", "Arena_flag_icon.png")))
        self.friendship_point = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset", "Friendship_Point.png")))
        self.flag_buy_button = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset","Flag_Buy_Button.png")))
        self.NPC_icon = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset", "NPC_ICON.png")))
        self.challenge_button = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset", "Challenge_Button.png")))
        self.start_button = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset", "Start_Button.png")))
        self.do_not_display = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset", "Do_Not_Display_Button.png")))
        self.auto_battle_button = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset", "Auto_Battle_Button.png")))
        self.confirm_Button = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset", "Confirm_Button.png")))
        

    def select_arena(self):
        if not self.utilities.wait_for_button_and_click_bool(self.arena,"find arena"):
            self.ui_listener.add_label_to_log_frame("failed to find find arena, trying for next button")
            if not self.utilities.wait_for_button_and_click_bool(self.NPC_challenge, "find npc challenge"):
                self.ui_listener.add_label_to_log_frame("failed to find npc challenge, iteration stop")

    def challenge_opponent(self):
        self.utilities.wait_for_button_and_click(self.NPC_icon, "find NPC_icon")
        self.utilities.wait_for_button_and_click(self.challenge_button, "find challenge_button")
        self.utilities.wait_for_button_and_click(self.start_button, "find start button")
        self.gear_check_notification()
        self.utilities.wait_for_button_and_click(self.auto_battle_button, "find auto_battle_button", 10, False)
        self.utilities.wait_for_button_and_click(self.confirm_Button, "find confirm_Button",60)

    def buy_extra_flag(self):
        self.utilities.wait_for_button_and_click(self.arena_flag_icon, "find arena_flag_icon")
        self.utilities.wait_for_button_and_click(self.friendship_point, "find friendship_point")
        self.utilities.wait_for_button_and_click(self.flag_buy_button, "find flag_buy_button")

    def gear_check_notification(self):
        if bool(self.utilities.find_image(self.utilities.get_numpy_screenshot(), self.do_not_display)):
            self.utilities.wait_for_button_and_click(self.do_not_display, "Do_Not_Display_Button")

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
                self.ui_listener.add_label_to_log_frame(text="####### Process Stopped #######")
                self.ui_listener.reset_ui_component(UIComponent.ARENA)
                break
            self.ui_listener.add_label_to_log_frame(text=f"--------Iteration: {current_iteration+1}--------")
            self.challenge_opponent()
            time.sleep(3)
            self.ui_listener.add_label_to_log_frame(text=f"--------Iteration: {current_iteration+1} ended--------")
        self.stop_daily_arena()

    # def daily_arena_with_thread(self):
    #     self.thread_shutdown.clear()
    #     self.thread = threading.Thread(target=self.arena_automation, daemon=True).start()
    #
    # def stop_daily_arena(self):
    #     self.thread_shutdown.set()
    #     if self.thread.is_alive():
    #         self.ui_listener.add_label_to_log_frame(text=f"thread join")
    #         self.thread.join()