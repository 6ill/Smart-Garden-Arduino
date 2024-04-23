from serial import Serial
from database import connect_database, insert_sensor_data
from datetime import datetime
ser = Serial('COM3', 9600)
conn = connect_database()


while True:
    data = ser.readline().decode().strip().split(',')  # Assuming data format: temp,moisture,light
    print(data)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_sensor_data(conn, timestamp, float(data[0]), float(data[1]), float(data[2]), float(data[3]), int(data[4]))