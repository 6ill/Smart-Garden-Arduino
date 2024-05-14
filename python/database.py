import sqlite3

def connect_sensor_database():
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
        );
    '''
    c.execute(query)
    c.close()
    return conn

def connect_mouse_database():
    conn = sqlite3.connect('mouse_data.db', check_same_thread=False)
    c = conn.cursor()
    query_mouse = '''
        CREATE TABLE IF NOT EXISTS mouse_checker (
            mouse_exist CHAR(1)
        );
    '''
    c.execute(query_mouse)
    conn.commit()   
    c.close()
    return conn


def insert_sensor_data(conn, timestamp, temperature, moisture, humidity, light_intensity, status):
    c = conn.cursor()
    c.execute("INSERT INTO sensor_data (timestamp, temperature, moisture, humidity, light_intensity, status) VALUES (?, ?, ?, ?, ?,?)",
              (timestamp, temperature, moisture, humidity, light_intensity, status))
    conn.commit()
    c.close()


def fetch_all_sensor_data(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_data")
    return c.fetchall()

def insert_mouse_check_data(conn, num):
    c = conn.cursor()
    c.execute("INSERT INTO mouse_checker (mouse_exist) VALUES (?)", (num))
    conn.commit()
    c.close()

def fetch_mouse_check_data(conn):
    c = conn.cursor()
    c.execute("SELECT mouse_exist from mouse_checker")
    return c.fetchall()[-1][0]

if __name__ == "__main__":
    conn = connect_sensor_database()
    print(fetch_mouse_check_data(conn))
