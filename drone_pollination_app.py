import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import cv2
from ultralytics import YOLO
import numpy as np


def check_infection(symptom_input):
    database = {
        "yellow spots": "Leaf Spot Disease",
        "wilting": "Bacterial Wilt",
        "white powder": "Powdery Mildew",
        "brown patches": "Blight",
        "root rot": "Root Rot Fungus",
        "leaf curl": "Leaf Curl Virus",
        "black spots": "Black Spot Fungus",
        "leaf blast": "Rice Blast",
        "stem rust": "Stem Rust (Wheat)",
        "late blight": "Late Blight (Tomato/Potato)",
        "early blight": "Early Blight (Tomato/Potato)",
        "downy mildew": "Downy Mildew (Grapes/Cucurbits)",
        "anthracnose": "Anthracnose (Mango/Beans)",
        "leaf spot": "Bacterial Leaf Spot",
        "tobacco mosaic": "Tobacco Mosaic Virus (TMV)",
        "curly top": "Curly Top Virus",
        "smut": "Smut (Corn/Sorghum)",
        "mosaic": "Mosaic Virus (Multiple Crops)",
        "scab": "Apple Scab",
        "leaf scorch": "Leaf Scorch (Wheat)"
    }

    found_diseases = []
    input_symptoms = [s.strip().lower() for s in symptom_input.split(',')]

    for symptom in input_symptoms:
        for key in database:
            if key in symptom:
                found_diseases.append(f"{symptom.title()} → {database[key]}")
                break
        else:
            found_diseases.append(f"{symptom.title()} → No known infection")

    return "\n".join(found_diseases)


