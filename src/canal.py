from src.utils import Utils

import time
from src.thingspeak import ThingSpeak
from tabulate import tabulate
import pdb
import re

# {'channel': {'id': 2338528, 'name': 'aethelflaed', 'description': 'Esta es la descripcion del canal 1', 'latitude': 
#              '0.0', 'longitude': '0.0', 'field1': 'CPU & RAM', 'field2': 'Temperature sensor 1', 
#              'created_at': '2023-11-08T22:47:43Z', 'updated_at': '2023-11-09T08:32:15Z', 'last_entry_id': 14}, 

class Channel:
    def __init__(self, user_api_key, index, channel_dict, channel_name):
        self.user_api_key = user_api_key
        self.channel_name = channel_name
        self.index = index
        self.channel_dict = channel_dict
        self.id = channel_dict['id']
        self.write_api_key = channel_dict['api_keys'][0]['api_key']
        self.read_api_key = channel_dict['api_keys'][1]['api_key']


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

    # Method to create the channel resume table
    def create_channel_resume_table(self):
        return Utils.printFormatedTable(["Nº", "NAME", "ID", "Created Date", "Description"],
                                [[f" Channel {self.index} ", self.channel_dict['name'],
                                self.channel_dict['id'], Utils.format_date(self.channel_dict['created_at']), self.channel_dict['description']]])


    # Method to update channel fields
    def update_channels_information(self):
        Utils.clear()
        # print(self.channel_dict)
        # input()
        
        # VALORES QUE NO SE PUEDEN CAMBIAR
        # channel id
        # create_at
        # Last entry
        # rankig (Porcentaje completado del canal)
        # license_id

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
        ]

        data = {
            "name": self.channel_dict['name'],
            "description": self.channel_dict['description'],
            "metadata": self.channel_dict['metadata'],
            "tags": ' '.join(tag['name'] for tag in self.channel_dict['tags'])
        }

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
                            "ts> name:NEW CHANNEL NAME,tags:tag1,tag2,tag3,description:This is the new description"
        # str_help_channel_info = "more info\tKeys of the channel.\n" \
        #                         "rename fields\tUpdate a the channel information. Name, tags, etc..."
        
        # options_dict = {
        #     "more info":
        # }

        i = Utils.endless_terminal(str_modify_message, exit=True)

        if i.__eq__("b"):
            return

        tags_list = []
        tags_end_valid_word = ''
        input_string_tags_removed = ''
        #COMPROBAR SI HAY TAGS PARA FORMATEAR LA CADENA Y OBTENER TODAS
        if 'tags' in i:
            tags_string = i.split('tags:')[1].split(',')

            for tag in tags_string:
                if ':' in tag:
                    tags_end_valid_word = tag.split(':')[0]
                    break
                tags_list.append(tag)
            #COMPROBAR SI HAY MAS COSAS DELANTE DE TAGS Y DETRAS
            first_part = ''
            second_part = ''
            first_part = i.split('tags:')[0]
            input(first_part)
            if first_part == '': # No hay anda delante de tags
                print('No hay nada delante')
            if tags_end_valid_word: # Si hay un valid word despues de las tags es que hay mas valores
                second_part = i.split(tags_end_valid_word)[1]
            if second_part == '':
                input("No hay nada detras")
            input_string_tags_removed = first_part + tags_end_valid_word + second_part

            if input_string_tags_removed == '':
                input("No hay cadena resultante")
            input(tags_list)

            # SI SOLO HAY TAGS
            if input_string_tags_removed == '': # Solamente se ha introducido tags
                string_joined_tags = ','.join(tags_list)
                input(string_joined_tags)
                updated_information['tags'] = ','.join(tags_list)
            else: # hya mas cosas aparte de tags
                entries = input_string_tags_removed.split(",")

                for entry in entries:
                    key, value = entry.split(":", 1)
                    key = key.strip()  # Asegúrate de que no haya espacios en blanco
                    value = value.strip()  # Asegúrate de que no haya espacios en blanco

                    if key in valid_fields_to_modify:
                        updated_information[key] = value
                    else:
                        return False
                if tags_list:
                    updated_information['tags'] = ','.join(tags_list)
        # SI NO HAY TAGS SE PROCEDE NORMAL
        else:
            entries = i.split(",")
            for entry in entries:
                key, value = entry.split(":", 1)
                key = key.strip()  # Asegúrate de que no haya espacios en blanco
                value = value.strip()  # Asegúrate de que no haya espacios en blanco

                if key in valid_fields_to_modify:
                    updated_information[key] = value
                else:
                    return False

        input(updated_information)
        req = ThingSpeak.update_channel_information(self.id, updated_information)

        if req.status_code == 200:
            self.channel_dict = ThingSpeak.get_channel_settings(self.id, self.user_api_key).json()
            print("Canal actualizado")
            Utils.wait(2)
    
    # Method to get the fields of the channel
    def get_channel_fields(self):
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
                self.channel_fields_names = fields_name
                return fields_index, fields_name
            else:
                return None


    # Method to print the fields of a channel
    def print_channel_fields(self):
        Utils.clear()

        fields = self.get_channel_fields()
        if fields:
            fields_index, fields_names = fields

            all_fields = []
            cont = 1
            for f in range(len(fields_index)):
                temp = []
                temp.append(str(cont))
                temp.append(fields_index[f])
                temp.append(fields_names[f])

                all_fields.append(temp)
                cont += 1

            # Just getting the index of each field
            self.valid_field_indexes = [all_fields[i][0] for i in range(len(all_fields))]
        else:
            if input("You have no fields. Do you want to create one? [y/n] ") == 'y':
                self.create_one_field()
                return 'refresh'
            else:
                return 'b'

        self.table_of_fields = tabulate(all_fields, tablefmt="rounded_grid")
    
    # Method to get the name of a field giving the correpondant index
    def get_field_name(self, index):

        if index is not 0:
            index -= 1

        for i in range(0, len(self.channel_fields_names)):
            if i == index:
                return self.channel_fields_names[i]

    #Method to select a field from the channel and create a new Field instance with it.
    def select_field(self):
        return Utils.endless_terminal(self.table_of_fields + "\n\nSelect a field by its index.\n", *self.valid_field_indexes)

    # Method to create fields
    def create_one_field(self):
        Utils.clear()
        new_field_dict = {"api_key": self.user_api_key}
        field_name = input("Enter the new field name: ")
        fields = self.get_channel_fields()

        if fields is None:
            new_field_dict['field1'] = field_name
        else:
            field_indexes, _ = fields

            if len(field_indexes) == 8:
                Utils.endless_terminal("You have all fields occupied.\nGo back to the channel main menu and delete one.")
                return

            cont = 1
            while cont <= len(field_indexes):
                cont += 1

            available_field = "field" + str(cont)
            new_field_dict[available_field] = field_name

        req = ThingSpeak.create_one_field_for_channel(new_field_dict, self.id)

        if req.status_code == 200:
            print(f"New field {field_name} created.")
            time.sleep(2)

    
    # Method to clear all the data from a field
    def clear_data_from_all_fields(self):
        Utils.clear()
        if input("Are you sure you want to delete the data from all fields? [y/n]") == 'y':
            res = ThingSpeak.clear_data_from_all_fields(self.id, self.user_api_key)
            if res.status_code == 200:
                print("All the data from fields deleted.")
                time.sleep(2)
            else:
                print(res.status_code)
                input()


    # Method to rename a field
    def rename_field_name(self):
        selected_index = Utils.endless_terminal(self.table_of_fields + "\n\nSelect the index of the field you want to delete.", *self.valid_field_indexes)
        new_name = str(input("Enter the new name: "))
        remove_field = {"api_key": self.user_api_key}

        for i in self.valid_field_indexes:
            if i == selected_index:
                remove_field['field' + i] = new_name
        
        req = ThingSpeak.create_one_field_for_channel(remove_field, self.id)
        
        if req.status_code == 200:
            print(f"Field renamed.")
            time.sleep(2)


    def delete_one_field():
        pass


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


    # Method to remove all the fields from a channel
    def delete_all_fields(self):

        fichero_json = {"api_key": self.user_api_key}

        for ite in range(1, 9):
            fichero_json[f"field{ite}"] = ""
        r = Utils.make_request(method="put", url=f"https://api.thingspeak.com/channels/{self.id}.json",
                            json=fichero_json)
        print(r.status_code)
        if r.status_code == 200:
            print("Fields have been deleted")
            time.sleep(2)


    # Method to delet the channel
    def delete_channel(self):
        i = Utils.endless_terminal("Are you sure you want to delete the channel? [y/n] ", tty=True)
        if i == "y":
            req = ThingSpeak.remove_channel(self.id, self.user_api_key)
            if req.status_code == 200:
                print("Channel successfully deleted!")
                Utils.wait(2)


    # Method to print commands help
    # @staticmethod
    # def print_help():
    #     str_field_list_commands_help = "create field\tTo create a new field. Up to 8 fields in total.\n" \
    #                                             "clear fields\tClear all the data from all the fields.\n" \
    #                                             "delete field\tDelete a existing field.\n" \
    #                                             "delete all fields\tDelete all existing field and their data.\n"
    #     return str_field_list_commands_help