import time

import aircv as ac
import PathConverter
from automation.Utilities import Utilities

covenant = ac.imread(PathConverter.get_current_path("image\\shop_refresh_asset", "Covenant.png"))
covenant_buy = ac.imread(PathConverter.get_current_path("image\\shop_refresh_asset", "CovenantBuy.png"))
covenant_buy_confirmation = ac.imread(
    PathConverter.get_current_path("image\\shop_refresh_asset", "CovenantBuyConfirmation.png"))
mystic = ac.imread(PathConverter.get_current_path("image\\shop_refresh_asset", "Mystic.png"))
mystic_buy = ac.imread(PathConverter.get_current_path("image\\shop_refresh_asset", "MysticBuy.png"))
mystic_buy_confirmation = ac.imread(
    PathConverter.get_current_path("image\\shop_refresh_asset", "MysticBuyConfirmation.png"))
refresh = ac.imread(PathConverter.get_current_path("image\\shop_refresh_asset", "Refresh.png"))
refresh_confirm = ac.imread(PathConverter.get_current_path("image\\shop_refresh_asset", "RefreshConfirm.png"))


class ShopRefresh:
    def __init__(self, utilities: Utilities):
        self.utilities = utilities

    def check_covenant(self) -> bool:
        return self.utilities.find_image(source_img=self.utilities.get_numpy_screenshot(),
                                         target_img=covenant) is not None

    def buy_covenant(self) -> bool:
        if not self.utilities.shop_refresh_click_target(source_img=self.utilities.get_numpy_screenshot(),
                                                        target_img=covenant_buy,
                                                        identifier="buy covenant in store page"):
            return False
        time.sleep(0.2)  # Delay is for animation
        if not self.utilities.shop_refresh_click_target(source_img=self.utilities.get_numpy_screenshot(),
                                                        target_img=covenant_buy_confirmation,
                                                        identifier="buy covenant in confirmation page"):
            return False
        time.sleep(0.2)
        return True

    def check_mystic(self) -> bool:
        return self.utilities.find_image(source_img=self.utilities.get_numpy_screenshot(),
                                         target_img=mystic) is not None

    def buy_mystic(self) -> bool:
        if not self.utilities.shop_refresh_click_target(source_img=self.utilities.get_numpy_screenshot(),
                                                        target_img=mystic_buy,
                                                        identifier="buy mystic in store page"):
            return False
        time.sleep(0.2)  # Delay is for animation
        if not self.utilities.shop_refresh_click_target(source_img=self.utilities.get_numpy_screenshot(),
                                                        target_img=mystic_buy_confirmation,
                                                        identifier="buy mystic in confirmation page"):
            return False
        time.sleep(0.2)
        return True

    def refresh_shop(self) -> bool:
        if not self.utilities.shop_refresh_click_target(source_img=self.utilities.get_numpy_screenshot(),
                                                        target_img=refresh,
                                                        identifier="refresh in store page"):
            return False
        time.sleep(0.2)  # Delay is for animation
        if not self.utilities.shop_refresh_click_target(source_img=self.utilities.get_numpy_screenshot(),
                                                        target_img=refresh_confirm,
                                                        identifier="refresh in confirmation page"):
            return False
        time.sleep(0.2)
        return True

    # temporary function holder
    def swipe_down(self):
        self.utilities.swipe_down()
