# HC-SR04 Ultrasonic Distance (MicroPython)
# - Robust: timeouts prevent freezing
# - Beginner friendly: clear steps + readable math

from machine import Pin
import time

# --- Wiring (Pico example) ---
TRIG = Pin(19, Pin.OUT)   # Pico GPIO19 -> HC-SR04 TRIG
ECHO = Pin(18, Pin.IN)    # Pico GPIO18 <- HC-SR04 ECHO 

# --- Constants ---
TRIG_PULSE_US = 10

# HC-SR04 typical max range is ~400 cm
# Round-trip time for 400 cm is about 23,000 us (23 ms), so choose a little bigger:
TIMEOUT_US = 30_000

# Speed of sound at room temp ≈ 343 m/s
# Convert to cm/us: 343 m/s = 34300 cm/s = 0.0343 cm/us
SPEED_CM_PER_US = 0.0343


def send_trigger_pulse():
    """Send the 10 us trigger pulse to start a measurement."""
    TRIG.value(0)
    time.sleep_us(2)               # short settle
    TRIG.value(1)
    time.sleep_us(TRIG_PULSE_US)   # >= 10 us
    TRIG.value(0)


def measure_echo_pulse_us(timeout_us=TIMEOUT_US):
    """
    Measure how long ECHO stays HIGH (in microseconds).
    Returns:
        pulse_us (int) if successful
        None if timeout (no echo / out of range / wiring issue)
    """
    # 1) Wait for ECHO to go HIGH (start of pulse)
    start_wait = time.ticks_us()
    while ECHO.value() == 0:
        if time.ticks_diff(time.ticks_us(), start_wait) > timeout_us:
            return None

    pulse_start = time.ticks_us()

    # 2) Wait for ECHO to go LOW (end of pulse)
    while ECHO.value() == 1:
        if time.ticks_diff(time.ticks_us(), pulse_start) > timeout_us:
            return None

    pulse_end = time.ticks_us()

    # pulse width = round-trip travel time
    return time.ticks_diff(pulse_end, pulse_start)


def distance_cm():
    """
    Trigger the sensor and return distance in cm.
    Returns:
        distance (float) or None if out of range/timeout.
    """
    send_trigger_pulse()

    echo_us = measure_echo_pulse_us()
    if echo_us is None:
        return None

    # Distance = (speed * time) / 2
    # time is round-trip, so divide by 2 to get one-way distance
    d_cm = (echo_us * SPEED_CM_PER_US) / 2
    return d_cm


# --- Main loop ---
time.sleep(2)  # optional: let sensor settle on power-up

while True:
    d = distance_cm()

    if d is None:
        print("Out of range / no echo")
    else:
        print("Distance: {:.1f} cm".format(d))

    time.sleep_ms(500)