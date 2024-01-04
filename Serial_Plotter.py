import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from fractions import Fraction
# Define the serial port settings
serial_port = 'COM5'  # Change this to your serial port
baud_rate = 115200
data_size = 2
packets_per_update = 1024
byte_order='big'




# Initialize serial port
ser = serial.Serial(serial_port, baud_rate)

# Create a figure and axis for plotting
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(-100, 100)  # Assuming the data range is between 0 and 255
ax.set_xlim(0, packets_per_update-1)  # Assuming the data range is between 0 and 255
# Initialize data buffer
data_buffer = []

# Function to initialize the plot
def init():
    line.set_data([], [])
    return line,

# Function to update the plot in real-time
def update(frame):
    global data_buffer

    # Read data from the serial port
    new_data = ser.read(packets_per_update * data_size)
    byte_data=new_data[0]
    print(new_data[0])
    byte_data=new_data[1]
    print(new_data[1])
    # Convert the binary data to a list of integers
    data_values = [int.from_bytes(new_data[i:i+data_size], byteorder=byte_order,signed=False) for i in range(0, len(new_data), data_size)]
    # Initialize an empty list to store the converted decimal values
    decimal_values = []
    for value in data_values:
        integer_part = value >> 15
        fractional_part = Fraction(value & 0x7FFF, 2**15)
        # Convert to decimal with fraction and append to the new list
        decimal_value = integer_part + fractional_part
        decimal_values.append(decimal_value)
    # Apply 10 * log10(data) transformation
    transformed_data = [10 * np.log10(float(data+0.00000000001))  for data in decimal_values]

    # Update the data buffer
    data_buffer = transformed_data
    print(data_buffer[0])
    # Plot the transformed data
    x_data = range(len(data_buffer))
    print(x_data[0],x_data[1023])
    print(len(data_buffer))
    line.set_data(x_data, data_buffer)

    return line,

# Set up the animation
ani = FuncAnimation(fig, update, frames=None, init_func=init, blit=True)

# Show the plot
plt.show()

# Close the serial port when the plot is closed
ser.close()
