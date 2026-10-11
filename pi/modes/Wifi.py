from bridge.modes.Mode import Mode
import sys
import socket



class WiFi:
    # Try connection to a set of reliable providers to check if wifi connected.
    @staticmethod
    def isConnected():
        connectionAddresses = [
            "1.1.1.1", # cloudflare
            "8.8.8.8", # google
            "208.67.222.222" # openDNS
            ]
        for address in connectionAddresses:
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                return True
            except OSError:
                pass
        return False



class ModeWifi(Mode):
    def __init__(self):
        super().__init__()
        self.wifi = WiFi()

    def enterMode(self):
        self.printMenu()
        self.getUserInput()

     
    def printMenu(self) -> None:
        print("Now in WiFi mode.")
        print("Current status:")
        #print(f"SSID: {self.config["Wifi"]["SSID"]}")
        #print(f"Password: {"*"*len(self.config["Wifi"]["password"])}")
        print(f"Connection status: {"Connected" if self.wifi.isConnected() else "Disconnected"}")

    def getUserInput(self)-> str:
        prompt = "Select next action"
        options = {
            "R": "Refresh status",
            "B": "Back",
            "Q": "Quit",
            }
        while True:
         super().getUserInput(prompt, options)


