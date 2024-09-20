# -*- coding: utf-8 -*-

import customtkinter as tk

from utils.func import google_sync, timer_start, timer_stop, generate_report

class UI(tk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Time Checker")
        self.geometry("400x400")
        self.resizable(False, False)
        tk.set_default_color_theme("dark-blue") # fonctionne pas à voir pk
        
    def load(self):

        title = tk.CTkLabel(self, text="Time Checker", font=("Arial", 24))

        sync_button = tk.CTkButton(self, text="Synchroniser l'agenda Google", command=google_sync)

        quit_button = tk.CTkButton(self, text="Quitter", command=self.quit)

        play_button = tk.CTkButton(self, text="▶️", font=("Arial", 24), command=timer_start)
        report_button = tk.CTkButton(self, text="Générer le rapport mensuel", command=generate_report)

        title.pack(pady=20)
        sync_button.pack(pady=20)
        play_button.pack(pady=20)
        report_button.pack(pady=20)
        quit_button.pack(pady=20)
        