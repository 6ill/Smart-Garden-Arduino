from flask import Flask, render_template, request, jsonify
import serial
# import sqlite3
from database import connect_database, insert_sensor_data, fetch_mouse_check_data
import time
from datetime import datetime
from ultralytics import YOLO
import cv2
import numpy as np
from threading import Thread

app = Flask(__name__)
ser = serial.Serial('COM3', 9600)  
conn = connect_database()

# model = YOLO("yolov8n.pt")
# results = model.predict(source=0, stream=True, imgsz=512, conf=0.5)
# names = model.names
# print("aa")
# for r in results:
#     l = [names[int(c)] for c in r.boxes.cls]
#     if 'person' in l:
#         # ser.write()
#         print("MOUSE DETECTED!!")


def control_actuator(second: int):
    ser.write(second.to_bytes(2, byteorder='big'))  
    time.sleep(0.5)  

def read_sensor_data():
    time.sleep(0.01)  
    response = ser.readline().decode().strip()  
    humidity, temperature, moist_pct, light, status = response.split(',')  
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_sensor_data(conn, timestamp, float(temperature), float(moist_pct), float(humidity), float(light), status)
    return {
        'humidity': humidity,
        'temperature': temperature,
        'moist_pct': moist_pct,
        'light': light,
        'status': "ON" if status == "1" else "OFF"
    }

# def create_app():
#     app = Flask(__name__)

#     # Define YOLO thread
#     yolo_thread = Thread(target=image_detector)
#     yolo_thread.daemon = True  # Ensures the thread exits when the main thread does
#     yolo_thread.start()

#     return app

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/data')
def get_data():
    return jsonify(read_sensor_data())

@app.route('/control', methods=['POST'])
def control():
    if request.method == 'POST':
        second = request.form['second']
        control_actuator(int(second))
    return index()

@app.route('/mouse', methods=['GET', 'POST'])
def read_mouse_checker():
    if (request.method == 'POST'):
        a = 100
        ser.write(a.to_bytes(2, byteorder='big'))
    else:
        res = fetch_mouse_check_data(conn)
        return jsonify({'status':res})

if __name__ == '__main__':
    app.run(debug=True)
