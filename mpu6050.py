from machine import I2C, Pin
import time

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')

    def get_values(self):
        raw_data = self.i2c.readfrom_mem(self.addr, 0x3B, 14)
        return {
            'AcX': self.bytes_to_int(raw_data[0:2]),
            'AcY': self.bytes_to_int(raw_data[2:4]),
            'AcZ': self.bytes_to_int(raw_data[4:6]),
        }

    def bytes_to_int(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def bytes_to_int(self, data):
        val = data[0] << 8 | data[1]
        if val & 0x8000:
            return val - 0x10000
        return val
