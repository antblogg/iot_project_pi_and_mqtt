from time import sleep
import subprocess
import json

def main():
    with open(__file__+"/../../config.json") as f:
        config: dict = json.load(f)
    path_to_mqtt = config.get("mqtt_run_filepath")
    subprocess.run([path_to_mqtt])

    # just run the mqtt server script and then
    while True:
        sleep(10)
if __name__ == "__main__":
    main()