import time
from typing import Tuple

import adbutils
import cv2
import numpy

import PathConverter
from automation.TaggedImage import TaggedImage


class Utilities:
    def __init__(self, serial: str):
        self.device = adbutils.device(serial)
        print(self.device.shell('wm size'))
        screen_size = self.device.shell('wm size').split(": ")[-1]
        self.screen_width, self.screen_height = map(int, screen_size.split("x"))
        self.is_wide_screen = self.screen_width/self.screen_height > 2
        print(f"Ratio: {self.screen_width/self.screen_height}")
        self.try_again = self.process_image_from_disk(PathConverter.get_current_path("image\\shop_refresh_asset",
                                                                                     "Try_Again.png"))
        self.position_cache: dict[str, tuple[int, int]] = {}

    def blur_image(self, image):
        return cv2.GaussianBlur(numpy.array(image), (5, 5), 0)

    def get_numpy_screenshot(self):
        """
        Get the blur version of screenshot in the adb device.
        """
        return self.blur_image(self.device.screenshot())

    def find_image(self, source_img, target_img, confidence: float = 0.82, color_sensitive: bool = False) -> dict[any, any]:
        """
        Find the target image in source image and return mid-point of found area.

        :param source_img: must be ndarray or UMat
        :param target_img: must be ndarray or UMat
        :param confidence: accuracy rate, from 0 to 1
        :param color_sensitive: will lower accuracy if color is different
        :return: the mid-point of found area if higher than designated confidence, otherwise empty {}
        """
        if color_sensitive:
            source_img = cv2.cvtColor(source_img, cv2.COLOR_BGR2HSV)
            target_img = cv2.cvtColor(target_img, cv2.COLOR_RGB2HSV)
        else:
            source_img = cv2.cvtColor(source_img, cv2.COLOR_BGR2GRAY)
            target_img = cv2.cvtColor(target_img, cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(source_img, target_img, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val >= confidence:
            top_left = max_loc
            bottom_right = (top_left[0] + target_img.shape[1], top_left[1] + target_img.shape[0])
            midpoint = int((top_left[0] + bottom_right[0])/2), int((top_left[1] + bottom_right[1])/2)
            return {"result": midpoint, "confidence": max_val}
        return {}

    def get_relative_coord(self, coord: Tuple[int, int]) -> Tuple[int, int]:
        """
        Find the relative position for cropped image or position from 1920x1080 adb device to increase accuracy.

        :param coord: must be in (width, height)
        :return: new relative (width, height) position
        """

        if self.is_wide_screen:
            return int(coord[0] / 1920 * (self.screen_width * 0.8)), int(coord[1] / 1080 * self.screen_height)
        else:
            return int(coord[0] / 1920 * self.screen_width), int(coord[1] / 1080 * self.screen_height)

    def process_image_from_disk(self, path: str) -> TaggedImage:
        """
        Process the image from given path to have unified image with identifier.

        :param path: must be relative path from PathConverter.get_current_path()
        :return: image with identifier
        """
        image_umat = cv2.imread(path)
        blur_umat = self.blur_image(image_umat)
        height, width = blur_umat.shape[:2]
        adjusted_image = cv2.resize(blur_umat, self.get_relative_coord((width, height)),
                                    interpolation=cv2.INTER_LINEAR_EXACT)
        return TaggedImage(adjusted_image, path.split("\\")[-1].split(".")[0])

    def save_image(self, save_file_name: str = "some.png"):
        """
        Take a screenshot from adb device and save it to local.

        :param save_file_name: desired filename
        """
        self.device.screenshot().save(save_file_name)

    def swipe_down(self):
        """
        Quickly swipe down the adb device screen
        """
        self.device.swipe(1400, 500, 1400, 200, 0.1)

    def click_target_offset(self, target_img=None, future_target_img=None, position_offset=(0, 0), retry_count: int = 3,
                            identifier: str = "default"):
        """
        Find and click the target image position on given offset position.
        Future_target_img is to make sure a successful click.

        :param target_img: must be ndarray or UMat, and it must be provided
        :param future_target_img: must be ndarray or UMat
        :param position_offset: click position offset from target_img
        :param retry_count: number of retries when target_img or future_target_img not found
        :param identifier: text to help where debugging if image not found
        """
        try:
            source_img = self.get_numpy_screenshot()
            target_img_pos = self.find_image(source_img, target_img)
            if bool(target_img_pos):
                print(f"identifier: {identifier}, img value: {str(target_img_pos)}")
                result = target_img_pos.get("result")
                relative_position_offset = self.get_relative_coord(position_offset)
                click_position = (result[0] + relative_position_offset[0], result[1] + relative_position_offset[1])
                self.device.click(click_position[0], click_position[1])
                # Check if it actually clicked if future_target_img is provided
                if future_target_img is not None:
                    time.sleep(0.5)
                    print("looking for future target img")
                    future_img_result = self.find_image(self.get_numpy_screenshot(), future_target_img)
                    print(f"future img result: {future_img_result}")
                    if not bool(future_img_result):
                        print("future image not found, trying again")
                        raise ValueError(f"Future Image Not Found For: {identifier}")
                return True
            if future_target_img is not None:
                print("check if future target image present")
                if bool(self.find_image(source_img, future_target_img)):
                    print("future target image presented")
                    return
            raise ValueError(f"Cannot Find Image: {identifier}")
        except Exception as e:
            print(f"Exception: {e}")
            if retry_count <= 0:
                raise
            is_expedition = self.check_and_refresh_expedition()
            print(f"Found expedition? {is_expedition}")
            # Re-click on target with new screenshot
            self.click_target_offset(target_img, future_target_img, position_offset, retry_count - 1, identifier)

    def click_target(self, target_tagged_img=None, future_tagged_imgs=None, retry_count: int = 3, timeout: float = 0.5,
                     color_sensitive: bool = False, confidence=0.8, identifier: str = "default",
                     cache_click: bool = True):
        """
        Find and click the target image, using caching technique to click faster.
        Future_target_img is to make sure a successful click.

        :param target_tagged_img: must be TaggedImage, and it must be provided
        :param future_tagged_imgs: must be TaggedImage, and it must be provided
        :param retry_count: number of retries when target_img or future_target_img not found
        :param timeout: keep looking for given image in a given timeout
        :param color_sensitive: will lower accuracy if color is different
        :param confidence: accuracy rate, from 0 to 1
        :param identifier: text to help where debugging if image not found
        :param cache_click: decide whether cacheing is needed or not
        """
        try:
            if type(future_tagged_imgs) is not list:
                future_tagged_imgs = [future_tagged_imgs]
            start_time = time.time()
            while time.time() - start_time < timeout:
                if target_tagged_img.tag in self.position_cache and cache_click:
                    position = self.position_cache.get(target_tagged_img.tag)
                    self.device.click(position[0], position[1])
                    time.sleep(0.5)
                    source_img = self.get_numpy_screenshot()
                    for tagged_img in future_tagged_imgs:
                        future_img_result = self.find_image(source_img=source_img,
                                                            target_img=tagged_img.image,
                                                            confidence=confidence, color_sensitive=color_sensitive)
                        # only return when the future image is found
                        # otherwise double check if image located in other place
                        if bool(future_img_result):
                            return
                    cache_click = False

                # If cache click failed or not intended to cache click
                # Normal click operation
                source_img = self.get_numpy_screenshot()
                target_img_pos = self.find_image(source_img=source_img, target_img=target_tagged_img.image,
                                                 confidence=confidence, color_sensitive=color_sensitive)
                if bool(target_img_pos):
                    result = target_img_pos.get("result")
                    self.position_cache[target_tagged_img.tag] = result
                    self.device.click(result[0], result[1])
                    time.sleep(0.5)
                    source_img = self.get_numpy_screenshot()
                    for tagged_img in future_tagged_imgs:
                        future_img_result = self.find_image(source_img=source_img, target_img=tagged_img.image,
                                                            confidence=confidence, color_sensitive=color_sensitive)
                        if bool(future_img_result):
                            return
                # Check again if the screenshot is already in correct page
                for tagged_img in future_tagged_imgs:
                    if bool(self.find_image(source_img=self.get_numpy_screenshot(), target_img=tagged_img.image,
                                            confidence=confidence, color_sensitive=color_sensitive)):
                        return
            raise ValueError(f"Cannot Find Image")
        except Exception as e:
            print(f"Exception: {e}, Identifier: {identifier}")
            if retry_count <= 0:
                raise ValueError(f"Exception: {e}, Identifier: {identifier}")
            is_expedition = self.check_and_refresh_expedition()
            print(f"Found expedition? {is_expedition}")
            if is_expedition:
                self.click_target(target_tagged_img, future_tagged_imgs, retry_count, 0.5, color_sensitive, confidence,
                                  identifier, False)
            self.click_target(target_tagged_img, future_tagged_imgs, retry_count - 1, 0.5, color_sensitive, confidence,
                              identifier, False)

    def check_and_refresh_expedition(self) -> bool:
        current_screenshot = self.get_numpy_screenshot()
        if self.find_image(source_img=current_screenshot, target_img=self.try_again.image):
            self.click_target(target_tagged_img=self.try_again, identifier="refresh expedition")
            time.sleep(2)  # Wait for a bit to check if there are some other expedition coming in
            self.swipe_down()  # Need to click at least once if another expedition popping up
            return True
        return False
