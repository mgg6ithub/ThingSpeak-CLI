import os
import requests
import sys
import platform
import time
import curses


class Utils:

    def __init__(self):
        self.clear_command = "cls" if platform.system() == "Windows" else "clear"
        curses.initscr()
    # Default checkings

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
        curses.curs_set(0)

    def show_cursor(self):
        curses.curs_set(1)

    def cleanup(self):
        curses.endwin()

    # Method to make http requests
    def make_request(**self):
        try:
            r = requests.request(**self)
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
