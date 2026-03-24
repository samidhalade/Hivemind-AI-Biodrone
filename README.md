# Biodrone-Hivemind-ai-
ai powered biodrone for pollination# Biodrone-Hivemind-ai

An AI-powered drone system for automated flower detection and pollination. This project leverages computer vision (YOLO), disease detection, and a Tkinter-based GUI to simulate and control a bio-pollination drone.

## Features

- 🌸 **Flower Detection:** Uses YOLOv8 for real-time flower detection via webcam.
- 🦠 **Disease Detection:** Input symptoms and get instant plant disease analysis.
- 🤖 **Pollination Simulation:** Visualizes drone pollination between flowers on a canvas.
- 🖥️ **User-Friendly GUI:** Control all features through an intuitive Tkinter interface.

## Getting Started

### Prerequisites

- Python 3.8+
- [ultralytics](https://github.com/ultralytics/ultralytics) (for YOLOv8)
- OpenCV (`opencv-python`)
- Tkinter (usually included with Python)
- numpy

Install dependencies:
```sh
pip install ultralytics opencv-python numpy

# Biodrone-Hivemind-ai

An AI-powered drone system for automated flower detection and pollination. This project leverages computer vision (YOLO), disease detection, and a Tkinter-based GUI to simulate and control a bio-pollination drone.


pip install ultralytics opencv-python numpy

Usage
1.Clone this repository:
git clone https://github.com/yourusername/Biodrone-Hivemind-ai.git
cd Biodrone-Hivemind-ai

2.Run the main application:
python drone_pollination_app.py

3.Use the GUI to:

Start the camera and detect flowers.
Check plant infection by entering symptoms.
Simulate the pollination process.

Files
drone_pollination_app.py — Main application with GUI and all features.
yolov8n.pt — YOLOv8 model weights (default, can be replaced with a custom-trained model).
flower_dataset.yaml — (Optional) Custom dataset config for training YOLO.
flower.jpg — Sample image for testing.
Acknowledgements
Ultralytics YOLO
OpenCV
Tkinter
License
MIT License
