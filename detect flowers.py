import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

# Simulated backend functions
def detect_flower():
    return random.choice(["flower", "no_flower"])

def check_infection(symptom):
    database = {
        "yellow spots": "Leaf spot disease",
        "wilting": "Bacterial wilt",
        "white powder": "Powdery mildew"
    }
    for key in database:
        if key in symptom.lower():
            return database[key]
    return "No known infection"

def pollinate():
    time.sleep(2)  # Simulate delay
    return "Pollination successful"

# GUI Application
class DronePollinationApp:
    def __init__(self, root):  # ✅ Fixed
        self.root = root
        self.root.title("AI Bio-Pollination Drone")
        self.root.geometry("400x400")
        self.root.config(bg="#e6ffe6")

        self.status_label = tk.Label(root, text="Drone Status: Idle", bg="#e6ffe6", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.detect_button = tk.Button(root, text="Detect Flower", command=self.detect_flower_gui, bg="#a3d9a5", font=("Arial", 12))
        self.detect_button.pack(pady=10)

        self.symptom_entry = tk.Entry(root, width=40)
        self.symptom_entry.insert(0, "Enter symptoms (e.g. yellow spots)")
        self.symptom_entry.pack(pady=10)

        self.infection_button = tk.Button(root, text="Check Infection", command=self.check_infection_gui, bg="#f7c59f", font=("Arial", 12))
        self.infection_button.pack(pady=10)

        self.pollinate_button = tk.Button(root, text="Start Pollination", command=self.start_pollination_gui, bg="#ffb347", font=("Arial", 12))
        self.pollinate_button.pack(pady=10)

    def detect_flower_gui(self):
        flower = detect_flower()
        self.status_label.config(text=f"Flower Detection: {flower}")
        if flower == "no_flower":
            messagebox.showinfo("Result", "No flower detected.")
        else:
            messagebox.showinfo("Result", "Flower detected!")

    def check_infection_gui(self):
        symptoms = self.symptom_entry.get()
        disease = check_infection(symptoms)
        self.status_label.config(text=f"Infection: {disease}")
        messagebox.showinfo("Disease Detection", f"Disease: {disease}")

    def start_pollination_gui(self):
        def task():
            self.status_label.config(text="Pollination in progress...")
            result = pollinate()
            self.status_label.config(text=result)
            messagebox.showinfo("Pollination", result)
        threading.Thread(target=task).start()

# ✅ Fixed entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = DronePollinationApp(root)
    root.mainloop()
