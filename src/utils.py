import os
import requests
import sys
import platform


class Utils:

    def __init__(self):
        self.clear_command = self.check_os_type()

    # Default checkings
    # Os detection
    def check_os_type(self):
        os_type = platform.system()

        if os_type == "Windows":
            return "cls"
        elif os_type == "Linux":
            return "clear"
        elif os_type == "Darwin":
            return "clear"
        else:
            pass

    # Program Utils
    def clear(self):
        return_code = os.system(self.clear_command)
        if return_code != 0:
            print("Error al limpiar la pantalla")

    # METODO PARA REALIZAR PETICIONES HTTP
    @staticmethod
    def realizar_peticion(**kwargs):
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
