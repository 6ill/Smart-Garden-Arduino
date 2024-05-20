from flask import Flask, request, jsonify, redirect
import serial

# import sqlite3
from database import connect_sensor_database, insert_sensor_data, fetch_mouse_check_data, connect_mouse_database
import time
from datetime import datetime

app = Flask(__name__)
ser = serial.Serial("COM3", 9600)
conn_sensor = connect_sensor_database()
conn_mouse = connect_mouse_database()


def control_actuator(second: int):
    ser.write(second.to_bytes(2, byteorder="big"))
    time.sleep(1)   


def read_sensor_data():
    response = ser.readline().decode().strip()
    humidity, temperature, moist_pct, light, status = response.split(",")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if datetime.now().second == 59:
        insert_sensor_data(
            conn_sensor,
            timestamp,
            float(temperature),
            float(moist_pct),
            float(humidity),
            float(light),
            status,
        )
    return {
        "humidity": humidity,
        "temperature": temperature,
        "moist_pct": moist_pct,
        "light": light,
        "status": "ON" if status == "1" else "OFF",
    }


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/data")
def get_data():
    try:
        return jsonify(read_sensor_data())
    except:
        data = {
        "humidity":"_",
        "temperature":"_",
        "moist_pct":"_",
        "light":"_",
        "status":"_",
        }           
        return jsonify(data)


@app.route("/control", methods=["POST"])
def control():
    if request.method == "POST":
        if 'second' not in request.form:
            return redirect("/")
        second = request.form["second"]
        control_actuator(int(second))
    return redirect("/")


@app.route("/mouse", methods=["GET"])
def read_mouse_checker():
    res = fetch_mouse_check_data(conn_mouse)
    if res == '1':
        a = 1
        ser.write(a.to_bytes(1,  byteorder='big'))
    else:
        a = 0
        ser.write(a.to_bytes(1, byteorder='big'))

    return jsonify({"status": res})


if __name__ == "__main__":
    app.run(debug=True)
