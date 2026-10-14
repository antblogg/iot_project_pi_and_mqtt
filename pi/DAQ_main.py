from modes.MQTT import ModeMQTT
from modes.ThingSpeak import ModeThingSpeak
from multiprocessing import Queue
import signal
import random
import time

HARDWARE_CONNECTED = True

class dummySensor:
    def getReading(self, *args, **kwargs): return 23.67 + random.gauss(0,4)
    def close(self, *args, **kwargs): return

class dummyPwm:
    def start(self, *args, **kwargs): return
    def stop(self, *args, **kwargs): return
    def ChangeDutyCycle(self, *args, **kwargs): return

class dummyGPIO:
    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    BCM = 2
    PUD_UP = 3

    def setmode(self, *args, **kwargs): return
    def setup(self, *args, **kwargs): return
    def PWM(self, *args,**kwargs): return dummyPwm()
    def input(self,*args,**kwargs): return self.HIGH
    def cleanup(self, *args, **kwargs): return


if HARDWARE_CONNECTED:
    import RPi.GPIO as GPIO
    from sensorCommunication.I2C import I2C
    from sensorCommunication.spi import SpiInterface
else:
    GPIO = dummyGPIO()



# Alarm limits
HIGH_TEMP_LIMIT = 28.0
LOW_TEMP_LIMIT = 18.0

# GPIO 
LED_PIN = 18      
BUTTON_PIN = 17   


def getAlarmBrightness(temp):

    if temp > HIGH_TEMP_LIMIT:
        deviation = temp - HIGH_TEMP_LIMIT
    elif temp < LOW_TEMP_LIMIT:
        deviation = LOW_TEMP_LIMIT - temp
    else:
        return 0

    duty = deviation * 10.0

    # Clamp to valid PWM range
    duty = max(5.0, duty)   # ensure alarm is visible
    duty = min(100.0, duty)

    return duty


def main():
    # no database - queue not needed, passing a dummy object
    dummyQueue = Queue(maxsize=1)
    mqtt = ModeMQTT(dummyQueue)
    ts = ModeThingSpeak()

    # Choose either I2C or SPI sensor. using I2C here.

    if HARDWARE_CONNECTED:
        sensor = I2C()
        #sensor = SpiInterface()
    else:
        sensor = dummySensor()

    if HARDWARE_CONNECTED:
        sensorname = "I2C temperature sensor"
    else:
        sensorname = "Dummy temperature sensor"

    # Raspberry Pi GPIO initialization
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    pwm = GPIO.PWM(LED_PIN, 1000)
    pwm.start(0)

    alarmActive = False
    alarmAcknowledged = False

    try:
        while True:
            val = sensor.getReading()

            ts.writeValue(val)

            mqtt.publishMessage({
                "Temperature": str(val),
                "Sensor": sensorname,
                "timestamp": time.ctime()
            })

            # Alarm logic
            alarmTriggered = ((val > HIGH_TEMP_LIMIT) or (val < LOW_TEMP_LIMIT))

            if alarmTriggered:
                if not alarmActive:
                    alarmActive = True
                    alarmAcknowledged = False
            else:
                alarmActive = False
                alarmAcknowledged = False
                
                pwm.ChangeDutyCycle(0)

            # Alarm acknowledgment
            if alarmActive and GPIO.input(BUTTON_PIN) == GPIO.LOW:
                alarmAcknowledged = True
                pwm.ChangeDutyCycle(0)
                # debounce
                time.sleep(0.2)

            # set LED brightness
            if alarmActive and not alarmAcknowledged:
                brightness = getAlarmBrightness(val)
                pwm.ChangeDutyCycle(brightness)

            time.sleep(0.5)

    except KeyboardInterrupt:
        pass

    finally:
        sensor.close()
        pwm.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()