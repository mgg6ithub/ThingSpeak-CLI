from src.utils import Utils

import time
from src.thingspeak import ThingSpeak
import psutil


class Channel:
    def __init__(self, user_api_key, u, index, channel_dict):
        self.user_api_key = user_api_key
        self.u = u
        self.index = index
        self.channel_dict = channel_dict
        self.id = channel_dict['id']
        self.print_channel(index, channel_dict)

    def __str__(self):
        return

    # Method to print channels
    def print_channel(self, index, channel_dict):
        self.u.clear()
        field_index_list, field_index_names = self.view_channel_fields()

        self.u.printFormatedTable(["Nº", "NAME", "ID", "Created Date", "Description"],
                                  [[f" Channel {index} ", channel_dict['name'],
                                    channel_dict['id'], channel_dict['created_at'], channel_dict['description']]])
        self.u.printFormatedTable(["LATITUDE", "LONGITUDE", "ELEVATION", "LAST ENTRY"],
                                  [[channel_dict['latitude'], channel_dict['longitude'],
                                    channel_dict['elevation'], channel_dict['last_entry_id']]])
        self.u.printFormatedTable(["WRITE API KEY", "READ API KEY"],
                                  [[channel_dict['api_keys'][0]['api_key'], channel_dict['api_keys'][1]['api_key']]])

        self.u.printFormatedTable(field_index_list, [field_index_names])

        self.channel_menu()

    # Channel options
    def channel_menu(self):
        str_channel_banner = "OPCIONES DEL CANAL\n" \
                             "------------------\n\n" \
                             "1 -- Modificar canal\n\n" \
                             "2 -- See channel fields\n\n" \
                             "3 -- Delete the channel.\n\n" \
                             "4 -- Create fields for uploading data.\n\n" \
                             "5 -- Delete fields from channel.\n\n" \
                             "6 -- Upload data.\n\n" \
                             "7 -- Read field data.\n\n" \
                             "Enter \"back\" to go backwards"

        option = self.u.endless_terminal(str_channel_banner, "1", "2", "3", "4", "5", "6", "7", c="c")

        if option.__eq__("back"):
            return
        elif option.__eq__("1"):
            self.update_channels_information()
        elif option.__eq__("2"):
            self.view_channel_fields()
        elif option.__eq__("3"):
            i = input("Are you sure you want to delete the channel? y/n")
            if i == "y":
                req = ThingSpeak.remove_channel(self.id, self.user_api_key)
                if req == 200:
                    print("Channel successfully deleted!")
        elif option.__eq__("4"):
            self.create_fields_in_channel()
        elif option.__eq__("5"):
            self.remove_fields_from_channel()
        elif option.__eq__("6"):
            self.subir_datos_practica()
        elif option.__eq__("7"):
            self.read_data("1")
            self.read_data("2")
        i = input()

    # Method to update channel fields
    def update_channels_information(self):
        valid_fields = [
            "description",
            "field1",
            "latitude",
            "longitude",
            "elevation",
            "metadata",
            "name",
            "public_flag",
            "tags",
            "url"
        ]

        updated_information = {"api_key": self.user_api_key}
        print("Enter the field/s value you want to change(Enter \"ok\" to finish).")
        while True:
            i = self.u.endless_terminal("Type a field: ", *valid_fields, c="c")

            if i.__eq__("ok"):
                break

            new_value = input(f"Type a new value for {i}: ")
            updated_information[i] = new_value

        req = ThingSpeak.update_channel_information(self.id, updated_information)

        if req.status_code == 200:
            self.channel_dict = ThingSpeak.get_channel_settings(self.id, self.user_api_key).json()
            self.print_channel(self.index, self.channel_dict)

    # Method to view the fields of the channel
    def view_channel_fields(self):
        req = ThingSpeak.get_channel_fields(self.id, self.channel_dict['api_keys'][1]['api_key'])

        # fields_dict = {}

        if req.status_code == 200:
            channel_data = req.json()

            fields_index = []
            fields_name = []
            for i in range(1, 9):
                field = "field" + str(i)

                if field in channel_data['channel']:
                    # print(field + ":" + channel_data['channel'][field])
                    # fields_dict[field] = channel_data['channel'][field]
                    fields_index.append(field)
                    fields_name.append(channel_data['channel'][field])

            return fields_index, fields_name

    # Method to remove the fields froma a channel
    def remove_fields_from_channel(self):

        fichero_json = {"api_key": self.user_api_key}

        for ite in range(1, 9):
            fichero_json[f"field{ite}"] = ""
        r = Utils.make_request(method="put", url=f"https://api.thingspeak.com/channels/{self.id}.json",
                               json=fichero_json)
        print(r.status_code)
        if r.status_code == 200:
            print("Fields have been deleted")
            time.sleep(2)

    # Method to create fields from a channel
    def create_fields_in_channel(self):
        cont = 1
        i = None
        new_fields = {"api_key": self.user_api_key}

        while i is not "n" and cont <= 8:
            print("Enter the name for the field: ")
            new_fields["field" + str(cont)] = input("[" + str(cont) + "º campo]=")
            cont += 1
            print("Do you wan to create another field? [y/n]\n")
            i = input("->")

        req = Utils.make_request(method="put", url=f"https://api.thingspeak.com/channels/{self.id}.json",
                                 json=new_fields)
        if req.status_code == 200:
            print("New fields created.")
            time.sleep(2)

    # Method to upload data to a field
    # def upload_data_to_field(self):
    #     pass
    def subir_datos_practica(self):
        i = 0
        while i < 100:
            cpu = psutil.cpu_percent()  # USO DE LA CPU
            vm = psutil.virtual_memory()
            ram = vm.percent  # USO DE LA RAM

            self.mostrar_recursos_hardware(cpu, ram, size=30)
            i += 1
            time.sleep(0.5)
            Utils.make_request(method="post", url="https://api.thingspeak.com/update.json", json={
                "api_key": self.channel_dict['api_keys'][0]['api_key'],
                "field1": cpu,
                "field2": ram
            })

    # GRAFICO TIMIDO para que se vea algo al subir los datos
    # Se podria implementar con un thread y meterle la actualizacion cada 2 segundos para que se vea mas real
    def mostrar_recursos_hardware(self, cpu, ram, size=50):
        cpu_p = (cpu / 100.0)
        cpu_carga = ">" * int(cpu_p * size) + "-" * (size - int(cpu_p * size))

        ram_p = (ram / 100.0)
        ram_carga = ">" * int(ram_p * size) + "-" * (size - int(ram_p * size))

        print(f"\rUSO DE LA CPU: |{cpu_carga}| {cpu:.2f}%", end="")
        print(f"\tUSO DE LA RAM: |{ram_carga}| {ram:.2f}%", end="\r")

    # Method to read data from on especific field
    def read_data(self, field_id):
        url_read_data_field = f"https://api.thingspeak.com/channels/{self.id}/fields/{field_id}.json?results=100&api_key={self.channel_dict['api_keys'][1]['api_key']}"
        req = Utils.make_request(method="GET", url=url_read_data_field)

        print(req.status_code)
        print(req.json()['feeds'])