import RPi.GPIO as GPIO
import smbus
import time


FRONT_SLAVE = 0x04


led_pin = 26
bus = smbus.SMBus(1)


def send_data_to_slave(data: str, address):
    ascii_values = [ord(char) for char in data]
    
    for value in ascii_values:
        bus.write_byte(address, value)
        time.sleep(0.1)


def setup():
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(led_pin, GPIO.OUT)
    pass


def loop():
    # send_data_to_slave("Je moeder", 0x04)
    # time.sleep(1)
    
    try:
        bus.write_byte(FRONT_SLAVE, 0x01)    
        length = bus.read_byte(FRONT_SLAVE)
        print(f"Received string length: {length}")
    
        received_data = bus.read_i2c_block_data(FRONT_SLAVE, 0, 31)
        received_string = ''.join(chr(value) for value in received_data)

        print(f"Received string: {received_string}")
    except Exception as e:
        print(f"Error: {e}")


    time.sleep(1)


if "__main__" == __name__:
    setup()

    try:
        while True:
            loop()

    except KeyboardInterrupt:
        GPIO.cleanup()
        bus.close()
