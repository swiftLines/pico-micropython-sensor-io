import machine
import utime

# ***** Ultrasonic Sensor LED Threshold *****

# Setup pins
TRIG = machine.Pin(3, machine.Pin.OUT)  # TRIG output
ECHO = machine.Pin(2, machine.Pin.IN)   # ECHO input
led = machine.Pin("LED", machine.Pin.OUT)  # onboard LED

def distance_cm():
    # Send a 10 µs HIGH pulse to TRIG
    TRIG.value(0)
    utime.sleep_us(2)
    TRIG.value(1)
    utime.sleep_us(10)
    TRIG.value(0)

    # Measure the duration of HIGH pulse on ECHO
    t = machine.time_pulse_us(ECHO, 1, 30000)  # timeout 30ms (≈5 m)
    if t < 0:
        return None  # timeout / no object detected
    
    # Convert time of flight → distance
    return (t / 2) / 29.1  # speed of sound ≈ 343 m/s → 29.1 µs per cm

while True:
    d = distance_cm()
    if d is not None:
        led.value(d < 10)  # LED ON if object <10cm away
        print("Distance:", round(d, 1), "cm")
    else:
        print("Out of range")
    utime.sleep_ms(100)


# ***** ADC LED Brightness *****

# adc = machine.ADC(26)  # GP26 = ADC0
# pwm = machine.PWM(machine.Pin(25))
# pwm.freq(1000)

# while True:
#     raw = adc.read_u16()  # 0..65535
#     pwm.duty_u16(raw)  # brightness follow the potentiometer
#     utime.sleep_ms(20)