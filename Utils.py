import random
import time

import numpy
from adbutils import adb
import aircv as ac

covenant = ac.imread("./image/Covenant.png")
covenant_buy = ac.imread("./image/CovenantBuy.png")
covenant_buy_confirmation = ac.imread("./image/CovenantBuyConfirmation.png")
mystic = ac.imread("./image/Mystic.png")
mystic_buy = ac.imread("./image/MysticBuy.png")
mystic_buy_confirmation = ac.imread("./image/MysticBuyConfirmation.png")
refresh = ac.imread("./image/Refresh.png")
refresh_confirm = ac.imread("./image/RefreshConfirm.png")
device = adb.device()


def get_numpy_screenshot():
    return numpy.array(device.screenshot())


def find_image(source_img, target_img):
    return ac.find_template(source_img, target_img, 0.95)


def click_target(source_img, target_img, identifier="default"):
    tup = find_image(source_img, target_img)
    result = tup.get("result")
    print(f"identifier: {identifier}, value: {str(tup)}")
    for click in range(0, random.randrange(2, 4)):
        device.click(result[0], result[1])
        time.sleep(0.2)


def check_covenant(source_img) -> bool:
    return find_image(source_img, covenant) is not None


def buy_covenant(source_img):
    click_target(source_img, covenant_buy, "buy covenant in store page")
    time.sleep(1)  # Delay is for animation
    click_target(get_numpy_screenshot(), covenant_buy_confirmation,
                 "buy covenant in confirmation page")
    time.sleep(1)


def check_mystic(source_img) -> bool:
    return find_image(source_img, mystic) is not None


def buy_mystic(source_img):
    click_target(source_img, mystic_buy, "buy mystic in store page")
    time.sleep(1)  # Delay is for animation
    click_target(get_numpy_screenshot(), mystic_buy_confirmation, "buy mystic in confirmation page")
    time.sleep(1)


def refresh_shop():
    click_target(get_numpy_screenshot(), refresh, "refresh in store page")
    time.sleep(0.5)  # Delay is for animation
    click_target(get_numpy_screenshot(), refresh_confirm, "refresh in confirmation page")
    time.sleep(0.5)


def check_and_buy_covenant() -> bool:
    store_page = get_numpy_screenshot()
    if check_covenant(store_page):
        buy_covenant(store_page)
        return True
    return False


def check_and_buy_mystic() -> bool:
    store_page = get_numpy_screenshot()
    if check_mystic(store_page):
        buy_mystic(store_page)
        return True
    return False



