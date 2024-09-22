# -*- coding: utf-8 -*-

import customtkinter as tk

from utils.func import google_sync, timer_start, timer_stop, generate_report

class UI(tk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Time Checker")
        self.geometry("400x400")
        self.resizable(False, False)
        
    def load(self):

        self.title = tk.CTkLabel(self, text="Time Checker", font=("Arial", 24))

        self.sync_button = tk.CTkButton(self, text="Synchroniser l'agenda Google", command=self.google_sync)

        self.quit_button = tk.CTkButton(self, text="Quitter", command=self.quit)

        self.play_button = tk.CTkButton(self, text="▶️", font=("Arial", 24), command=self.timer_start)
        self.report_button = tk.CTkButton(self, text="Générer le rapport mensuel", command=self.generate_report)

        self.title.pack(pady=20)
        self.sync_button.pack(pady=20)
        self.play_button.pack(pady=20)
        self.report_button.pack(pady=20)
        self.quit_button.pack(pady=20)


    def google_sync(self):
        self.service_google = google_sync()


    def timer_start(self):
        self.start_time = timer_start()
        self.play_button.configure(text="⏸️", command=self.timer_stop)

    def timer_stop(self):
        timer_stop(self.service_google, self.start_time)
        self.play_button.configure(text="▶️", command=self.timer_start)


    def generate_report(self):
        generate_report(self.service_google)