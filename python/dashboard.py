import streamlit as st
from serial import Serial
from database import connect_database, insert_sensor_data
from datetime import datetime

@st.experimental_fragment(run_every=1)
def show_data():
    if 'conn' not  in st.session_state:
        return
    try:
        ser = Serial('COM3', 9600)
        data = ser.readline().decode().strip().split(',')  # Assuming data format: temp,moisture,light
        humidity, temperature, moist_pct, light, status = data
        status_str = "ON" if status == "1" else "OFF"
        st.write("Humidity: " +  humidity)
        st.write("Temperature: " +  temperature + " celsius")
        st.write("Moisture: " +  moist_pct + " %")
        st.write("Light: " +  light)
        st.write("Actuator Status: " +  status_str)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_sensor_data(st.session_state.conn, timestamp, float(temperature), float(moist_pct), float(humidity), float(light), 0)
    except:
        st.error("Error dalam membaca data")
        

if __name__ == "__main__":
    st.header("Smart Garden")
    if 'conn' not  in st.session_state:
        st.session_state['conn'] = connect_database()

    show_data()

    if st.button("Refresh"):
        st.rerun()