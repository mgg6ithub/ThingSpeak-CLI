from src.utils import Utils

import time
from progress.bar import IncrementalBar
from tqdm import tqdm
from src.thingspeak import ThingSpeak
import psutil
from tabulate import tabulate
import re

class Channel:
    def __init__(self, user_api_key, index, channel_dict):
        self.user_api_key = user_api_key
        self.index = index
        self.channel_dict = channel_dict
        self.id = channel_dict['id']

    def __str__(self):
        return

    # Method to print channels
    # def print_channel(self, index, channel_dict):
    #     Utils.clear()
        
    #     Utils.printFormatedTable(["Nº", "NAME", "ID", "Created Date", "Description"],
    #                             [[f" Channel {index} ", channel_dict['name'],
    #                             channel_dict['id'], Utils.format_date(channel_dict['created_at']), channel_dict['description']]])
    #     # Utils.printFormatedTable(["LATITUDE", "LONGITUDE", "ELEVATION", "LAST ENTRY"],
    #     #                         [[channel_dict['latitude'], channel_dict['longitude'],
    #     #                         channel_dict['elevation'], channel_dict['last_entry_id']]])
    #     # Utils.printFormatedTable(["WRITE API KEY", "READ API KEY"],
    #     #                         [[channel_dict['api_keys'][0]['api_key'], channel_dict['api_keys'][1]['api_key']]])
        
    #     # Check fields of the channels  
    #     fields_of_channel = self.view_channel_fields()
        

    # Channel options
    def channel_menu(self, index, channel_dict):
        Utils.clear()
        
        fields_of_channel = self.view_channel_fields()
        Utils.printFormatedTable(["Nº", "NAME", "ID", "Created Date", "Description"],
                                [[f" Channel {index} ", channel_dict['name'],
                                channel_dict['id'], Utils.format_date(channel_dict['created_at']), channel_dict['description']]])
        
        if fields_of_channel is not None:
            field_index_list, field_index_names = fields_of_channel
            Utils.printFormatedTable(field_index_list, [field_index_names])
        # else:
        #     return 'b'

        str_channel_banner = "OPCIONES DEL CANAL\n" \
                            "------------------\n\n" \
                            "1 -- Channel settings\n\n" \
                            "2 -- Channel fields\n\n" \
                            "3 -- Delete the channel.\n\n" \
                            "4 -- Create fields for uploading data.\n\n" \
                            "5 -- Delete fields from channel.\n\n" \
                            "6 -- Upload data.\n\n" \
                            "7 -- Read field data.\n\n" \
                            "Enter \"back\" to go backwards"

        option = Utils.endless_terminal(str_channel_banner, "1", "2", "3", "4", "5", "6", "7")

        if option.__eq__('b'):
            return 'b'

        if option.__eq__("1"):

            self.update_channels_information()
            # while not modify_state:
            #     print("Has introducido mal algun campo")
            #     Utils.wait(2)
            #     modify_state = self.update_channels_information()

        elif option.__eq__("2"):
            # bar = IncrementalBar('Uploading data', max=100)
            # for i in range(1,100):
            #     time.sleep(0.2)
            #     bar.next()
            # bar.finish()

            # total_iterations = 100

            # # Crea una barra de progreso
            # progress_bar = tqdm(total=total_iterations)

            # # Itera a través de las tareas
            # for i in range(total_iterations):
            #     # Simula una tarea que toma un tiempo
            #     time.sleep(0.5)  # Espera medio segundo

            #     # Actualiza la barra de progreso
            #     progress_bar.update(1)

            # # Cierra la barra de progreso
            # progress_bar.close()
            self.print_channel_fields()

        elif option.__eq__("3"):

            i = Utils.endless_terminal("Are you sure you want to delete the channel? [y/n] ", tty=False)
            if i == "y":
                req = ThingSpeak.remove_channel(self.id, self.user_api_key)
                if req.status_code == 200:
                    print("Channel successfully deleted!")
                    Utils.wait(2)
                    return 'delete'

        elif option.__eq__("4"):

            self.create_fields_in_channel()

        elif option.__eq__("5"):

            self.remove_fields_from_channel()

        elif option.__eq__("6"):

            self.subir_datos()

        elif option.__eq__("7"):

            self.read_data("1")
            self.read_data("2")

        # if self.print_channel(self.index, self.channel_dict) is None:
        #     return

    # Method to update channel fields
    def update_channels_information(self):
        Utils.clear()

        valid_fields_to_modify = [
            "latitude",
            "description",
            "longitude",
            "elevation",
            "metadata",
            "name",
            "public_flag",
            "tags",
            "url",
            "field1",
            "field2",
            "field3",
            "field4",
            "field5",
            "field6",
            "field7",
            "field8"
        ]

        data = {
            "name": self.channel_dict['name'],
            "description": self.channel_dict['description'],
        }

        data['metadata'] =  self.channel_dict['metadata']

        tags = ', '.join(self.channel_dict['tags'])
        data['tags'] = tags

        url = self.channel_dict['url']
        if url:
            data['url'] = url
        else:
            data['url'] = ""
        
        url_github = self.channel_dict['github_url']
        if url_github:
            data['url_github'] = url_github
        else:
            data['url_github'] = ""
        
        data['elevation'] = self.channel_dict['elevation']
        data['latitude'] = self.channel_dict['latitude']
        data['longitude'] = self.channel_dict['longitude']
        data['public_flag'] = self.channel_dict['public_flag']    

        # Crear una lista de pares (clave, valor) para tabular
        table_data = [(key, value) for key, value in data.items()]

        # Utilizar tabulate para mostrar la información en una tabla
        table = tabulate(table_data, tablefmt="rounded_grid")

        print(table)

        updated_information = {"api_key": self.user_api_key}
        str_modify_message = "\nExample\n" \
                            "ts> name:NEW CHANNEL NAME,description:This is the new description"

        i = Utils.endless_terminal(str_modify_message, exit=True)

        if i.__eq__("b"):
            return

        entries = i.split(",")

        for entry in entries:
            key, value = entry.split(":", 1)
            key = key.strip()  # Asegúrate de que no haya espacios en blanco
            value = value.strip()  # Asegúrate de que no haya espacios en blanco

            if key in valid_fields_to_modify:
                updated_information[key] = value
            else:
                return False

        req = ThingSpeak.update_channel_information(self.id, updated_information)

        if req.status_code == 200:
            self.channel_dict = ThingSpeak.get_channel_settings(self.id, self.user_api_key).json()
            print("Canal actualizado")
            Utils.wait(2)
    
    def print_channel_fields(self):
        Utils.clear()
        data = {}
        fields = self.view_channel_fields()

        if fields:
            fields_index, fields_name = fields
            for f, n in zip(fields_index, fields_name):
                data[f] = n
        table_data = [(key, value) for key, value in data.items()]
        table = tabulate(table_data, tablefmt="rounded_grid")

        option = Utils.endless_terminal(table, *fields_index)

        if option == 'b':
            return

        index = re.findall("\d", option)[0]
        self.read_data(index)

    # Method to view the fields of the channel
    def view_channel_fields(self):
        req = ThingSpeak.get_channel_fields(self.id, self.channel_dict['api_keys'][1]['api_key'])

        if req.status_code == 200:
            channel_data = req.json()

            fields_index = []
            fields_name = []
            for i in range(1, 9):
                field = "field" + str(i)

                if field in channel_data['channel']:
                    fields_index.append(field)
                    fields_name.append(channel_data['channel'][field])

            if len(fields_index) > 0 and len(fields_name) > 0:
                return fields_index, fields_name
            else:
                return None

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

    def subir_datos(self):
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
                "field1": cpu
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

    # Method to read data from a especific field
    def read_data(self, field_id):
        url_read_data_field = f"https://api.thingspeak.com/channels/{self.id}/fields/{field_id}.json?results=100&api_key={self.channel_dict['api_keys'][1]['api_key']}"
        req = Utils.make_request(method="GET", url=url_read_data_field)

        if req.status_code == 200:
            field_values = req.json()['feeds']
            
            field_entries = []
            cont = 1
            for entri in field_values:
                e = []
                e.append(cont)
                datetime = Utils.format_date(entri['created_at'])
                date, time = datetime.split(" ")
                e.append(date)
                e.append(time)
                e.append(entri[f'field{field_id}'])
                field_entries.append(e)
                cont += 1

            table = tabulate(field_entries, tablefmt="rounded_grid")

            Utils.endless_terminal(table, "1", clear="yes")
