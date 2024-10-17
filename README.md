# Illegal Parking Detection 🚗🚫

This project leverages **YOLO (You Only Look Once)** for real-time object detection and **Deep SORT** for multi-object tracking to build an intelligent **Illegal Parking Detection System**. The system monitors video streams, identifies vehicles entering restricted zones, and assigns unique IDs to each vehicle for consistent tracking. If a vehicle remains parked in the designated **illegal zone** for a defined **threshold time**, it is flagged as illegally parked. 🚦

![](https://github.com/Kevinjoythomas/Illegal-Parking-Detection/blob/main/img.png)

The combination of **YOLO** for object detection and **Deep SORT** for tracking ensures both accuracy and speed, making the solution viable for **real-time applications**. With the help of **vehicle ID tracking**, the system avoids duplicate detections and ensures the same vehicle is not misidentified across multiple frames. ⏱️ This allows smooth tracking even in crowded areas, making it effective for **urban parking management**.

Once a violation is detected, the system **saves the event** with relevant details such as the vehicle’s ID, timestamp, and captured image. 🗂️ The results can be stored as **JSON logs** and **JPEG images** for further analysis or evidence. This solution is ideal for **automated surveillance** in no-parking zones, mall driveways, or government-regulated areas, helping authorities enforce parking rules efficiently. 🚓

