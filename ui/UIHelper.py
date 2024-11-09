import customtkinter as tk
from typing import Union

CTkFrames = Union[tk.CTkFrame, tk.CTkScrollableFrame]


def add_label_to_frame(frame: CTkFrames, text: str):
    label = tk.CTkLabel(frame, text=text)
    label.grid(sticky="nsew")
    frame._parent_canvas.yview_moveto(1.0)


def reset_frame(frame: CTkFrames):
    if frame.children:
        for widget in list(frame.children.values()):
            widget.destroy()
        frame.update()
