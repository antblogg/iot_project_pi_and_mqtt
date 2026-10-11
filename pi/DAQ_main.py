

from modes.MQTT import ModeMQTT
from modes.ThingSpeak import ModeThingSpeak
from multiprocessing import Queue
import signal
import time

"""
from sensorCommunication.I2C import I2C
from sensorCommunication.spi import SpiInterface
"""

class dummySensor():
    def getReading(self): return 23.67
    def close(self): return


def main():
    # no database - queue not needed, passing a dummy object
    dummyQueue = Queue(maxsize=1)
    mqtt = ModeMQTT(dummyQueue)
    ts = ModeThingSpeak()
    # Choose either I2C or SPI sensor. using I2C here.
    #sensor = I2C()
    #sensor = SpiInterface()
    sensor = dummySensor()
    
    
    sensorname = "Dummy temperature sensor"

    try:
        while True:
            val = sensor.getReading()
            ts.writeValue(val)
            mqtt.publishMessage({
                "Temperature": str(val),
                "Sensor": sensorname,
                "timestamp": time.ctime()
            })
            time.sleep(5)
    except KeyboardInterrupt:
        sensor.close()

if __name__ == "__main__":
    main()