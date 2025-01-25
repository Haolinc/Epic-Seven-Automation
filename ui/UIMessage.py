from ui.UIComponentEnum import UIThreadMessage


class UIMessage:
    def __init__(self, msg_enum: UIThreadMessage, text: str = "default text"):
        self.msg_enum = msg_enum
        self.text = text
