import machine


class accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.iic.stop()

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = (self.bytes_toint(raw_ints[0], raw_ints[1]))/16384
        vals["AcY"] = (self.bytes_toint(raw_ints[2], raw_ints[3]))/16384
        vals["AcZ"] = (self.bytes_toint(raw_ints[4], raw_ints[5]))/16384-1
        vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            print(self.get_values())
            sleep(0.05)
            
    def calibrate(self, num_samples=1000):
        from time import sleep
        sum_values = {"AcX": 0, "AcY": 0, "AcZ": 0, "Tmp": 0, "GyX": 0, "GyY": 0, "GyZ": 0}
        
        for _ in range(num_samples):
            raw_values = self.get_raw_values()
            
            sum_values["AcX"] += self.bytes_toint(raw_values[0], raw_values[1]) / 16384
            sum_values["AcY"] += self.bytes_toint(raw_values[2], raw_values[3]) / 16384
            sum_values["AcZ"] += self.bytes_toint(raw_values[4], raw_values[5]) / 16384 - 1
            sum_values["Tmp"] += self.bytes_toint(raw_values[6], raw_values[7]) / 340.00 + 36.53
            sum_values["GyX"] += self.bytes_toint(raw_values[8], raw_values[9])
            sum_values["GyY"] += self.bytes_toint(raw_values[10], raw_values[11])
            sum_values["GyZ"] += self.bytes_toint(raw_values[12], raw_values[13])
            sleep(0.001) #wait for next sample

        calibration_values = {key: value / num_samples for key, value in sum_values.items()}
        return calibration_values
        