from bridge.modes.Mode import Mode
import requests
import time
import sys

class ModeThingSpeak(Mode):
    def __init__(self):
        super().__init__()
        self.config = self._config["thingspeak"]


    def enterMode(self):
        self.printMenu()
        while True:
            option = self.getUserInput()
            match option:
                case "S":
                    break
                    self.printMenu()
                case "B":
                    return
                case "Q":
                    sys.exit()

     
    def printMenu(self) -> None:
        print("Now in Thingspeak mode.")
        print("Current status:")
        print(f"Connection status: idk")#{"Connected" if self.isConnected() else "Disconnected"}")

    def getUserInput(self)-> str:
        prompt = "Select next action"
        options = {
            #"S": "Show status",
            "B": "Back",
            "Q": "Quit",
            }
        return super().getUserInput(prompt, options)

    def getLastReading(self):
        write_api_key = self.config["thingspeak"]["write_API_key"]
        lastReading = requests.get("")

    def isConnected(self):
        return True
        



