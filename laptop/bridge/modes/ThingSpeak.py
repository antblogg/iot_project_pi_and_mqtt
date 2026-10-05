from bridge.modes.Mode import Mode
import requests
import time

class ModeThingSpeak(Mode):
    def __init__(self):
        super().__init__()
        self.config = self.loadConfig()

        input("You're Terry now son")

    def enterMode(self):
        self.printMenu()
        self.getUserInput()

     
    def printMenu(self) -> None:
        print("Now in WiFi mode.")
        print("Current status:")
        print(f"Connection status: {"Connected" if self.isConnected() else "Disconnected"}")

    def getUserInput(self)-> str:
        prompt = "Select next action"
        options = {
            "R": "Refresh status",
            "B": "Back",
            "Q": "Quit",
            }
        while True:
         super().getUserInput(prompt, options)

    def getLastReading(self):
        read_api_key = self.config["thingspeak"]["read_API_key"]
        lastReading = requests.get("")

    def isConnected(self):
        lastReading = self.getLastReading()



