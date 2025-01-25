import time
import PathConverter
from automation.Utilities import Utilities
from ui.UIComponentEnum import UIThreadMessage
from ui.UIMessage import UIMessage


class ShopRefresh:
    def __init__(self, utilities: Utilities, msg_queue):
        self.utilities = utilities
        self.msg_queue = msg_queue
        self.covenant = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "Covenant.png"))
        self.covenant_buy_confirmation = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "CovenantBuyConfirmation.png"))
        self.mystic = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "Mystic.png"))
        self.mystic_buy_confirmation = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "MysticBuyConfirmation.png"))
        self.refresh = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "Refresh.png"))
        self.refresh_confirm = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "RefreshConfirm.png"))
        self.shop_icon = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "Shop.png"))

    def check_covenant(self) -> bool:
        return bool(self.utilities.find_image(source_img=self.utilities.get_numpy_screenshot(), target_img=self.covenant,
                                              confidence=0.93))

    def buy_covenant(self) -> str:
        if not self.utilities.click_by_position(target_img=self.covenant,
                                                future_target_img=self.covenant_buy_confirmation,
                                                position_offset=(850, 25),
                                                identifier="buy covenant in store page"):
            return "Covenant Buy Button Not Found"
        if not self.utilities.better_click_target(target_img=self.covenant_buy_confirmation,
                                                  future_target_img=self.shop_icon,
                                                  identifier="buy covenant in confirmation page"):
            return "Covenant Buy Confirm Button Not Found"
        return "Success"

    def check_mystic(self) -> bool:
        return bool(self.utilities.find_image(source_img=self.utilities.get_numpy_screenshot(), target_img=self.mystic,
                                              confidence=0.93))

    def buy_mystic(self) -> str:
        if not self.utilities.click_by_position(target_img=self.mystic,
                                                future_target_img=self.mystic_buy_confirmation,
                                                position_offset=(850, 25),
                                                identifier="buy mystic in store page"):
            return "Mystic Buy Button Not Found"
        if not self.utilities.better_click_target(target_img=self.mystic_buy_confirmation,
                                                  future_target_img=self.shop_icon,
                                                  identifier="buy mystic in confirmation page"):
            return "Mystic Buy Confirm Button Not Found"
        return "Success"

    def refresh_shop(self) -> str:
        if not self.utilities.better_click_target(target_img=self.refresh, future_target_img=self.refresh_confirm,
                                                  identifier="refresh in store page"):
            return "Refresh Button Not Found"
        if not self.utilities.better_click_target(target_img=self.refresh_confirm,
                                                  future_target_img=self.shop_icon,
                                                  identifier="refresh in confirmation page"):
            return "Refresh Confirm Button Not Found"
        return "Success"

    def check_bookmark_and_update_log(self):
        if self.check_covenant():
            buy_result = self.buy_covenant()
            if buy_result == "Success":
                self.msg_queue.put(UIMessage(UIThreadMessage.COVENANT_FOUND))
            # This only happens when multiple retry attempt fails
            else:
                raise ValueError(buy_result)
        if self.check_mystic():
            buy_result = self.buy_mystic()
            if buy_result == "Success":
                self.msg_queue.put(UIMessage(UIThreadMessage.MYSTIC_FOUND))
            # This only happens when multiple retry attempt fails
            else:
                raise ValueError(buy_result)

    def start_store_fresh_iteration(self, total_iteration: int):
        current_iteration = 0
        self.msg_queue.put(UIMessage(UIThreadMessage.START_SHOP_REFRESH))
        self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, "Initial Search"))
        try:
            while current_iteration < total_iteration:
                self.check_bookmark_and_update_log()
                self.utilities.swipe_down()
                time.sleep(0.5)
                self.check_bookmark_and_update_log()
                # When refresh failed, Stop the application
                refresh_result = self.refresh_shop()
                if refresh_result != "Success":
                    raise ValueError(refresh_result)
                current_iteration += 1
                self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, f"Iteration: {current_iteration}"))
            # Check again for last refresh
            self.check_bookmark_and_update_log()
            self.utilities.swipe_down()
            time.sleep(0.5)
            self.check_bookmark_and_update_log()
            self.msg_queue.put(UIMessage(UIThreadMessage.STOP))
        except Exception as e:
            self.msg_queue.put(UIMessage(UIThreadMessage.ERROR, str(e)))
