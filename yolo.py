from ultralytics import YOLO
import cv2

# Load the model (replace with your trained model path if available)
model = YOLO('yolov8n.pt')  # Replace with 'flower_model.pt' if you have one

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    # Draw results
    annotated_frame = results[0].plot()
    cv2.imshow("YOLOv8 - Flower Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
