from ultralytics import YOLO
import cv2
import numpy as np
import time
from database import connect_mouse_database, insert_mouse_check_data

conn = connect_mouse_database()
cam = "http://10.252.232.105:4747/video"
model = YOLO("yolov8n.pt")
results = model.predict(source="0", stream=True, imgsz=512, conf=0.5)
names = model.names
for r in results:
    l = [names[int(c)] for c in r.boxes.cls]
    if 'cat' in l:
        insert_mouse_check_data(conn, '1')
        print("CAT DETECTED!!")
    else:
        insert_mouse_check_data(conn, '0')
    time.sleep(0.1)