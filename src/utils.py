import os
import requests
import sys
import platform
import time
import json
from colorama import Fore
from tabulate import tabulate

# Define la variable global
clear_command = "cls" if platform.system() == "Windows" else "clear"
menu_stack = []


class Utils:

    def __init__(self):
        self.clear_command = "cls" if platform.system() == "Windows" else "clear"

    @staticmethod
    # Clear screen method
    def clear():
        return_code = os.system(clear_command)
        if return_code != 0:
            print("Error al limpiar la pantalla")

    @staticmethod
    def printRequest(req):
        print(req.status_code)
        print(req.json())

    @staticmethod
    def printFormatedTable(tableHeaders, tableData):
        table = tabulate([tableHeaders, *tableData], headers="firstrow", tablefmt="simple_grid", stralign="center")
        print(table)
        print("\n")

    @staticmethod
    # Wait method
    def wait(t):
        try:
            time.sleep(t)
        except KeyboardInterrupt:
            print("Has interrumpido la espera del programa.\n")

    @staticmethod
    def hide_cursor():
        print("\x1b[?25l")  # hidden

    @staticmethod
    def show_cursor():
        print("\x1b[?25h")  # shown

    @staticmethod
    # Wait and hide cursor
    def wait_animation(time_to_wait):
        Utils.hide_cursor()
        Utils.wait(time_to_wait)
        Utils.show_cursor()

    @staticmethod
    # Endless ThingSpeak -CLI terminal
    def endless_terminal(message, *options, c=None, exit=False, tty=True):

        if c is None:
            Utils.clear()

        if not tty:
            return input(message)

        print(message)
        while True:
            i = str(input(Fore.GREEN + "ts> " + Fore.WHITE))
            if i in options or i.__eq__("b") or exit:
                return i

    @staticmethod
    # Metodo para convertir una lista a un objeto json
    def list_to_json(lista):
        return json.dumps(lista)

    @staticmethod
    # Method to make http requests
    def make_request(**kwargs):
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

    @staticmethod
    def push(menu_method):
        menu_stack.append(menu_method)

    @staticmethod
    def pop():
        if not Utils.isEmpty():
            menu_stack.pop()


    @staticmethod
    def isEmpty():
        return len(menu_stack) == 0