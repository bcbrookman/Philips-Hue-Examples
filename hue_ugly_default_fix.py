# When powering on after a power failure or light switch on/off event, bulbs occasionally do not follow the power-on
# rules defined in the Hue app and default to a warm yellow. This script checks every 30 seconds and changes the color
# of the bulbs to the "Energize" scene.

import json
import os
import requests
import time

username = os.environ['HUE_USERNAME']
hub = os.environ['HUE_HUB']
api_url = f"http://{hub}/api/{username}/lights"

headers = {"Content-Type": "application/json"}


ugly_default_xy = {
    "on": True,
    "bri": 254,
    "xy": [
        0.4574,
        0.41
    ]
}

ugly_default_ct = {
    "on": True,
    "bri": 254,
    "xy": [
        0.4573,
        0.41
    ]
}

energize = {
    "on": True,
    "bri": 254,
    "xy": [
        0.3143,
        0.3301
    ]
}


while True:
    lights_dict = requests.get(api_url).json()

    for light, info in lights_dict.items():
        if info["state"]["on"] and info["state"]["reachable"]:

            if info["state"]["colormode"] == "xy" and "xy" in info["state"]:
                if info["state"]["xy"][0] == ugly_default_xy["xy"][0] \
                        and info["state"]["xy"][1] == ugly_default_xy["xy"][1] \
                        and info["state"]["bri"] == ugly_default_xy["bri"]:
                    requests.put(f"{api_url}/{light}/state", data=json.dumps(energize), headers=headers)

            elif info["state"]["colormode"] == "ct" and "xy" in info["state"]:
                if info["state"]["xy"][0] == ugly_default_ct["xy"][0] \
                        and info["state"]["xy"][1] == ugly_default_ct["xy"][1] \
                        and info["state"]["bri"] == ugly_default_ct["bri"]:
                    requests.put(f"{api_url}/{light}/state", data=json.dumps(energize), headers=headers)

    time.sleep(30)
