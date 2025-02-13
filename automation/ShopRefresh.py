import time
import PathConverter
from automation.Utilities import Utilities
from ui.UIComponentEnum import UIThreadMessage
from ui.UIMessage import UIMessage


class ShopRefresh:
    """
    Secret shop bookmark purchase automation class
    """
    def __init__(self, utilities: Utilities, msg_queue):
        self.utilities = utilities
        self.msg_queue = msg_queue
        self.covenant = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "Covenant.png"))
        self.covenant_buy_confirmation = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "Covenant_Buy_Confirmation.png"))
        self.mystic = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "Mystic.png"))
        self.mystic_buy_confirmation = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "Mystic_Buy_Confirmation.png"))
        self.refresh = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "Refresh.png"))
        self.refresh_confirm = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "Refresh_Confirm.png"))
        self.shop_icon = utilities.process_image_from_disk(
            PathConverter.get_current_path("image\\shop_refresh_asset", "Shop.png"))

    def __check_covenant(self) -> bool:
        return bool(self.utilities.find_image(source_img=self.utilities.get_numpy_screenshot(),
                                              target_img=self.covenant.image, confidence=0.93, color_sensitive=True))

    def __buy_covenant(self):
        self.utilities.click_target_offset(target_img=self.covenant.image, future_target_img=self.covenant_buy_confirmation.image,
                                           position_offset=(850, 25), identifier="Buy Covenant Button")
        self.utilities.click_target(target_tagged_img=self.covenant_buy_confirmation, future_tagged_imgs=self.shop_icon,
                                    identifier="Buy Covenant Confirmation Button")
        self.msg_queue.put(UIMessage(UIThreadMessage.COVENANT_FOUND))

    def __check_mystic(self) -> bool:
        return bool(self.utilities.find_image(source_img=self.utilities.get_numpy_screenshot(),
                                              target_img=self.mystic.image, confidence=0.93, color_sensitive=True))

    def __buy_mystic(self):
        self.utilities.click_target_offset(target_img=self.mystic.image, future_target_img=self.mystic_buy_confirmation.image,
                                           position_offset=(850, 25), identifier="Buy Mystic Button")
        self.utilities.click_target(target_tagged_img=self.mystic_buy_confirmation, future_tagged_imgs=self.shop_icon,
                                    identifier="Buy Mystic Confirmation Button")
        self.msg_queue.put(UIMessage(UIThreadMessage.MYSTIC_FOUND))

    def __refresh_shop(self):
        self.utilities.click_target(target_tagged_img=self.refresh, future_tagged_imgs=self.refresh_confirm,
                                    identifier="Refresh Button")
        self.utilities.click_target(target_tagged_img=self.refresh_confirm, future_tagged_imgs=self.shop_icon,
                                    identifier="Refresh Confirmation Button")

    def __check_bookmark_and_update_log(self):
        if self.__check_covenant():
            self.__buy_covenant()
        if self.__check_mystic():
            self.__buy_mystic()

    def start_store_fresh_iteration(self, total_iteration: int):
        current_iteration = 0
        self.msg_queue.put(UIMessage(UIThreadMessage.START_SHOP_REFRESH))
        self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, "Initial Search"))
        try:
            while current_iteration < total_iteration:
                self.__check_bookmark_and_update_log()
                self.utilities.swipe_down()
                time.sleep(0.5)
                self.__check_bookmark_and_update_log()
                self.__refresh_shop()
                current_iteration += 1
                self.msg_queue.put(UIMessage(UIThreadMessage.ADD_TO_LOG_FRAME, f"Iteration: {current_iteration}"))
            # Check again for last refresh
            self.__check_bookmark_and_update_log()
            self.utilities.swipe_down()
            time.sleep(0.5)
            self.__check_bookmark_and_update_log()
            self.msg_queue.put(UIMessage(UIThreadMessage.STOP))
        except Exception as e:
            self.msg_queue.put(UIMessage(UIThreadMessage.ERROR, str(e)))
