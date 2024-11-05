import aircv as ac
import PathConverter
import time

from automation.Utilities import Utilities

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
    def __init__(self, utilities: Utilities):
        self.utilities = utilities

    def select_arena(self):
        if not self.utilities.wait_for_button_and_click_bool(arena_icon,"find arena_icon"):
            print("Failed to find image. try next button")
            if not self.utilities.wait_for_button_and_click_bool(arena,"find arena"):
                print("Failed to find image. try next button")
                if not self.utilities.wait_for_button_and_click_bool(NPC_challenge, "find npc challenge"):
                    print("Failed to find image. loop end here")


    def challenge_opponent(self):
        self.utilities.wait_for_button_and_click(NPC_icon, "find NPC_icon")
        self.utilities.wait_for_button_and_click(challenge_button, "find challenge_button")
        self.utilities.wait_for_button_and_click(start_button, "find start button")
        self.gear_check_notification()
        self.utilities.wait_for_button_and_click(auto_battle_button, "find auto_battle_button", 10)
        self.utilities.wait_for_button_and_click(confirm_Button, "find confirm_Button",60)

    def buy_extra_flag(self):
        self.utilities.wait_for_button_and_click(arena_flag_icon, "find arena_flag_icon")
        self.utilities.wait_for_button_and_click(friendship_point, "find friendship_point")
        self.utilities.wait_for_button_and_click(flag_buy_button, "find flag_buy_button")

    def gear_check_notification(self):
        if self.utilities.find_image(self.utilities.get_numpy_screenshot(), do_not_display) is not None:
            self.utilities.wait_for_button_and_click(do_not_display, "Do_Not_Display_Button")

    def arena_automation (self, battle_count = 5, with_extra = False):
        self.utilities.click_center_of_screen()
        self.select_arena()
        if with_extra:
            battle_count += 5
            print(battle_count)
            self.buy_extra_flag()
        for _ in range(battle_count):
            self.challenge_opponent()
            time.sleep(3)