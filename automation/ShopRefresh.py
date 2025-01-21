import threading
import time

import PathConverter
from automation.Utilities import Utilities
from ui.UIComponentEnum import *


class ShopRefresh:
    thread_shutdown = threading.Event()

    def __init__(self, utilities: Utilities, listener):
        self.utilities = utilities
        self.covenant_count = 0
        self.mystic_count = 0
        self.ui_listener = listener

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

    def buy_covenant(self) -> bool:
        if not self.utilities.click_by_position(target_img=self.covenant,
                                                future_target_img=self.covenant_buy_confirmation,
                                                position_offset=(850, 25),
                                                identifier="buy covenant in store page"):
            return False
        if not self.utilities.better_click_target(target_img=self.covenant_buy_confirmation,
                                                  future_target_img=self.shop_icon,
                                                  identifier="buy covenant in confirmation page"):
            return False
        return True

    def check_mystic(self) -> bool:
        return bool(self.utilities.find_image(source_img=self.utilities.get_numpy_screenshot(), target_img=self.mystic,
                                              confidence=0.93))

    def buy_mystic(self) -> bool:
        if not self.utilities.click_by_position(target_img=self.mystic,
                                                future_target_img=self.mystic_buy_confirmation,
                                                position_offset=(850, 25),
                                                identifier="buy mystic in store page"):
            return False
        if not self.utilities.better_click_target(target_img=self.mystic_buy_confirmation,
                                                  future_target_img=self.shop_icon,
                                                  identifier="buy mystic in confirmation page"):
            return False
        return True

    def refresh_shop(self) -> bool:
        if not self.utilities.better_click_target(target_img=self.refresh, future_target_img=self.refresh_confirm,
                                                  identifier="refresh in store page"):
            return False
        if not self.utilities.better_click_target(target_img=self.refresh_confirm,
                                                  future_target_img=self.shop_icon,
                                                  identifier="refresh in confirmation page"):
            return False
        return True

    def check_bookmark_and_update_log(self):
        if self.check_covenant():
            if self.buy_covenant():
                self.ui_listener.add_label_to_log_frame(text="Found Covenant Bookmark!")
                self.covenant_count += 5
                self.ui_listener.set_label_text(label_enum=LabelEnum.COVENANT_COUNT,
                                                text="Total Covenant: " + str(self.covenant_count))
            # This only happens when multiple retry attempt fails
            else:
                self.ui_listener.add_label_to_log_frame(text="Covenant Purchase Fail, Stopping the application")
                self.stop_shop_refresh()
                return
        if self.check_mystic():
            if self.buy_mystic():
                self.ui_listener.add_label_to_log_frame(text="Found Mystic Bookmark!")
                self.mystic_count += 50
                self.ui_listener.set_label_text(label_enum=LabelEnum.MYSTIC_COUNT,
                                                text="Total Mystic: " + str(self.mystic_count))
            # This only happens when multiple retry attempt fails
            else:
                self.ui_listener.add_label_to_log_frame(text="Mystic Purchase Fail, Stopping the application")
                self.stop_shop_refresh()

    def start_store_fresh_iteration(self):
        total_iteration: int = self.ui_listener.get_entry_count(EntryEnum.SHOP_REFRESH_COUNT_ENTRY)
        current_iteration = 0
        self.ui_listener.reset_log_frame()
        self.ui_listener.add_label_to_log_frame(text=f"Initial Search")
        while current_iteration < total_iteration and not self.thread_shutdown.is_set():
            self.check_bookmark_and_update_log()
            if self.thread_shutdown.is_set():
                break
            self.utilities.swipe_down()
            time.sleep(0.5)
            self.check_bookmark_and_update_log()
            # Check shutdown signal before refresh
            if self.thread_shutdown.is_set():
                break
            # When refresh failed, Stop the application
            if not self.refresh_shop():
                self.ui_listener.add_label_to_log_frame(text="Refresh Shop Fail, Stopping the application")
                break
            current_iteration += 1
            self.ui_listener.add_label_to_log_frame(text=f"--------Iteration: {current_iteration}--------")
        # Check again for last refresh ONLY when thread is not exiting
        if not self.thread_shutdown.is_set():
            self.check_bookmark_and_update_log()
            self.utilities.swipe_down()
            time.sleep(0.5)
            self.check_bookmark_and_update_log()
        self.ui_listener.add_label_to_log_frame(text="####### Process Stopped #######")
        self.ui_listener.reset_ui_component(UIComponent.SHOP_REFRESH)

    def start_shop_refresh_with_thread(self):
        self.thread_shutdown.clear()
        threading.Thread(target=self.start_store_fresh_iteration, daemon=True).start()

    def stop_shop_refresh(self):
        self.thread_shutdown.set()
