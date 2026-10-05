import json
from pathlib import Path
import os
from requests.structures import CaseInsensitiveDict


class Mode:

    FOLDER_PATH = __file__+"/../../../"+""

    def __init__(self):
        self.config = self.loadConfig()
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
        while userin not in options.keys():
            print(prompt)
            for k, v in options.items():
                print(f"{k} - {v}")
            userin = input(
            ).upper()
        return userin
        