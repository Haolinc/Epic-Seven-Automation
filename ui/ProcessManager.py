import multiprocessing
from ui.UIThreadHandler import MessageThreadHandler


class ProcessManager:
    def __init__(self, function=None, args=(), ui_listener=None, msg_queue=None):
        self.ui_listener = ui_listener
        self.process = multiprocessing.Process(target=function, args=args)
        self.process.daemon = True
        self.thread_handler = MessageThreadHandler(ui_listener=ui_listener, msg_queue=msg_queue)

    def start_process(self):
        self.process.start()
        self.thread_handler.start_thread()

    def stop_process(self):
        self.process.kill()
        self.thread_handler.stop_thread()

