import PySimpleGUI as sg
import serial
import time

# Connect to Arduino Uno through serial communication
#arduino_port = '/dev/ttyUSB0'  # Change this to the port where your Arduino is connected on Windows
baud_rate = 9600

try:
    ser = serial.Serial('/dev/ttyUSB0', baud_rate, timeout=1)
except serial.SerialException as e:
    print(f"Serial Exception: {e}")
    ser = serial.Serial('/dev/ttyUSB1', baud_rate, timeout=1)
time.sleep(3)
ser.reset_input_buffer()
print("Serial Connection Ok")

# Define the layout of the window
layout = [

     [sg.Text('', size=(3, 1), font=('Helvetica', 50), justification='left', key='-TOP_LEFT-', background_color='black', text_color='white'),
           sg.Text('', size=(14, 1), font=('Helvetica', 50), justification='center', key='-DUMMY1-', background_color='black', text_color='black'),

     sg.Text('', size=(3, 1), font=('Helvetica', 50), justification='right', key='-TOP_RIGHT-', background_color='black', text_color='white')],

     [sg.Text('', size=(1,1), font=('Helvetica', 50), justification='center', key='-DUMMY2-', background_color='black', text_color='black')],


    [sg.Text('', size=(4, 1), font=('Helvetica', 50), justification='center', key='-DUMMY3-', background_color='black', text_color='black'),
     sg.Text('', size=(3, 1), font=('Helvetica', 120), justification='center', key='-CENTER_LEFT-', background_color='black', text_color='red'),
     sg.Text('', size=(1, 1), font=('Helvetica', 20), justification='center', key='-DUMMY4-', background_color='black', text_color='black'),
     sg.Text('', size=(3, 1), font=('Helvetica', 80), justification='center', key='-CENTER_RIGHT-', background_color='black', text_color='blue')],
    
    [sg.Text('', size=(1, 1), font=('Helvetica', 45), justification='center', key='-DUMMY5-', background_color='black', text_color='black')],


    [sg.Text('', size=(3, 1), font=('Helvetica', 50), justification='left', key='-BOTTOM_LEFT-', background_color='black', text_color='white'),
     sg.Text('', size=(14, 1), font=('Helvetica', 50), justification='center', key='-DUMMY6-', background_color='black', text_color='black'),
     sg.Text('', size=(3, 1), font=('Helvetica', 50), justification='right', key='-BOTTOM_RIGHT-', background_color='black', text_color='white')],
    
e
]

# Create the window with specified size and background color
window = sg.Window('Car Dashboard Panel', layout,no_titlebar=True, finalize=True, size=(800, 480), background_color='black')

while True:
    event, values = window.read(timeout=100)  # Set a timeout for the event loop (milliseconds)

    if event in (sg.WINDOW_CLOSED,):
        break

    # Read data from Arduino
    try:
        arduino_data = ser.readline().decode().strip().split(',')
        if len(arduino_data) == 6:
            center_top_value, center_bottom_value, bottom_left_value, bottom_right_value, top_left_value, top_right_value = arduino_data

            # Update the displayed values
            window['-CENTER_LEFT-'].update(center_top_value)
            window['-CENTER_RIGHT-'].update(center_bottom_value)
            window['-BOTTOM_LEFT-'].update(bottom_left_value)
            window['-BOTTOM_RIGHT-'].update(bottom_right_value)
            window['-TOP_LEFT-'].update(top_left_value)
            window['-TOP_RIGHT-'].update(top_right_value)
    except (serial.SerialException, KeyboardInterrupt) as e:
        print(f" Exception: {e}")
        ser.close()
        window.close()