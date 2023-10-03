import requests
from colorama import Fore, init
import time


class ThingSpeak:

    def __init__(self, user_apy_key, u):
        self.user_apy_key = user_apy_key
        self.u = u

    def __str__(self):
        print(f"Tu apy key es: {self.user_apy_key}")

    # Menu de la cuenta ThigSpeak
    def main_menu(self):
        str = "Menu principal\n" \
              "1 -- Ver canales\n" \
              "2 -- Salir al menu principal\n"

        i = self.u.endless_terminal(str, "1", "2")

        if i == "1":
            length, channels_list = self.get_channels_list()
            if length == 0:
                print("No hay canales")
            else:
                print(f"Hay {length} canales")
                for c in range(0, length):
                    print(channels_list.json()[c])

                i = input()
                self.main_menu()
        elif i == "2":
            return

    # Method to get the list of all existing channels
    def get_channels_list(self):
        req = self.u.make_request(method="GET",
                                  url=f"https://api.thingspeak.com/channels.json?api_key={self.user_apy_key}")
        return len(req.json()), req

    # Method to get the list of all public channels
    def list_public_channels(self):
        req = self.u.make_request(method="GET",
                                  url="https://api.thingspeak.com/users/mwa0000031155118/channels.json")

        print(req.status_code)
        print(req.json())
        print(req.text)
        i = input()

    # Method to get all the channel settings
    def get_channel_settings(self, id):
        req = self.u.make_request(method="GET",
                                  url=f"https://api.thingspeak.com/channels/{id}.json?api_key={self.user_apy_key}")

        print(req.status_code)
        print(req.json())
        print(req.text)
        i = input()

    # Metodo para obtener los objetos json de los canales a partir de la lista
    def get_channels_json(self, list):
        pass
