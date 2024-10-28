import random
import time
from turtledemo.penrose import start

import numpy
import adbutils
import aircv as ac
import PathConverter


class Utilities:
    def __init__(self, serial: str):
        self.device = adbutils.device(serial)

    def get_numpy_screenshot(self):
        return numpy.array(self.device.screenshot())

    def find_image(self, source_img, target_img) -> dict[any, any]:
        return ac.find_template(source_img, target_img, 0.95)

    def save_image(self):
        self.device.screenshot().save("some.png")

    def click_target(self, source_img, target_img, identifier="default"):
        tup = self.find_image(source_img, target_img)
        result = tup.get("result")
        print(f"identifier: {identifier}, value: {str(tup)}")
        self.device.click(result[0], result[1])
        time.sleep(0.2)

    def swipe_down(self):
        self.device.swipe(900, 500, 900, 0)

    def wait_for_button_and_click(self, target_img, description="default", timeout = 5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            print("looping while")
            if self.find_image(self.get_numpy_screenshot(), target_img):
                self.click_target(self.get_numpy_screenshot(),target_img)
                return True
            else:
                time.sleep(1)
        raise Exception(f"Timeout: {description} not found within {timeout} seconds")

    def click_center_of_screen(self):
        center_x = 500
        center_y = 500
        self.device.click(center_x, center_y)


