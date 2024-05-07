from flask import Flask, render_template, request, jsonify
import serial
# import sqlite3
from database import connect_database, insert_sensor_data
import time
from datetime import datetime

app = Flask(__name__)
ser = serial.Serial('COM3', 9600)  
conn = connect_database()

def control_actuator(second: int):
    ser.write(second.to_bytes(2, byteorder='big'))  
    time.sleep(0.5)  

def read_sensor_data():
    time.sleep(1)  
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

if __name__ == '__main__':
    app.run(debug=True)
