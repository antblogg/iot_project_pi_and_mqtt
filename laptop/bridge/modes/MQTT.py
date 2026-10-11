
import json
import time
from bridge.modes.Mode import Mode
import paho.mqtt.client as paho
import random
from requests.structures import CaseInsensitiveDict
import subprocess
import signal
import sys
from multiprocessing import Queue

class ModeMQTT(Mode):
    def __init__(self, sharedQueue: Queue) -> None:
        super().__init__()
        client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.config: CaseInsensitiveDict = self._config["MQTT"]
        self.sharedQueue = sharedQueue
        
        broker = self.config["broker"]
        port = int(self.config["port"])
        self.connectionStatus = False
        self.isPrinting = False
        self.stopFlag = False
        self.client = paho.Client(
            client_id=client_id,
            callback_api_version=paho.CallbackAPIVersion.VERSION2,
        )
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(broker, port)
        self.client.loop_start()
        self.client.subscribe(self.config["topic"])
        self.client.on_message = self.on_message

    def enterMode(self):
        self.printMenu()
        while True:
            userIn = self.getUserInput()
            match userIn:
                case "S":
                    self.printMenu()
                case "I":
                    self.setBrokerIp()
                case "T":
                    self.setTopic()
                case "L":
                    self.liveView()
                case "B":
                    return
                case "Q":
                    sys.exit()

    def liveView(self):
        import os
        subprocess.run(["cls"], shell=True)
        defaultSignalHandler =  signal.signal(signal.SIGINT, self._setStop)
        print("Displaying all recieved messages:")
        time.sleep(3)
        self.isPrinting = True
        while not self.stopFlag:
            time.sleep(0.1)
        self.isPrinting = False
        signal.signal(signal.SIGINT, defaultSignalHandler)

    def printMenu(self) -> None:
        print("Now in MQTT mode.")
        print(f"Connection status: {"Connected" if self.isConnected() else "Disconnected"}")

    def getUserInput(self)-> str:
        prompt = "Select next action"
        options = {
            "S": "Show MQTT status",
            "I": "Set IP of the broker (password protected)",
            "T": "Set Topic name (password protected)", 
            "L": "Show live view of MQTT messages",
            "B": "Go back",
            "Q": "Quit",
            }
        return super().getUserInput(prompt, options)


    def setTopic(self):
        self.setConfigEntry("MQTT","topic")
        self.config = self._config["MQTT"]

    def setBrokerIp(self):
        if not self.validatePassword(): return
        print(f"Broker IP: {self.config["broker"]}/{self.config["port"]}")
        newName = input(f"Input the new broker name. (Press enter to cancel):\n")
        if newName == "":
            print("Cancelled update!")
            return
        [broker, port] = newName.split("/")
        self.writeConfig({"MQTT": {"broker" : broker}})
        self.writeConfig({"MQTT": {"port" : port}})
        self.config = self._config["MQTT"]
    
    def on_connect(self,client, userdata, flags, reason_code, properties):
        self.connectionStatus = True

    def on_disconnect(self,client, userdata, disconnect_flags, reason_code, properties):
        self.connectionStatus = False
        print("Mqqtt disconoeted")

    def isConnected(self):
        return self.connectionStatus

    def on_message(self,client, userdata, msg: paho.MQTTMessage):
        x = msg.payload.decode()
        d: dict = json.loads(x)
        if self.isPrinting:
            print(json.dumps(d, indent=1))
        self.sharedQueue.put_nowait(d)

    def publishMessage(self, msg: dict):
        self.client.publish(
            topic=self.config["topic"],
            payload=json.dumps(msg, indent=2)
            )

    def _setStop(self, event, signal):
        self.stopFlag = True


