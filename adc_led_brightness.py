import machine
import utime

adc = machine.ADC(26)  # GP26 = ADC0
pwm = machine.PWM(machine.Pin(25))
pwm.freq(1000)

while True:
    raw = adc.read_u16()  # 0..65535
    pwm.duty_u16(raw)  # brightness follow the potentiometer
    utime.sleep_ms(20)