from src.thingspeak import ThingSpeak
from src.utils import Utils

from colorama import Fore, Back, Style, init
import requests
import signal
import sys
import time
import os

# Instancia global para utilizar la clase utils
u = Utils()


def signal_handler(signum, frame):
    os.system("clear")
    print(Fore.RED + "Saliendo de TS")
    u.wait_animation(1)
    sys.exit(1)


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

    while True:
        u.clear()
        print("1. Iniciar Sesion con CREDENCIALES.\n")
        print("2. Iniciar sesion con APY KEY.\n")
        print("CTRL + C para salir en cualquier momento.\n")

        i = input(Fore.GREEN + "ts:> " + Fore.WHITE)
        u.clear()

        if i == "2":
            apy_key = input("Introduce tu apy key: ")

            if checkUserApyKey(apy_key):
                print(Fore.GREEN + "Successfull " + Fore.WHITE + "APY KEY provided.")
                ts = ThingSpeak(apy_key, u)
                u.wait_animation(1)

                ts.main_menu()
                # ts.read_settings()
            else:
                print(Fore.RED + "Wrong " + Fore.WHITE + "APY KEY provided.")
                u.wait_animation(1)
        i = input()


if __name__ == '__main__':
    # main()
    menu()
