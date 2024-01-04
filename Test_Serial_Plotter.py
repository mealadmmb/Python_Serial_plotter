import serial
import time
import random

# Define the serial port settings
serial_port = 'COM4'  # Change this to your serial port
baud_rate = 115200

# Initialize serial port
ser = serial.Serial(serial_port, baud_rate)

# Function to send dummy data packets
def send_dummy_data():
    while True:
        # Generate 1024 random 2-byte values (simulating a packet of data)
        dummy_data = [random.randint(0, 255) for _ in range(1024*2)]

        # Convert the values to bytes and send through the serial port
        ser.write(bytearray(dummy_data))
        
        # Pause for a short time (simulating data transmission rate)
        time.sleep(1)

# Uncomment the line below to start sending dummy data
send_dummy_data()
