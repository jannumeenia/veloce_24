import PySimpleGUI as sg
import serial
import time
from PySimpleGUI.PySimpleGUI import ProgressBar


# Connect to Arduino Uno through serial communication
#arduino_port = '/dev/ttyUSB0'  # Change this to the port where your Arduino is connected on Windows
baud_rate = 115200


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
                                                                                                                    
     [sg.Text('', size=(1, 1), font=('Helvetica', 40), justification='left', key='top_left_blank', background_color='black', text_color='white'),
     ProgressBar(6500, orientation='h', size=(46, 70), key='rpm_bar', bar_color=('#6924ad', 'black')),
     sg.Text('', size=(1, 1), font=('Helvetica', 40), justification='right', key='lv_blank', background_color='black', text_color='white'),
     sg.Text('', size=(4, 1), font=('Helvetica', 40), justification='right', key='lv', background_color='black', text_color='white'),
     sg.Text('V', size=(1, 1), font=('Helvetica', 30), justification='right', key='lv_symbol', background_color='black', text_color='white') 
     ],

     [sg.Text('         0', size=(5,1) , font = ('Helvetica',12), justification ='left' , key  ='rpm_scale0', background_color = 'black', text_color = '#08ff08'),
      sg.Text('||||||||||||||', size=(6,1) , font = ('Helvetica',10), justification ='left' , key  ='rpm_scale1', background_color = 'black', text_color = '#08ff08'),
      sg.Text('1', size=(1,1) , font = ('Helvetica',12), justification ='left' , key  ='rpm_scale2', background_color = 'black', text_color = '#08ff08'),
      sg.Text('||||||||||||||', size=(6,1) , font = ('Helvetica',10), justification ='left' , key  ='rpm_scale3', background_color = 'black', text_color = '#08ff08'),
      sg.Text('2', size=(1,1) , font = ('Helvetica',12), justification ='left' , key  ='rpm_scale4', background_color = 'black', text_color = 'yellow'),
      sg.Text('||||||||||||||', size=(6,1) , font = ('Helvetica',10), justification ='left' , key  ='rpm_scale5', background_color = 'black', text_color = 'yellow'),
      sg.Text('3', size=(1,1) , font = ('Helvetica',12), justification ='left' , key  ='rpm_scale6', background_color = 'black', text_color = 'yellow'),
      sg.Text('||||||||||||||', size=(6,1) , font = ('Helvetica',10), justification ='left' , key  ='rpm_scale7', background_color = 'black', text_color = 'yellow'),
      sg.Text('4', size=(1,1) , font = ('Helvetica',12), justification ='left' , key  ='rpm_scale8', background_color = 'black', text_color = 'yellow'),
      sg.Text('||||||||||||||', size=(6,1) , font = ('Helvetica',10), justification ='left' , key  ='rpm_scale9', background_color = 'black', text_color = 'yellow'),
      sg.Text('5', size=(1,1) , font = ('Helvetica',12), justification ='left' , key  ='rpm_scale10', background_color = 'black', text_color = 'red'),
      sg.Text('||||||||||||||', size=(6,1) , font = ('Helvetica',10), justification ='left' , key  ='rpm_scale11', background_color = 'black', text_color = 'red'),
      sg.Text('6', size=(1,1) , font = ('Helvetica',12), justification ='left' , key  ='rpm_scale12', background_color = 'black', text_color = 'red'),
      sg.Text('|||||||||||', size=(5,1) , font = ('Helvetica',10), justification ='left' , key  ='rpm_scale13', background_color = 'black', text_color = 'red'),
      ],

     [sg.Text('', size=(20,1), font=('Helvetica', 42), justification='center', key='hv_blank', background_color='black', text_color='black'),
      sg.Text('', size=(3, 1), font=('Helvetica', 40), justification='center', key='hv', background_color='black', text_color='blue'),
      sg.Text('⚡', size=(1, 1), font=('Helvetica',25), justification='center', key='hv_bolt_symbol', background_color='black', text_color='blue')
      ],

    [sg.Text('', size=(5, 1), font=('Helvetica', 20), justification='center', key='wheel_speed_blank', background_color='black', text_color='black'),
     sg.Text('', size=(2, 1), font=('Helvetica', 120), justification='center', key='wheel_speed', background_color='black', text_color='red'),
     sg.Text('kmph', size=(4, 1), font=('Helvetica',25), justification='center', key='wheel_speed_kmph', background_color='black', text_color= 'red'),
     sg.Text('|', size=(1, 1), font=('Helvetica', 130), justification='center', key='wheel_speed_rpm_divider', background_color='black', text_color='#6924ad'),
     sg.Text('', size=(4, 1), font=('Helvetica', 50), justification='center', key='motor_rpm', background_color='black', text_color='#6924ad'),
     ],
     
     [sg.Text('', size=(1, 1), font=('Helvetica', 25), justification='center', key='-DUMMY4-', background_color='black', text_color='black'),
     ],
    
    [sg.Text('', size=(4, 1), font=('Helvetica', 45), justification='left', key='hvbattery_temperature', background_color='black', text_color='white'),
     #sg.Text('🔋', size=(1, 1), font=('Helvetica', 45), justification='left', key='hvbattery_temperature_emoji', background_color='black', text_color='white'),
     sg.Text('℃', size=(2, 1), font=('Helvetica', 30), justification='left', key='hvbattery_temperature_celcious', background_color='black', text_color='white'),
     sg.Text('', size=(10, 1), font=('Helvetica', 40), justification='center', key='bottom_blank', background_color='black', text_color='black'),
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
            window['rpm_bar'].update(int(motor_rpm))
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

