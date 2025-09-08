import machine
import utime

# --- Ultrasonic (HC-SR04): TRIG=GP3, ECHO=GP2 ---
TRIG = machine.Pin(3, machine.Pin.OUT)
ECHO = machine.Pin(2, machine.Pin.IN)

# --- Servo on GP15 (external 5V power, GNDs tied together) ---
servo = machine.PWM(machine.Pin(15))
servo.freq(50)  # 50 Hz (~20 ms period)

# Servo helper: write angle in degrees (0..180)
def write_deg(deg: float) -> None:
    deg = max(0, min(180, deg))
    us = 500 + (deg * 2000) / 180.0  # 0°≈500us, 180°≈2500us
    duty = int(us / 20000.0 * 65535.0)  # 20ms period -> duty_u16
    servo.duty_u16(duty)

# Ultrasonic distance in cm; None on timeout
def distance_cm(timeout_us=30000):
    TRIG.value(0); utime.sleep_us(2)
    TRIG.value(1); utime.sleep_us(10)
    TRIG.value(0)
    t = machine.time_pulse_us(ECHO, 1, timeout_us)
    if t < 0:
        return None
    return (t / 2.0) / 29.1

# Map distance range -> angle range
def map_distance_to_angle(d_cm, near=8, far=50, min_deg=0, max_deg=180):
    if d_cm is None:
        return None
    # Clamp to [near, far]
    d = max(near, min(far, d_cm))
    # Closer -> higher angle (invert mapping)
    span = float(far - near)
    pct = (far - d) / span
    return min_deg + pct * (max_deg - min_deg)

while True:
    d = distance_cm()
    if d is not None:
        angle = map_distance_to_angle(d)
        write_deg(angle)
        print("d = {:.1f} cm -> {:.0f}°".format(d, angle))
    else:
        print("out of range")
    utime.sleep_ms(80)
