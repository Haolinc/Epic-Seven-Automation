import random
import time
import numpy
import adbutils
import aircv as ac
import PathConverter


covenant = ac.imread(PathConverter.get_current_path("image", "Covenant.png"))
covenant_buy = ac.imread(PathConverter.get_current_path("image", "CovenantBuy.png"))
covenant_buy_confirmation = ac.imread(PathConverter.get_current_path("image", "CovenantBuyConfirmation.png"))
mystic = ac.imread(PathConverter.get_current_path("image", "Mystic.png"))
mystic_buy = ac.imread(PathConverter.get_current_path("image", "MysticBuy.png"))
mystic_buy_confirmation = ac.imread(PathConverter.get_current_path("image", "MysticBuyConfirmation.png"))
refresh = ac.imread(PathConverter.get_current_path("image", "Refresh.png"))
refresh_confirm = ac.imread(PathConverter.get_current_path("image", "RefreshConfirm.png"))


class Utils:
    def __init__(self, serial: str):
        self.device = adbutils.device(serial)

    def __get_numpy_screenshot(self):
        return numpy.array(self.device.screenshot())

    def __find_image(self, source_img, target_img) -> dict[any, any]:
        return ac.find_template(source_img, target_img, 0.95)

    def __click_target(self, source_img, target_img, identifier="default"):
        tup = self.__find_image(source_img, target_img)
        result = tup.get("result")
        print(f"identifier: {identifier}, value: {str(tup)}")
        for click in range(0, random.randrange(2, 4)):
            self.device.click(result[0], result[1])
            time.sleep(0.2)

    def swipe_down(self):
        self.device.swipe(900, 500, 900, 0)

    def check_covenant(self, source_img) -> bool:
        return self.__find_image(source_img, covenant) is not None

    def buy_covenant(self, source_img):
        self.__click_target(source_img, covenant_buy, "buy covenant in store page")
        time.sleep(1)  # Delay is for animation
        self.__click_target(self.__get_numpy_screenshot(), covenant_buy_confirmation,
                            "buy covenant in confirmation page")
        time.sleep(1)

    def check_mystic(self, source_img) -> bool:
        return self.__find_image(source_img, mystic) is not None

    def buy_mystic(self, source_img):
        self.__click_target(source_img, mystic_buy, "buy mystic in store page")
        time.sleep(1)  # Delay is for animation
        self.__click_target(self.__get_numpy_screenshot(), mystic_buy_confirmation, "buy mystic in confirmation page")
        time.sleep(1)

    def refresh_shop(self):
        self.__click_target(self.__get_numpy_screenshot(), refresh, "refresh in store page")
        time.sleep(0.5)  # Delay is for animation
        self.__click_target(self.__get_numpy_screenshot(), refresh_confirm, "refresh in confirmation page")
        time.sleep(0.5)

    def check_and_buy_covenant(self) -> bool:
        store_page = self.__get_numpy_screenshot()
        if self.check_covenant(store_page):
            self.buy_covenant(store_page)
            return True
        return False

    def check_and_buy_mystic(self) -> bool:
        store_page = self.__get_numpy_screenshot()
        if self.check_mystic(store_page):
            self.buy_mystic(store_page)
            return True
        return False
