from src.thingspeak import ThingSpeak
from src.utils import Utils

from colorama import Fore, Back, Style, init
import requests
import signal
import sys
import time
import os


# login_url = "https://thingspeak.com/login?skipSSOCheck=true"
#
# email = "yaxeb66148@nickolis.com"
# password = "Cuenta2314"


def signal_handler(signum, frame):
    os.system("clear")
    print()
    print(Fore.RED + "Saliendo de TS")
    time.sleep(1)
    sys.exit(1)


def main():
    # URL inicial de inicio de sesión en ThingSpeak
    login_url = 'https://thingspeak.com/login?skipSSOCheck=true'

    # Tus credenciales de inicio de sesión
    email = 'tu_correo_electronico'
    password = 'tu_contraseña'

    # Realiza la primera solicitud GET a la página de inicio de sesión
    session = requests.session()
    response = session.get(login_url)

    print(response.text)


def menu():
    signal.signal(signal.SIGINT, signal_handler)
    init()
    u = Utils()

    while True:
        u.clear()
        print("1. Iniciar Sesion con CREDENCIALES.\n")
        print("2. Iniciar sesion con APY KEY.\n")
        print("CTRL + C para salir en cualquier momento.\n")

        i = input(Fore.GREEN + "ts:> " + Fore.WHITE)

        if i == "2":
            apy_key = input("Introduce tu apy key: ")

            ts = ThingSpeak(apy_key)
            c = ts.checkUserApyKey()
            try:
                u.hide_cursor()
                u.wait(2)
                u.show_cursor()
                u.clear()
            finally:
                u.cleanup()

            if c:
                print("MENU DEL CANAL")

                i = input()


if __name__ == '__main__':
    # main()
    menu()
