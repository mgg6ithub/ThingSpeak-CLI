from src.utils import Utils

import requests
from colorama import Fore, init
import time


class ThingSpeak:

    def __init__(self, user_apy_key):
        self.user_apy_key = user_apy_key
        self.u = Utils()

    def __str__(self):
        print(f"Tu apy key es: {self.user_apy_key}")

    def checkUserApyKey(self):
        self.u.clear()
        init()
        req = Utils.make_request(method="GET",
                                 url=f"https://api.thingspeak.com/channels.json?api_key={self.user_apy_key}")

        if req.status_code == 200:
            print(Fore.GREEN + "Successfull " + Fore.WHITE + "APY KEY provided.")
            return True
        elif req.status_code == 401:
            print(Fore.RED + "Wrong " + Fore.WHITE + "APY KEY provided.")
            return False

