import sqlite3

def connect_database():
    conn = sqlite3.connect('sensor_data.db', check_same_thread=False)
    c = conn.cursor()
    query = '''
        CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        temperature REAL,
        moisture REAL,
        humidity REAL,
        light_intensity REAL,
        status CHAR(1)
        )
    '''
    c.execute(query)
    conn.commit()
    return conn

def insert_sensor_data(conn, timestamp, temperature, moisture, humidity, light_intensity, status):
    c = conn.cursor()
    c.execute("INSERT INTO sensor_data (timestamp, temperature, moisture, humidity, light_intensity, status) VALUES (?, ?, ?, ?, ?,?)",
              (timestamp, temperature, moisture, humidity, light_intensity, status))
    conn.commit()

def fetch_all_sensor_data(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_data")
    return c.fetchall()


if __name__ == "__main__":
    conn = connect_database()
    print(fetch_all_sensor_data(conn)[-10:])
