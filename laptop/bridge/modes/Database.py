
from pymongo import MongoClient
from bridge.modes.Mode import Mode

class ModeDatabase(Mode):
    def __init__(self):
        super().__init__()
        hostname = "TODO"
        portnumber = 27017
        self.mongo = MongoClient(
            host=hostname,
            port=portnumber
        )
        
    def enterMode(self):
        self.printMenu()
        while True:
            userIn = self.getUserInput()
            match userIn:
                case "TODO":
                    pass



     
    def printMenu(self) -> None:
        print("Now in database mode.")
        print("Current status:")
        print(f"SSID: {self.config["Wifi"]["SSID"]}")
        print(f"Password: {"*"*len(self.config["Wifi"]["password"])}")
        print(f"Connection status: {}")

    def getUserInput(self)-> str:
        prompt = "Select next action"
        options = {
            "P" : "Show password",
            "Q": "Quit",
            }
        return super().getUserInput(prompt, options)


