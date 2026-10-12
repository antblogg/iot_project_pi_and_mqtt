from modes.MQTT import ModeMQTT
from modes.ThingSpeak import ModeThingSpeak
from multiprocessing import Queue
import signal
import time


import RPi.GPIO as GPIO
from sensorCommunication.I2C import I2C
from sensorCommunication.spi import SpiInterface

class dummySensor():
    def getReading(self): return 23.67
    def close(self): return


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
    #sensor = I2C()
    #sensor = SpiInterface()
    sensor = dummySensor()

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

            time.sleep(5)

    except KeyboardInterrupt:
        pass

    finally:
        sensor.close()
        pwm.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()