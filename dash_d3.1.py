import PySimpleGUI as sg
import serial
import time
from PySimpleGUI.PySimpleGUI import ProgressBar
import math
import random


# Connect to Arduino Uno through serial communication
#arduino_port = '/dev/ttyUSB0'  # Change this to the port where your Arduino is connected on Windows
baud_rate = 115200

# Constants
WHEEL_DIAMETER = 0.4046  # meters
CIRCUMFERENCE = math.pi * WHEEL_DIAMETER  # meter


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
                                                                                                                    
     [sg.Text('', size=(1, 1), font=('Helvetica', 20), justification='left', key='top_left_blank', background_color='black', text_color='white'),
     ProgressBar(6500, orientation='v', size=(25, 50), key='rpm_bar', bar_color=('#6924ad', 'black')),
     sg.Text('', size=(4, 1), font=('Helvetica', 10), justification='right', key='lv_blank', background_color='black', text_color='white'),
     sg.Text('', size=(4, 1), font=('Helvetica', 120), justification='center', key='motor_rpm', background_color='black', text_color='red'),
     sg.Text('|', size=(1, 1), font=('Helvetica', 110), justification='center', key='wheel_speed_rpm_divider', background_color='black', text_color='#6924ad'),
     sg.Text('',pad = ((0,0),(20,0)), size=(2, 1), font=('Helvetica', 50), justification='center', key='wheel_speed', background_color='black', text_color='#cc2f4c'),
     sg.Text('kmph', size=(4, 1), font=('Helvetica',10), justification='center', key='wheel_speed_kmph', background_color='black', text_color= '#874a6f'),

     sg.Text('', size=(5, 1), font=('Helvetica', 40), justification='center', key='hv', background_color='black', text_color='blue'),
     sg.Text('⚡', size=(1, 1), font=('Helvetica',15), justification='center', key='hv_bolt_symbol', background_color='black', text_color='blue'),


     ],
     
    [sg.Text('', size=(1, 60), font=('Helvetica', 10), justification='center', key='-DUMMY4-', background_color='black', text_color='black'),

     sg.Text('', size=(4, 1), font=('Helvetica', 25), justification='center', key='odo', background_color='black', text_color='white')
     sg.Text('km', size=(4, 1), font=('Helvetica', 25), justification='center', key='odo_km_text', background_color='black', text_color='white')


     ],

     [
     #sg.Text('', size=(8, 1), font=('Helvetica', 45), justification='center', key='bottom_blank', background_color='black', text_color='black'),
      sg.Text('', size=(5, 1), font=('Helvetica', 55), justification='center', key='hv', background_color='black', text_color='blue'),
      sg.Text('⚡', size=(1, 1), font=('Helvetica',25), justification='center', key='hv_bolt_symbol', background_color='black', text_color='blue'),
      sg.Text('',pad = ((0,0),(0,0)), size=(16, 1), font=('Helvetica', 25), justification='center', key='bottom_blank', background_color='black', text_color='white'),
      sg.Text('', size=(16, 1), font=('Helvetica', 25), justification='center', key='odo', background_color='black', text_color='white'),
      sg.Text('', size=(4, 1), font=('Helvetica', 45), justification='left', key='hvbattery_temperature', background_color='black', text_color='white'),
      #sg.Text('🔋', size=(1, 1), font=('Helvetica', 45), justification='left', key='hvbattery_temperature_emoji', background_color='black', text_color='white'),
      sg.Text('℃', size=(2, 1), font=('Helvetica', 30), justification='left', key='hvbattery_temperature_celcious', background_color='black', text_color='white'),
      ],
    
    [ 
     #sg.Text('', size=(1, 1), font=('Helvetica', 40), justification='right', key='lv_blank', background_color='black', text_color='white'),
     sg.Text('', size=(4, 1), font=('Helvetica', 40), justification='right', key='lv', background_color='black', text_color='white'),
     sg.Text('V', size=(1, 1), font=('Helvetica', 30), justification='right', key='lv_symbol', background_color='black', text_color='white'),
     sg.Text('#NEVER GIVE UP',pad = ((0,0),(0,0)), size=(26, 1), font=('Helvetica', 18), justification='center', key='bottom_blank', background_color='black', text_color='grey'),
     sg.Text('⚙️', size=(2, 1), font=('Helvetica', 20), justification='left', key='motor_temperature_emoji', background_color='black', text_color='white'),
     sg.Text('', size=(4, 1), font=('Helvetica', 45), justification='right', key='motor_temperature', background_color='black', text_color='white'),
     sg.Text('℃', size=(2, 1), font=('Helvetica', 30), justification='left', key='motor_temperature_celcious', background_color='black', text_color='white')
     ],
    
    ]

