# -*- coding: utf-8 -*-

import customtkinter as tk
import datetime

from utils.func import google_sync, timer_start, timer_stop, generate_report, get_hours, is_time

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

        self.start_time = is_time()
        if self.start_time:
            self.play_button = tk.CTkButton(self, text="⏸️", font=("Arial", 24), command=self.timer_stop)
        else:
            self.play_button = tk.CTkButton(self, text="▶️", font=("Arial", 24), command=self.timer_start)

        self.get_hours_button = tk.CTkButton(self, text="Obtenir le nombre d'heures", command=self.get_hours)
        self.report_button = tk.CTkButton(self, text="Générer le rapport mensuel", command=self.generate_report)

        self.title.pack(pady=20)
        self.sync_button.pack(pady=20)
        self.play_button.pack(pady=20)
        self.get_hours_button.pack(pady=10)
        self.report_button.pack(pady=10)
        self.quit_button.pack(pady=20)


    def google_sync(self):
        self.service_google = google_sync()
        self.sync_button.configure(text="Synchronisation terminée", state="disabled")


    def timer_start(self):
        self.start_time = timer_start()
        self.play_button.configure(text="⏸️", command=self.timer_stop)

    def timer_stop(self):
        timer_stop(self.service_google, self.start_time)
        self.play_button.configure(text="▶️", command=self.timer_start)


    def get_hours(self):
        infos = get_hours(self.service_google)
        total = sum(infos["duration"], datetime.timedelta())
        print(f"{total.days * 24 + total.seconds // 3600}:{(total.seconds % 3600) // 60:02}:{total.seconds % 60:02}")

    def generate_report(self):
        generate_report(self.service_google)