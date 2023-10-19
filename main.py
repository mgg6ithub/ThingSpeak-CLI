from src.thingspeak import ThingSpeak
from src.utils import Utils
from src.canal import Channel

import keyboard
from colorama import Fore, init
import signal
import sys
import os
import pdb

# u = Utils()
init()


# Method to handle the exit of the program when Ctrl + C is pressed
def signal_handler(signum, frame):
    Utils.clear()
    print(Fore.RED + "Saliendo de TS")
    Utils.wait_animation(1)
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


# Metodo para comprobar la clave ingresada
def checkUserApyKey(user_api_key):
    Utils.clear()
    init()
    req = Utils.make_request(method="GET",
                             url=f"https://api.thingspeak.com/channels.json?api_key={user_api_key}")

    if req.status_code == 200:
        return True
    elif req.status_code == 401:
        return False


def login():
    while True:
        Utils.clear()
        str_banner = "1. Iniciar Sesion con CREDENCIALES.\n\n" \
                     "2. Iniciar sesion con APY KEY.\n\n" \
                     "CTRL + C para salir en cualquier momento.\n"

        option = Utils.endless_terminal(str_banner, "1", "2")
        Utils.clear()

        if option == "2":
            user_api_key = input("Introduce tu apy key: ")

            if checkUserApyKey(user_api_key):
                print(Fore.GREEN + "Successfull " + Fore.WHITE + "APY KEY provided.")
                Utils.wait_animation(1)
                # ts = ThingSpeak(user_api_key, u)
                # menu_principal(user_api_key)
            else:
                print(Fore.RED + "Wrong " + Fore.WHITE + "APY KEY provided.")
                Utils.wait_animation(1)
        i = input()


# ThingSpeak menu Method
def menu_principal(user_api_key):
    ts = ThingSpeak(user_api_key)

    if ts.hayCanales:

        str_banner = "1 -- Ver canales públicos.\n\n" \
                     "2 -- Ver canales privados.\n\n" \
                     "3 -- Ver todos los canales\n\n"

        option = Utils.endless_terminal(str_banner, "1", "2", "3")

        if option.__eq__("b"):
            keyboard.press_and_release('ctrl+c')

        if option == "1":
            indexes = ts.print_channel_index(ts.public_channels)
        elif option == "2":
            indexes = ts.print_channel_index(ts.private_channels)
        else:
            indexes = ts.print_channel_index(ts.all_channels)

        i = Utils.endless_terminal("\nSelect a channel.\nOr enter \"back\" to go backwards.", *indexes.keys(), c="c")

        Channel(user_api_key, i, indexes[i])

    else:
        i = Utils.endless_terminal("You dont have any channels in this account.\nDo you want to create one? [y/n] ",
                               tty=False)
        if i.__eq__("y"):
            ts.create_channel(user_api_key)
        else:
            pass
    menu_principal(user_api_key)


if __name__ == '__main__':
    menu_principal("0WX1WIYR7G3QMKUR")