# Create the window with specified size and background color
window = sg.Window('Car Dashboard Panel', layout,no_titlebar=True, finalize=True, size=(800, 480), background_color='black')

while True:
    # event, values = window.read(timeout=10)  # Set a timeout for the event loop (milliseconds)

    # if event in (sg.WINDOW_CLOSED,):
    #     break

    # Read data from Arduino
    try:
        arduino_data = ser.readline().decode().strip().split(',')
        if len(arduino_data) == 5:
            motor_rpm, hv, hvbattery_temperature, motor_temperature, lv = arduino_data
            wheel_speed = int((int(motor_rpm)*1.436*60)/(1000*4.57))
            # Update the displayed values
            # wheel_speed =  int(wheel_speed - (wheel_speed*(15/100)))


            # Function to simulate getting the current RPM
            total_distance = 0  # in meters
            previous_time = time.time()   # convert to milliseconds
            print(time.time())

            # Main loop
            while True:
                current_rpm = motor_rpm  # get the current RPM
                current_time = time.time()   # current time in milliseconds
                
                # Calculate time difference in seconds
                time_diff_s = current_time - previous_time
                previous_time = current_time
                
                # Convert RPM to RPS (revolutions per second)
                rps = current_rpm / 60.0
                
                # Calculate distance traveled in this time interval
                distance = rps * 1.436 * time_diff_s
                
                # Update total distance
                total_distance += distance
                
                # Sleep for a short interval before the next reading (sampling every millisecond)
                time.sleep(0.001)  # sleep for 1 millisecond

            window['rpm_bar'].update(int(motor_rpm))
            window['odo'].update(int(total_distance))  
            window['lv'].update(lv)  
            window['hv'].update(hv)
            window['wheel_speed'].update(wheel_speed)
            window['motor_rpm'].update(motor_rpm)
            window['hvbattery_temperature'].update(hvbattery_temperature)
            window['motor_temperature'].update(motor_temperature)
            
            if float(lv) < 12.20:
                window['lv'].update(text_color = 'red')
                window['lv_symbol'].update(text_color = 'red')
            elif float(lv) > 12.20 and float(lv) <13.00 :
                window['lv'].update(text_color = '#268045')
                window['lv_symbol'].update(text_color = '#268045')
            elif float(lv) >= 13.00 :
                window['lv'].update(text_color = '#22738a')
                window['lv_symbol'].update(text_color = '#22738a') 

            if float(hv) <= 320.00 :
                 window['hv'].update(text_color = 'red')
                 window['hv_bolt_symbol'].update(text_color = 'red')
            elif float(hv) > 320.00 and float(hv) < 340.00 :
                window['hv'].update(text_color = '#268045')
                window['hv_bolt_symbol'].update(text_color = '#268045')
            elif float(hv) >= 340.00 :
                window['hv'].update(text_color = '#22738a')
                window['hv_bolt_symbol'].update(text_color = '#22738a')
            
            if float(motor_temperature) >= 65.00 :
                 window['motor_temperature'].update(text_color = 'red')
                 window['motor_temperature_celcious'].update(text_color = 'red')
                 window['motor_temperature_emoji'].update(text_color = 'red')
            elif float(motor_temperature) < 65.00 and float(motor_temperature) > 42.00 :
                window['motor_temperature'].update(text_color = '#c2bd3a')
                window['motor_temperature_celcious'].update(text_color = '#c2bd3a')
                window['motor_temperature_emoji'].update(text_color = '#c2bd3a')
            elif float(motor_temperature) <= 42.00 :
                window['motor_temperature'].update(text_color = '#3974d4')
                window['motor_temperature_celcious'].update(text_color = '#3974d4')
                window['motor_temperature_emoji'].update(text_color = '#3974d4')

            
            
            if float(hvbattery_temperature) >= 60.00 :
                 window['hvbattery_temperature'].update(text_color = 'red')
                 window['hvbattery_temperature_celcious'].update(text_color = 'red')
                 #window['hvbattery_temperature_celcious'].update(text_color = 'red')
            elif float(hvbattery_temperature) < 60.00 and float(motor_temperature) > 42.00 :
                window['hvbattery_temperature'].update(text_color = '#c2bd3a')
                window['hvbattery_temperature_celcious'].update(text_color = '#c2bd3a')
                #window['hvbattery_temperature_emoji'].update(text_color = '#c2bd3a')
            elif float(hvbattery_temperature) <= 42.00 :
                window['hvbattery_temperature'].update(text_color = '#3974d4')
                window['hvbattery_temperature_celcious'].update(text_color = '#3974d4')
                #window['hvbattery_temperature_emoji'].update(text_color = '#3974d4')
                
    except (serial.SerialException, KeyboardInterrupt) as e:
        print(f" Exception: {e}")
        ser.close()
        window.close()


