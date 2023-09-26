import requests
from colorama import Fore, init
import time


class ThingSpeak:

    def __init__(self, user_apy_key):
        self.user_apy_key = user_apy_key

    def __str__(self):
        print(f"Tu apy key es: {self.user_apy_key}")

    def checkUserApyKey(self):
        init()
        req = requests.request(method="GET",
                               url=f"https://api.thingspeak.com/channels.json?api_key={self.user_apy_key}")

        if req.status_code == 200:
            print(Fore.GREEN + "Successfull " + Fore.WHITE + "APY KEY.")
            print(req.status_code)
        elif req.status_code == 401:
            print(Fore.RED + "Wrong " + Fore.WHITE + "APY KEY.")
            print(req.text)

        i = input()
