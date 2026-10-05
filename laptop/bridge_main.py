
import argparse
import json
from pathlib import Path
from bridge.modes.MainMenu import MainMenu
from bridge.modes.Database import ModeDatabase
from bridge.modes.MQTT import ModeMQTT
from bridge.modes.ThingSpeak import ModeThingSpeak
from bridge.modes.Wifi import ModeWifi
from requests.structures import CaseInsensitiveDict

class Bridge:
    FOLDER_PATH = __file__ + "/../"
    def __init__(self):
        self.config = self.loadConfig()
        self.wifi = ModeWifi()
        self.database = ModeDatabase()
        self.thingspeak = ModeThingSpeak()
        self.mqtt = ModeMQTT()

    def loadConfig(self) -> CaseInsensitiveDict:
        try:
            with open(self.FOLDER_PATH+"config.json", "r", encoding="utf-8") as f:
                return CaseInsensitiveDict(json.load(f))
        except json.JSONDecodeError:
            print("loadConfig: load failed. Falling back to default config")
            with open(self.FOLDER_PATH+"default_config.json", "r", encoding="utf-8") as f:
                return CaseInsensitiveDict(json.load(f))


def main():

    mainMenu = MainMenu()

    while True:
        option = mainMenu.getUserInput()
        match option:
            case "D":

                ModeDatabase()
            case "M":
                ModeMQTT()
            case "T":
                ModeThingSpeak()
            case "W": # commented out of menu options 
                ModeWifi()
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
