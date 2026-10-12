
import json
from pathlib import Path
from bridge.modes.MainMenu import MainMenu
from bridge.modes.MQTT import ModeMQTT
from bridge.modes.Database import ModeDatabase
from bridge.modes.ThingSpeak import ModeThingSpeak

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