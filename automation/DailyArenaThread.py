import threading
import time

from ui.UIComponentEnum import *

class DailyArenaThread(threading.Thread):
    def __init__(self, daily_arena_instance, ui_listener):
        super().__init__(daemon=True)
        self.daily_arena_instance = daily_arena_instance
        self.ui_listener = ui_listener
        self.shutdown_event = threading.Event()

    def run(self):
        self.ui_listener.add_label_to_log_frame(text=f"####### Daily Arena Thread Started #######")
        try:
            self.daily_arena_instance.run_arena_automation(self.shutdown_event)
        except Exception as e:
            self.ui_listener.add_label_to_log_frame(text=f"Error:{str(e)}")
        finally:
            self.ui_listener.add_label_to_log_frame(text=f"####### Daily Arena Thread Ended #######")
            self.ui_listener.reset_ui_component(UIComponent.ARENA)

    def stop(self):
        self.shutdown_event.set()