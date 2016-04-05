import smbus
import math

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
axis2addr = {
    'x': 0x3b,
    'y': 0x3d,
    'z': 0x3f
}


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)


def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


class Accelerometer(object):
    def __init__(self):
        self.bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        self.address = 0x68       # This is the address value read via the i2cdetect command
        
    def initialize():
        self.bus.write_byte_data(self.address, power_mgmt_1, 0)

    def read_accel(self, axis):
        return read_word_2c(axis2addr[axis]) / 16384.0