class DronePollinationApp:
    def _init_(self, root):
        self.root = root
        self.root.title("🌸 AI Bio-Pollination Drone")
        self.root.geometry("800x700")
        self.root.config(bg="#f4f9f4")

        header = tk.Label(root, text="🌼 AI Bio-Pollination Drone Interface", font=("Arial", 20, "bold"),
                          bg="#f4f9f4", fg="#2d6a4f")
        header.pack(pady=10)

        self.status_label = tk.Label(root, text="Drone Status: Idle", bg="#f4f9f4", font=("Arial", 12),
                                     fg="#40916c")
        self.status_label.pack(pady=5)

        self.console = scrolledtext.ScrolledText(root, height=12, width=85, font=("Courier", 10), bg="#ffffff")
        self.console.pack(pady=10)
        self.log("System initialized... Ready.")

        self.start_camera_button = tk.Button(root, text="🎥 Start Camera & Detect Flower", command=self.start_camera,
                                             bg="#b7e4c7", font=("Arial", 12), width=30)
        self.start_camera_button.pack(pady=10)

        self.symptom_entry = tk.Entry(root, width=60, font=("Arial", 12))
        self.symptom_entry.insert(0, "Enter symptoms (e.g. late blight)")
        self.symptom_entry.pack(pady=10)

        self.infection_button = tk.Button(root, text="🧪 Check Infection", command=self.check_infection_gui,
                                          bg="#ffc9de", font=("Arial", 12), width=30)
        self.infection_button.pack(pady=10)

        self.pollinate_button = tk.Button(root, text="🌼 Start Pollination Process", command=self.start_pollination_process,
                                          bg="#d8f3dc", font=("Arial", 12), width=30)
        self.pollinate_button.pack(pady=10)

        self.canvas = tk.Canvas(root, width=600, height=200, bg="#ffffff")
        self.canvas.pack(pady=10)

        self.source_flower = self.canvas.create_oval(50, 80, 100, 130, fill="pink", outline="red")
        self.target_flower = self.canvas.create_oval(500, 80, 550, 130, fill="yellow", outline="orange")
        self.drone = self.canvas.create_rectangle(60, 60, 90, 90, fill="gray")

        self.camera_running = False

        # Load YOLO model (use your trained model path or yolov8n.pt for default)
        self.yolo_model = YOLO("yolov8n.pt")

    def log(self, message):
        self.console.insert(tk.END, f"> {message}\n")
        self.console.see(tk.END)

    def start_camera(self):
        if not self.camera_running:
            self.camera_running = True
            self.status_label.config(text="Drone Status: Camera Started - Detecting Flower...")
            self.log("Starting camera for flower detection...")
            threading.Thread(target=self.camera_loop, daemon=True).start()
            self.start_camera_button.config(text="🛑 Stop Camera")
        else:
            self.camera_running = False
            self.status_label.config(text="Drone Status: Camera Stopped")
            self.log("Camera stopped.")
            self.start_camera_button.config(text="🎥 Start Camera & Detect Flower")

    def detect_flower_by_yolo(self, frame):
        results = self.yolo_model(frame)[0]  # Run YOLO inference

        flower_detected = False
        detected_classes = []

        for box in results.boxes:
            cls = int(box.cls.cpu().numpy())  # Class index as int
            class_name = self.yolo_model.names[cls]
            detected_classes.append(class_name)

            # Draw bbox and label on frame
            xyxy = box.xyxy.cpu().numpy()[0]  # bounding box coordinates [x1, y1, x2, y2]
            conf = box.conf.cpu().numpy()[0]  # confidence score

            x1, y1, x2, y2 = map(int, xyxy)
            color = (0, 255, 0)  # Green box for detected flowers
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            label = f"{class_name} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            if "flower" in class_name.lower():
                flower_detected = True

        self.log(f"Detected YOLO classes: {detected_classes}")

        return flower_detected, frame

    def camera_loop(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.log("❌ Cannot open camera")
            messagebox.showerror("Error", "Cannot open camera")
            self.camera_running = False
            self.status_label.config(text="Drone Status: Camera Error")
            self.start_camera_button.config(text="🎥 Start Camera & Detect Flower")
            return

        self.log("📷 Camera opened. Press 'q' in the camera window to stop.")

        flower_already_notified = False

        while self.camera_running:
            ret, frame = cap.read()
            if not ret:
                self.log("❌ Can't receive frame. Exiting camera...")
                break

            flower_found, display_frame = self.detect_flower_by_yolo(frame)

            text = "Flower Detected!" if flower_found else "No Flower Detected"
            color = (0, 255, 0) if flower_found else (0, 0, 255)
            cv2.putText(display_frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.imshow('Drone Camera Feed - Press q to Quit', display_frame)

            if flower_found and not flower_already_notified:
                self.log("✅ Flower detected by YOLO!")
                self.status_label.config(text="Drone Status: Flower Detected - Ready to Pollinate")
                messagebox.showinfo("Flower Detection", "🌸 Flower detected by AI drone camera!")
                flower_already_notified = True

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.camera_running = False
                break

        cap.release()
        cv2.destroyAllWindows()
        self.status_label.config(text="Drone Status: Camera Stopped")
        self.log("Camera feed closed.")
        self.start_camera_button.config(text="🎥 Start Camera & Detect Flower")

    def check_infection_gui(self):
        symptoms = self.symptom_entry.get()
        results = check_infection(symptoms)
        self.status_label.config(text="Infection Results Logged")
        self.log("Infection Check Results:")
        self.log(results)
        messagebox.showinfo("Disease Detection", f"Results:\n{results}")

    def start_pollination_process(self):
        self.status_label.config(text="Drone Status: Pollination Started")
        self.log("🌸 Step 1: Pollination started...")
        self.root.update()
        time.sleep(1)

        self.log("🌿 Step 2: Collecting pollens from the source flower...")
        self.status_label.config(text="Drone Status: Collecting Pollens")
        self.root.update()
        time.sleep(2)

        self.log("🌼 Step 3: Flying to target flower...")
        self.status_label.config(text="Drone Status: Flying to Target")
        self.root.update()
        self.animate_drone_movement()

        self.log("💧 Step 4: Dropping pollens on the target flower...")
        self.status_label.config(text="Drone Status: Dropping Pollens")
        self.root.update()
        time.sleep(2)

        self.log("✅ Step 5: Pollination successful!")
        self.status_label.config(text="Drone Status: Pollination Completed")
        messagebox.showinfo("Pollination Status", "✅ Pollination was successful!")

    def animate_drone_movement(self):
        for _ in range(50):
            self.canvas.move(self.drone, 9, 0)
            self.canvas.update()
            time.sleep(0.05)


if __name__ == "__main__":
    # your main function or logic call here

    root = tk.Tk()
    app = DronePollinationApp(root)
    root.mainloop()