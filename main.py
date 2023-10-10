from src.thingspeak import ThingSpeak
from src.utils import Utils

from colorama import Fore, init
import signal
import sys
import os

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
                menu_principal(api_key)
            else:
                print(Fore.RED + "Wrong " + Fore.WHITE + "APY KEY provided.")
                u.wait_animation(1)
        i = input()


# Menu de la cuenta ThigSpeak
def menu_principal(api_key):
    ts = ThingSpeak(api_key, u)

    print(f"En total hay {ts.get_channels_length()} canales\n\n")

    req = ts.get_channels_list()

    u.printRequest(req)

    print(f"En total hay {ts.get_public_channels_length()} canales publicos\n\n")

    req1 = ts.get_public_channels()

    u.printRequest(req1)

    private_channels = 0

    for c in range(0, ts.get_channels_length()):
        if not req.json()[c]["public_flag"]:
            private_channels += 1

    print(f"En total hay {str(private_channels)} canales privados")

    # ts.get_channel_settings("2289652")

    # print()
    #
    # length, req1 = ts.get_channels_list()
    # print(req1.json()[0])
    #
    # # ts.main_menu()
    # # ts.read_settings()
    #
    # str_banner = "Menu principal\n" \
    #              "1 -- Ver canales\n" \
    #              "2 -- Salir al menu principal\n"
    #
    # i = self.u.endless_terminal(str, "1", "2")
    #
    # if i == "1":
    #     length, channels_list = self.get_channels_list()
    #     if length == 0:
    #         print("No hay canales")
    #     else:
    #         print(f"Hay {length} canales")
    #         for c in range(0, length):
    #             self.u.printFormatedTable(["ID", "NAME"],
    #                                       [[channels_list.json()[c]["id"], channels_list.json()[c]["name"]]])
    #
    #         i = input()
    #         self.main_menu()
    # elif i == "2":
    #     return


if __name__ == '__main__':
    # main()
    login()
