from machine import Pin, time_pulse_us
import time

# set up pins for the ultrasonic sensor
TRIG = Pin(19, Pin.OUT)   # trigger pin sends pulse to sensor
ECHO = Pin(18, Pin.IN)    # echo pin receives return signal

# onboard LED on Pico W
led = Pin("LED", Pin.OUT)

while True:

    # send a short trigger pulse to start measurement
    TRIG.value(0)
    time.sleep_us(2)
    TRIG.value(1)
    time.sleep_us(10)
    TRIG.value(0)

    # measure how long the echo pin stays HIGH
    duration = time_pulse_us(ECHO, 1, 30000)

    # if a valid echo was received
    if duration > 0:

        # convert time to distance in centimeters
        distance = (duration * 0.0343) / 2

        # print distance to terminal
        print("Distance:", distance)

        # turn LED on if object is closer than 10 cm
        if distance < 10:
            led.value(1)
        else:
            led.value(0)

    else:
        # print message if no echo detected
        print("No echo")

    # short delay before next measurement
    time.sleep(0.3)