import queue
import threading
from multiprocessing import Queue

import ExceptionHandler
from ui.UIComponentEnum import UIThreadMessage as MsgEnum, LabelEnum, ButtonEnum
from ui.UIMessage import UIMessage


class ThreadHandler:
    def __init__(self, ui_listener, msg_queue):
        self.ui_listener = ui_listener
        self.thread = threading.Thread(target=self.fetch_msg, daemon=True)
        self.end_checking_ui_event = threading.Event()
        self.msg_queue: Queue = msg_queue

    def start_thread(self):
        self.end_checking_ui_event.clear()
        self.thread.start()

    def stop_thread(self):
        self.end_checking_ui_event.set()

    def fetch_msg(self):
        while not self.end_checking_ui_event.is_set():
            try:
                message: UIMessage = self.msg_queue.get(timeout=0.2)
                print(f"msg {message.msg_enum}, text: {message.text}")
                match message.msg_enum:
                    case MsgEnum.ADD_TO_LOG_FRAME:
                        self.ui_listener.add_label_to_log_frame(f"-------- {message.text} --------")

                    case MsgEnum.START_SHOP_REFRESH:
                        self.ui_listener.reset_log_frame()
                        self.ui_listener.set_button_state(ButtonEnum.ARENA_START, "disabled")
                        self.ui_listener.set_button_text(ButtonEnum.SHOP_REFRESH_START, "Stop Shop Refresh")

                    case MsgEnum.START_DAILY_ARENA:
                        self.ui_listener.reset_log_frame()
                        self.ui_listener.set_button_state(ButtonEnum.SHOP_REFRESH_START, "disabled")
                        self.ui_listener.set_button_text(ButtonEnum.ARENA_START, "Stop Arena Automation")

                    case MsgEnum.COVENANT_FOUND:
                        self.ui_listener.add_label_to_log_frame(f"Found Covenant Bookmark!")
                        current_count = int(self.ui_listener.get_label_text(LabelEnum.COVENANT_COUNT).split(": ")[-1])
                        label_text = f"Total Covenant: {current_count + 5}"
                        self.ui_listener.set_label_text(label_enum=LabelEnum.COVENANT_COUNT, text=label_text)

                    case MsgEnum.MYSTIC_FOUND:
                        self.ui_listener.add_label_to_log_frame(f"Found Mystic Bookmark!")
                        current_count = int(self.ui_listener.get_label_text(LabelEnum.MYSTIC_COUNT).split(": ")[-1])
                        label_text = f"Total Mystic: {current_count + 50}"
                        self.ui_listener.set_label_text(label_enum=LabelEnum.MYSTIC_COUNT, text=label_text)

                    case MsgEnum.RESET_LOG:
                        self.ui_listener.reset_log_frame()

                    case MsgEnum.ERROR:
                        ExceptionHandler.output_error_to_file(message.text)
                        self.ui_listener.add_label_to_log_frame(text=f"Error: {message.text}")
                        self.end_checking_ui_event.set()

                    case MsgEnum.STOP:
                        self.end_checking_ui_event.set()

                    case _:
                        print("something wrong")

            except queue.Empty:
                pass
        self.ui_listener.reset_ui_component()
        self.ui_listener.add_label_to_log_frame("####### Process Stopped #######")
        # self.ui_listener.update_ui()
