import os
import requests
import sys
import platform
import time
import json


class Utils:

    def __init__(self):
        self.clear_command = "cls" if platform.system() == "Windows" else "clear"

    # Clear screen method
    def clear(self):
        return_code = os.system(self.clear_command)
        if return_code != 0:
            print("Error al limpiar la pantalla")

    # Wait method
    def wait(self, t):
        try:
            time.sleep(t)
        except KeyboardInterrupt:
            print("Has interrumpido la espera del programa.\n")

    def hide_cursor(self):
        print("\x1b[?25l") # hidden

    def show_cursor(self):
        print("\x1b[?25h") # shown

    # Wait and hide cursor
    def wait_animation(self, time_to_wait):
        self.hide_cursor()
        self.wait(time_to_wait)
        self.show_cursor()

    # Metodo para convertir una lista a un objeto json
    def list_to_json(self, lista):
        return json.dumps(lista)

    # Method to make http requests
    def make_request(self, **kwargs):
        try:
            r = requests.request(**kwargs)
        except requests.exceptions.HTTPError as err:
            # print(f"MEDOTOD: {tipo}")
            print("Informacion del error -> " + err.args[0])
        except requests.exceptions.ConnectionError as err:
            # print(f"MEDOTOD: {tipo}")
            print(err.args[0])
            print("Error al conectarse. Intentos maximos superados.")
        except requests.exceptions.InvalidSchema as err:
            # print(f"MEDOTOD: {tipo}")
            print(err.args[0])
            print("Comprueba que el protocolo es correcto.\nEjemplo -> https://")
        else:
            return r
