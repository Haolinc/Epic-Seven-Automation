import time
import PathConverter
from automation.Utilities import Utilities
from ui.UIComponentEnum import UIThreadMessage
from ui.UIMessage import UIMessage


class DailyArena:

    def __init__(self, utilities: Utilities, msg_queue):
        self.utilities = utilities
        self.msg_queue = msg_queue
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
        self.quick_start_button = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset", "Quick_Start_Button.png")))
        self.quick_confirm_button = utilities.process_image_from_disk((PathConverter.get_current_path("image\\arena_asset", "Quick_Confirm_Button.png")))

    def select_arena(self):
        if not self.utilities.wait_for_button_and_click_bool(self.NPC_challenge, "find npc challenge"):
            self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME,
                                         "failed to find npc challenge, iteration stop"))

    def challenge_opponent(self):
        self.utilities.wait_for_button_and_click(self.NPC_icon, "find NPC_icon")
        self.utilities.wait_for_button_and_click(self.challenge_button, "find challenge_button")
        time.sleep(2)
        if bool(self.utilities.find_image(self.utilities.get_numpy_screenshot(), self.quick_start_button)):
            self.utilities.wait_for_button_and_click(self.quick_start_button, "find quick start button")
            self.gear_check_notification()
            self.utilities.wait_for_button_and_click(self.quick_confirm_button, "find quick_confirm_button")
        else:
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

    def run_arena_automation_subprocess(self, total_iteration, run_with_friendship_flag):
        try:
            self.msg_queue.put(UIMessage(UIThreadMessage.START_DAILY_ARENA))
            self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, "Daily Arena Process Started"))
            self.select_arena()
            if run_with_friendship_flag:
                total_iteration += 5
                self.buy_extra_flag()
            self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, f"Starting {total_iteration} npc challenge"))
            for current_iteration in range(total_iteration):
                self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, f"Iteration: {current_iteration+1}"))
                self.challenge_opponent()
                time.sleep(3)
                self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, f"Iteration: {current_iteration+1} ended"))
            self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, "Arena automation completed!"))
            self.msg_queue.put(UIMessage(UIThreadMessage.STOP))
        except Exception as e:
            self.msg_queue.put(UIMessage(UIThreadMessage.ERROR, str(e)))
            self.msg_queue.put(UIMessage(UIThreadMessage.STOP))
