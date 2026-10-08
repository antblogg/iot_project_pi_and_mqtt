
import json
from pathlib import Path
from bridge.modes.MainMenu import MainMenu
from bridge.modes.MQTT import ModeMQTT
from bridge.modes.Database import ModeDatabase
from bridge.modes.ThingSpeak import ModeThingSpeak
from bridge.modes.Wifi import ModeWifi
from requests.structures import CaseInsensitiveDict
from multiprocessing import Queue
import sys


def main():

    sharedQueue = Queue(maxsize=10)

    database = ModeDatabase(sharedQueue)
    mqtt = ModeMQTT(sharedQueue)
    ts = ModeThingSpeak()

    mainMenu = MainMenu()
    while True:
        option = mainMenu.getUserInput()
        match option:
            case "D":
                database.enterMode()
            case "M":
                mqtt.enterMode()
            case "T":
                ts.enterMode()
            case "S":
                print("System summary:")
                for name, mode in zip(["Database", "MQTT        ","ThingSpeak"], [database,mqtt,ts]):
                    print(name +"\t:\t", "Connected" if mode.isConnected else "Disconnected")
            case "Q":
                return
            

if __name__ == "__main__":
    main()

# Parse arguments to optionally run in background


# load config
# button to load config - run the other script and rerun load config
# close button
# create labels for last N sensor values
# Create indicators green/red for connection status

# Connect to MQTT
# Connect to database
