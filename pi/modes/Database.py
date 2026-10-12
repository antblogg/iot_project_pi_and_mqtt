
from requests.structures import CaseInsensitiveDict
from pymongo import MongoClient
from pymongo import DESCENDING
import sys
import subprocess
from bson import ObjectId
import threading
from multiprocessing import Queue

import signal
import time


from .Mode import Mode

class ModeDatabase(Mode):
    def __init__(self, messages: Queue): 
        super().__init__()
        self.config =CaseInsensitiveDict( self._config)
        self.messages = messages
        self.mongoclient = None
        self.backgroundThread = threading.Thread(target=self.buildABridge, daemon=True)
        self.backgroundThread.start()
        connected = self.tryConnect()

    def tryConnect(self)-> bool:
        self.menuStopFlag = False
        if self.mongoclient is not None:
            self.mongoclient.close()

        hostName = self.config.get("mOnGodB").get("connectionString")
        databaseName = self.config.get("mOnGodB").get("database")
        collectionName = self.config.get("mOnGodB").get("collection")

        self.mongoclient = MongoClient(host=hostName)
        self.database = self.mongoclient.get_database(databaseName)
        self.collection = self.database.get_collection(collectionName)

        tryFindOne = threading.Thread(target=self.collection.find_one, daemon=False)
        tryFindOne.start()
        tryFindOne.join(timeout=1.0)
        itemFound = not tryFindOne.is_alive()
        return itemFound
        
    def isConnected(self):
        return self.tryConnect()
        
    def enterMode(self):
        self.printMenu()
        while True:
            userIn = self.getUserInput()
            match userIn:
                case "S":
                    self.printMenu()
                case "C":
                    self.setCollectionName()
                case "D":
                    self.setDatabaseName()
                case "L":
                    self.liveView()
                case "B":
                    return
                case "Q":
                    sys.exit()

    def printMenu(self) -> None:
        print("Now in database mode.")
        print("Current status:")
        print(f"Connection status: {"Connected" if self.isConnected() else "Disconnected"}")
        print(f"Database name: {self.config["monGodB"]["database"]}")
        print(f"Collection name: {self.config["monGodB"]["collection"]}")

    def getUserInput(self)-> str:
        prompt = "Select next action"
        options = {
            "S": "Show database status",
            "C": "Set database name (password protected)",
            "D":"Set database name (password protected)", 
            "L": "Show live view of database inserts",
            "B": "Go back",
            "Q": "Quit",
            }
        return super().getUserInput(prompt, options)


    def setCollectionName(self):
        newName = self.setConfigEntry("mongodb","collection")
        self.config =CaseInsensitiveDict( self._config)
        if newName is not None:
            self.collection = newName
            _ = self.tryConnect()

    def setDatabaseName(self):
        newName = self.setConfigEntry("mongodb","database")
        self.config =CaseInsensitiveDict( self._config)
        if newName is not None:
            self.collection = newName
            _ = self.tryConnect()

    def liveView(self):
        self.menuStopFlag = False
        defaultSignalHandler =  signal.signal(signal.SIGINT, self._setStop)
        connStatus = "Connected" if self.isConnected() else "Disconnected"
        while not self.menuStopFlag:
            subprocess.run(["cls"], shell=True)
            print(f"Connection status: {connStatus}")
            print(f"Database name: {self.config["monGodB"]["database"]}")
            print(f"Collection name: {self.config["monGodB"]["collection"]}")
            print("Last five measurements:")
            items = self.collection.find().sort("_id", -1).limit(5)
            for item in items:
                print(""+
                    "itemID:", item.get("_id"),"\t",
                    "timestamp:", item.get("timestamp"),"\t",
                    "measurement:",item.get("measurement"),"\t"
                    )
            time.sleep(1)
        signal.signal(signal.SIGINT, defaultSignalHandler)
        
    def _setStop(self,event, signal):
        self.menuStopFlag = True

    def buildABridge(self):
        numberOfFailedRetries = 0
        maxRetryDelayCount = 5
        while True:
            messages=[]
            messageRead=False
            while not self.messages.empty():
                messageRead = True
                message = self.messages.get(timeout=1+0.5*numberOfFailedRetries)
                messages.append(message)
            if messageRead:
                if numberOfFailedRetries > 0: numberOfFailedRetries -= 1
            else:
                if numberOfFailedRetries < maxRetryDelayCount: numberOfFailedRetries += 1
            if len(messages) > 0:
                self.collection.insert_many(messages)
            time.sleep(numberOfFailedRetries)
            

