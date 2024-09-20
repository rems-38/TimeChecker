# -*- coding: utf-8 -*-

import tkinter as tk

class UI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("[Degecom] Time Checker")
        self.geometry("400x400")

    def init_frame(self):
        self.frame = tk.Frame(self)
        self.frame.pack()
