import aircv as ac
import PathConverter
import time

from Utilities import Utilities

arena_icon = ac.imread(PathConverter.get_current_path("image/arena_asset", "ArenaIcon.png"))
arena = ac.imread(PathConverter.get_current_path("image/arena_asset", "Arena.png"))
NPC_challenge = ac.imread((PathConverter.get_current_path("image/arena_asset", "")))
arena_flag_icon = ac.imread((PathConverter.get_current_path("image/arena_asset", "Arena_flag_icon")))
friendship_point = ac.imread((PathConverter.get_current_path("image/arena_asset", "Friendship_Point")))
flag_buy_button = ac.imread((PathConverter.get_current_path("image/arena_asset","Flag_Buy_Button")))
NPC_icon = ac.imread((PathConverter.get_current_path("image/arena_asset", "NPC_ICON")))
challenge_button = ac.imread((PathConverter.get_current_path("image/arena_asset", "Challenge_Button")))
start_button = ac.imread((PathConverter.get_current_path("image/arena_asset", "Start_Button")))
do_not_display = ac.imread((PathConverter.get_current_path("image/arena_asset", "Do_Not_Display_Button")))
auto_battle_button = ac.imread((PathConverter.get_current_path("image/arena_asset", "Auto_Battle_Button")))

class DailyArena:
    def __init__(self, utilities: Utilities):
        self.utilities = utilities

    def arena_automation (self):
        self.select_arena()
        self.challenge_opponent()

    def arena_automation_with_extra (self) :
        self.select_arena()
        self.buy_extra_flag()
        self.challenge_opponent()


    def select_arena(self):
        self.utilities.click_target(self.utilities.get_numpy_screenshot(), arena_icon, "find arena_icon")
        time.sleep(1)
        self.utilities.click_target(self.utilities.get_numpy_screenshot(), arena, "find arena")
        time.sleep(1)
        self.utilities.click_target(self.utilities.get_numpy_screenshot(), NPC_challenge, "find npc challenge")
        time.sleep(1)

    def buy_extra_flag(self):
        self.utilities.click_target(self.utilities.get_numpy_screenshot(), arena_flag_icon, "find arena_flag_icon")
        time.sleep(1)
        self.utilities.click_target(self.utilities.get_numpy_screenshot(), friendship_point, "find friendship_point")
        time.sleep(1)
        self.utilities.click_target(self.utilities.get_numpy_screenshot(), flag_buy_button, "find flag_buy_button")
        time.sleep(1)

    def challenge_opponent(self):
        self.utilities.click_target(self.utilities.get_numpy_screenshot(), NPC_icon, "find NPC_icon")
        time.sleep(1)
        self.utilities.click_target(self.utilities.get_numpy_screenshot(), challenge_button, "find challenge_button")
        time.sleep(1)
        self.utilities.click_target(self.utilities.get_numpy_screenshot(), start_button, "find start button")
        time.sleep(1)
        self.gear_check_notification()
        self.utilities.click_target(self.utilities.get_numpy_screenshot(), auto_battle_button, "find start button")
        time.sleep(1)
        self.utilities.click_target(self.utilities.get_numpy_screenshot(), start_button, "find start button")
        time.sleep(1)


    def gear_check_notification(self):
        if self.utilities.find_image(do_not_display) is not None:
            self.utilities.click_target(self.utilities.get_numpy_screenshot(), arena_icon, "Do_Not_Display_Button")

