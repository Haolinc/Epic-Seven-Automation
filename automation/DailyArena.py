import time
import PathConverter
from automation.Utilities import Utilities
from ui.UIComponentEnum import UIThreadMessage
from ui.UIMessage import UIMessage


class DailyArena:
    """
    NPC challenge arena automation main logic.
    """
    def __init__(self, utilities: Utilities, msg_queue):
        self.utilities = utilities
        self.msg_queue = msg_queue
        self.arena_icon = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\arena_asset", "Arena_Icon.png"))
        self.arena = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\arena_asset", "Arena.png"))
        self.NPC_challenge = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "NPC_Challenge.png")))
        self.NPC_challenge_identifier = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "NPC_Challenge_Identifier.png")))
        self.match_window_identifier = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Match_Window_Identifier.png")))
        self.arena_flag_icon = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Arena_Flag_Icon.png")))
        self.friendship_point = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Friendship_Point.png")))
        self.flag_buy_button = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Flag_Buy_Button.png")))
        self.NPC_icon = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "NPC_ICON.png")))
        self.challenge_button = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Challenge_Button.png")))
        self.start_button = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Start_Button.png")))
        self.do_not_display = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Do_Not_Display_Button.png")))
        self.auto_battle_button = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Auto_Battle_Button.png")))
        self.auto_battle_identifier = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Auto_Battle_Identifier.png")))
        self.confirm_Button = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Confirm_Button.png")))
        self.quick_start_button = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Quick_Start_Button.png")))
        self.quick_confirm_button = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Quick_Confirm_Button.png")))
        self.empty_quick_match = utilities.process_image_from_disk(
            (PathConverter.get_current_path("image\\arena_asset", "Empty_Quick_Match.png")))

    def __select_arena(self):
        self.utilities.click_target(target_tagged_img=self.NPC_challenge,
                                    future_tagged_imgs=self.NPC_challenge_identifier,
                                    identifier="find npc challenge")

    def __challenge_opponent(self):
        self.utilities.click_target(target_tagged_img=self.NPC_icon, future_tagged_imgs=self.challenge_button,
                                    timeout=5, identifier="find NPC_icon")
        self.utilities.click_target(target_tagged_img=self.challenge_button, future_tagged_imgs=self.match_window_identifier,
                                    timeout=5, color_sensitive=True, identifier="find challenge_button")
        if bool(self.utilities.find_image(self.utilities.get_numpy_screenshot(), self.quick_start_button.image)):
            self.utilities.click_target(target_tagged_img=self.quick_start_button,
                                        future_tagged_imgs=[self.do_not_display, self.quick_confirm_button],
                                        timeout=5, identifier="find quick start button")
            self.__gear_check_notification()
            self.utilities.click_target(target_tagged_img=self.quick_confirm_button,
                                        future_tagged_imgs=self.NPC_challenge_identifier, timeout=10, cache_click=False,
                                        color_sensitive=True, confidence=0.93, identifier="find quick_confirm_button")
        else:
            self.__empty_quick_match_check()
            self.utilities.click_target(target_tagged_img=self.start_button,
                                        future_tagged_imgs=[self.do_not_display, self.auto_battle_button], timeout=5,
                                        identifier="find start button")
            self.__gear_check_notification()
            self.utilities.click_target(target_tagged_img=self.auto_battle_button,
                                        future_tagged_imgs=self.auto_battle_identifier, timeout=10,
                                        identifier="find auto_battle_button")
            self.utilities.click_target(target_tagged_img=self.confirm_Button,
                                        future_tagged_imgs=self.NPC_challenge_identifier, timeout=60, cache_click=False,
                                        identifier="find confirm_Button")
        time.sleep(3)   # Need around 3 seconds for animation

    def __buy_extra_flag(self):
        self.utilities.click_target(target_tagged_img=self.arena_flag_icon, future_tagged_imgs=self.flag_buy_button,
                                    identifier="find arena_flag_icon")
        if bool(self.utilities.find_image(self.utilities.get_numpy_screenshot(), self.friendship_point.image)):
            self.utilities.click_target(target_tagged_img=self.friendship_point, future_tagged_imgs=self.flag_buy_button,
                                        identifier="find friendship_point")
        self.utilities.click_target(target_tagged_img=self.flag_buy_button,
                                    future_tagged_imgs=self.NPC_icon, identifier="find flag_buy_button")

    def __gear_check_notification(self):
        if bool(self.utilities.find_image(self.utilities.get_numpy_screenshot(), self.do_not_display.image)):
            self.utilities.click_target(target_tagged_img=self.do_not_display, future_tagged_imgs=self.quick_confirm_button,
                                        identifier="Do_Not_Display_Button")

    def __empty_quick_match_check(self):
        if bool(self.utilities.find_image(self.utilities.get_numpy_screenshot(), self.empty_quick_match.image)):
            self.utilities.click_target(target_tagged_img=self.empty_quick_match, future_tagged_imgs=self.start_button,
                                        identifier="Empty_Quick_Match")

    def run_arena_automation_subprocess(self, total_iteration, run_with_friendship_flag):
        try:
            self.msg_queue.put(UIMessage(UIThreadMessage.START_DAILY_ARENA))
            self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, "Daily Arena Process Started"))
            self.__select_arena()
            if run_with_friendship_flag:
                total_iteration += 5
                self.__buy_extra_flag()
            self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, f"Starting {total_iteration} npc challenge"))
            for current_iteration in range(total_iteration):
                self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, f"Iteration: {current_iteration + 1}"))
                self.__challenge_opponent()
                self.msg_queue.put(
                    UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, f"Iteration: {current_iteration + 1} ended"))
            self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, "Arena automation completed!"))
            self.msg_queue.put(UIMessage(UIThreadMessage.STOP))
        except Exception as e:
            self.msg_queue.put(UIMessage(UIThreadMessage.ERROR, str(e)))
