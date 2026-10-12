import json
from pathlib import Path
import os
from requests.structures import CaseInsensitiveDict


class Mode:

    FOLDER_PATH = __file__+"/../../../"+"secrets/"

    def __init__(self):
        self._config =CaseInsensitiveDict( self.loadConfig())
        pass

    def loadConfig(self) -> CaseInsensitiveDict:
        try:
            with open(self.FOLDER_PATH+"config.json", "r", encoding="utf-8") as f:
                return CaseInsensitiveDict(json.load(f))
        except json.JSONDecodeError:
            print("loadConfig: load failed. Falling back to default config")
            with open(self.FOLDER_PATH+"default_config.json", "r", encoding="utf-8") as f:
                return CaseInsensitiveDict(json.load(f))

    def writeConfig(self, config: dict) -> None:
        base_config = self.loadConfig()
        base_config.update(config)
        with open(self.FOLDER_PATH+"config.json", "w", encoding="utf-8") as f:
            return json.dump(base_config, f, indent=3)

    def getUserInput(self, prompt: str, options: dict):
        userin = "some long phrase which is super unlikely to come up by accident - also jclkxhzhiuowajdaw+0sdvfudihb"
        print("super getuserinput")
        while userin not in options.keys():
            print("tryinnnggg")
            print(prompt)
            for k, v in options.items():
                print(f"{k} - {v}")
            print("asking for input")
            userin = input(
            ).upper()
            print("got", userin)
        print("returned", userin)
        return userin

    def validatePassword(self) -> bool:
        password = input("Enter the password:\n")
        ok = password == self._config["common"]["password"]
        if not ok:
            print("Error: Invalid password")
        return ok
        
    def setConfigEntry(self, subsystem: str, configEntry):
        if not self.validatePassword(): return
        print("Current value:", self.config[subsystem][configEntry])
        newName = input(f"Input the new {configEntry} name. (Press enter to cancel):\n")
        if newName == "":
            print("Cancelled update!")
            return
        self.writeConfig({subsystem: {configEntry :newName}})
        self._config =CaseInsensitiveDict( self.loadConfig())
        print("Successfully wrote", newName, "as the database name.")
        return newName