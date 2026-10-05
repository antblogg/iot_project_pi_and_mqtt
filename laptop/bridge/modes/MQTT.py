from bridge.modes.Mode import Mode


class ModeMQTT(Mode):
    def __init__(self):
        super().__init__()
        input("You're a MQTT pie now son")