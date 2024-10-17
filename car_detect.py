from tracker import Tracker
from ultralytics import YOLO
from metrics import generate_color,calculate_containment_ratio,is_bbox_similar
import numpy as np
import configparser
import time
import ast
import cv2
from PIL import Image


#Configs
config = configparser.ConfigParser()
config.read("./config/config.ini")
show_gui = config['DEFAULT'].getboolean('show_gui')
print("SHOW GUI:",show_gui)
source = config['DEFAULT'].get('source')
print("Source File:",source)
points = config['DEFAULT'].get('coordinates_of_illegal_zone')
points = ast.literal_eval(f"[{points}]")
print("Illegal Points:",points)

# Load YOLO model
model = YOLO('./models/yolov10n.pt')

# Convert points to a numpy array
points_array = np.array(points, np.int32)
points_array = points_array.reshape((-1, 1, 2))

x, y, w, h = cv2.boundingRect(points_array)
polygon_bbox = (x, y, x + w, y + h)

# Open the video file
cap = cv2.VideoCapture(source)

# Tracker
tracker = Tracker()

# Initialize variables
car_last_seen = {}
car_stopped = {}
car_status = {}
colors = [generate_color() for _ in range(30)]
frame_count = 0


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count%7!=0:
        continue
    # Detect objects in the frame
    results = model(frame,imgsz = (288,480))
    detections = []
    height, width = frame.shape[:2]

# Print dimensions
    print(f"Width: {width}, Height: {height}")
    # Process detections
    for result in results:
        for detection in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            x1 = int(x1)
            x2 = int(x2)
            y2 = int(y2)
            y1 = int(y1)
            class_id = int(class_id)
            score = float(score)
            if class_id == 2:  # Assuming 'car' is the label for cars
                detections.append([x1, y1, x2, y2, score])
    
    # Get current time
    current_time = time.time()

    detections = np.array(detections)

    deep_sort_start_time = time.time()
    tracker.update(frame, detections)
    for track in tracker.tracks:
        bbox = track.bbox
        track_id = track.track_id
        track_id = int(track_id)
        x1, y1, x2, y2 = bbox
        x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
        if track_id in car_last_seen and is_bbox_similar(bbox, car_last_seen[track_id]):
            if track_id in car_stopped:
                if current_time-car_stopped[track_id]>4:
                    if calculate_containment_ratio(bbox,polygon_bbox):
                        car_status[track_id] = "Illegal"
                        print("ILLEGAL CAR DETECTED")
                    
        else:
                value = car_status.pop(track_id, None)
                car_last_seen[track_id] = bbox
                car_stopped[track_id] = time.time()

    for track in tracker.tracks:
        bbox = track.bbox
        track_id = track.track_id
        track_id = int(track_id)
        x1, y1, x2, y2 = bbox
        x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
        if track_id in car_status:
            cv2.rectangle(frame, (max(x1, 0), max(y1, 0)), (max(x2, 0), max(y2, 0)),(0,0,255), 3)        
            cv2.putText(frame, str(track_id)+": Illegal", (max(x1, 0), max(y1 - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)
        else:
            cv2.rectangle(frame, (max(x1, 0), max(y1, 0)), (max(x2, 0), max(y2, 0)),colors[int(int(track_id) % len(colors))], 3)        
            cv2.putText(frame, str(track_id)+": Car", (max(x1, 0), max(y1 - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, colors[int(int(track_id) % len(colors))], 2)


    # Draw the rhombus on the frame
    cv2.polylines(frame, [points_array], isClosed=True, color=(0, 0, 255), thickness=2)

    # Display the frame
    cv2.imshow("YOLO Detection with SORT Tracking", frame)

    # Wait for a key press and check if it's the escape key
    if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the escape key
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()


