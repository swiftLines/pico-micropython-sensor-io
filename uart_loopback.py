import machine
import utime

# Configure UART0 with TX=GP0, RX=GP1
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

# Send message
uart.write(b"hello\r\n")

# Give receiver a moment
utime.sleep_ms(10)

# Read back if available
if uart.any():
    print("uart:", uart.read())
    