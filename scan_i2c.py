import machine
import utime

# I2C0 on Pico: SDA=GP16, SCL=GP17
i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16), freq=400_000)

utime.sleep_ms(100)
addrs = i2c.scan()

if not addrs:
    print("No I2C devices found.")
else:
    print("I2C device addresses:")
    for a in addrs:
        print(" - 0x{:02X}".format(a))
