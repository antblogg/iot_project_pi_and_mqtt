
import smbus

class I2C:

    filterConstant = 0.9 # (0.0, 1.0]

    I2CChannel = 1
    I2CAdress = 0x48 # Todo find address
    """
    TCA0 = 0x48
    TCA1 = 0x49
    ...
    TCA7 = 0x4F
    """
    I2CReadRegister = 0x00 

    def __init__(self):
        self.bus = smbus.SMBus(self.I2CChannel)
        self.signal = self._scaleSignal(self._getRawSensorValue()) # initalize to raw value

    def __del__(self):
        self.close()

    def close(self):
        self.bus.close()

    @staticmethod
    def _scaleSignal(signal):
        if signal > 127: signal-=256
        return signal

    def _getRawSensorValue(self):
        raw = self.bus.read_byte_data(self.I2CAdress,self.I2CReadRegister) 
        return raw

    def filterSignal(self, signal):
        a = self.filterConstant
        return a*signal + (1-a)*self.signal

    def getReading(self):
        signal = self._getRawSensorValue()
        signal = self._scaleSignal(signal)
        self.signal = self.filterSignal(signal)
        return self.signal


