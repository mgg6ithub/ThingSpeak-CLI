from src.thingspeak import ThingSpeak
from src.utils import Utils
from src.canal import Channel

from colorama import Fore, init
import signal
import sys
import os
import pdb

# Instancia global para utilizar la clase utils
u = Utils()
init()


def signal_handler(signum, frame):
    os.system("clear")
    print(Fore.RED + "Saliendo de TS")
    u.wait_animation(1)
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


# Metodo para comprobar la clave ingresada
def checkUserApyKey(apy_key):
    u.clear()
    init()
    req = u.make_request(method="GET",
                         url=f"https://api.thingspeak.com/channels.json?api_key={apy_key}")

    if req.status_code == 200:
        return True
    elif req.status_code == 401:
        return False


def login():
    while True:
        u.clear()
        str_banner = "1. Iniciar Sesion con CREDENCIALES.\n\n" \
                     "2. Iniciar sesion con APY KEY.\n\n" \
                     "CTRL + C para salir en cualquier momento.\n"

        option = u.endless_terminal(str_banner, "1", "2")
        u.clear()

        if option == "2":
            api_key = input("Introduce tu apy key: ")

            if checkUserApyKey(api_key):
                print(Fore.GREEN + "Successfull " + Fore.WHITE + "APY KEY provided.")
                u.wait_animation(1)
                # ts = ThingSpeak(api_key, u)
                # menu_principal(api_key)
            else:
                print(Fore.RED + "Wrong " + Fore.WHITE + "APY KEY provided.")
                u.wait_animation(1)
        i = input()


# Menu de la cuenta ThigSpeak
def menu_principal(api_key):
    str_banner = "1 -- Ver canales públicos.\n\n" \
                 "2 -- Ver canales privados.\n\n" \
                 "3 -- Ver todos los canales\n\n"

    option = u.endless_terminal(str_banner, "1", "2", "3")

    ts = ThingSpeak(api_key, u)

    if option == "1":
        indexes = ts.print_channel_index(ts.public_channels)
    elif option == "2":
        indexes = ts.print_channel_index(ts.private_channels)
    else:
        indexes = ts.print_channel_index(ts.all_channels)

    i = u.endless_terminal("\nSelect a channel.\nOr enter \"back\" to go backwards.", *indexes.keys(), c="c")

    # Recursive call
    if i.__eq__("back"):
        menu_principal(api_key)

    Channel(api_key, u, i, indexes[i])
    menu_principal(api_key)


if __name__ == '__main__':
    # main()
    # login()
    menu_principal("0WX1WIYR7G3QMKUR")
    # ts = ThingSpeak("0WX1WIYR7G3QMKUR", u)

    # print(ts.__str__())
