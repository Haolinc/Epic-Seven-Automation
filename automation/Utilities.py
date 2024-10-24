import random
import time
import numpy
import adbutils
import aircv as ac
import PathConverter


class Utilities:
    def __init__(self, serial: str):
        self.device = adbutils.device(serial)

    def get_numpy_screenshot(self):
        return numpy.array(self.device.screenshot())

    def find_image(self, target_img) -> dict[any, any]:
        return ac.find_template(self.get_numpy_screenshot(), target_img, 0.95)

    def click_target(self, source_img, target_img, identifier="default"):
        tup = self.find_image(source_img, target_img)
        result = tup.get("result")
        print(f"identifier: {identifier}, value: {str(tup)}")
        for click in range(0, random.randrange(2, 4)):
            self.device.click(result[0], result[1])
            time.sleep(0.2)

    def swipe_down(self):
        self.device.swipe(900, 500, 900, 0)