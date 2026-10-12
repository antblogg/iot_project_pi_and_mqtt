from .Mode import Mode

class MainMenu(Mode):
    def __init__(self):
        super().__init__()

    def getUserInput(self):
        print("getuserinput")
        prompt = "Choose a subfunction"
        options = {
            "S": "Show system summary",
            "D": "Database",
            "M": "MQTT",
            "T": "ThingSpeak",
        #    "W": "Wifi",
            "Q": "Quit",
        }
        return super().getUserInput(prompt, options)