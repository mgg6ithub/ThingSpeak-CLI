from src.utils import Utils

import time
from src.thingspeak import ThingSpeak
from tabulate import tabulate
import pdb
import re


class Channel:
    def __init__(self, user_api_key, index, channel_dict, channel_name):
        self.user_api_key = user_api_key
        self.channel_name = channel_name
        self.index = index
        self.channel_dict = channel_dict
        self.id = channel_dict['id']
        self.write_api_key = channel_dict['api_keys'][0]['api_key']
        self.read_api_key = channel_dict['api_keys'][1]['api_key']
        self.valid_channel_information_fields =  [
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


    # Method to return the flow control to the main channel menu
    def doNothing(self):
        pass

    # Method to create the channel resume table
    def create_channel_resume_table(self):
        return Utils.printFormatedTable(["Nº", "NAME", "ID", "Created Date", "Description"],
                                [[f" Channel {self.index} ", self.channel_dict['name'],
                                self.channel_dict['id'], Utils.format_date(self.channel_dict['created_at']), self.channel_dict['description']]])


    def check_urls(self, data, url_type):

        url = self.channel_dict[f'{url_type}']
        
        if url:
            data[f'{url_type}'] = url
        else:
            data[f'{url_type}'] = ''
    

    def generate_channel_information_table(self):
        Utils.clear()
        
        # VALORES QUE NO SE PUEDEN CAMBIAR
        # channel id
        # create_at
        # Last entry
        # rankig (Porcentaje completado del canal)
        # license_id
        self.channel_name = self.channel_dict['name']
        data = {
            "name": self.channel_dict['name'],
            "description": self.channel_dict['description'],
            "metadata": self.channel_dict['metadata'],
            "tags": ' '.join(tag['name'] for tag in self.channel_dict['tags']) # Iterate over the tags for printing them
        }

        self.check_urls(data, "url")
        self.check_urls(data, "github_url")
        
        data['elevation'] = self.channel_dict['elevation']
        data['latitude'] = self.channel_dict['latitude']
        data['longitude'] = self.channel_dict['longitude']
        data['public_flag'] = self.channel_dict['public_flag']    

        # Crear una lista de pares (clave, valor) para tabular
        table_data = [(key, value) for key, value in data.items()]

        # Utilizar tabulate para mostrar la información en una tabla
        return tabulate(table_data, tablefmt="rounded_grid")
        

    def display_more_channel_info(self):
        table = Utils.printFormatedTable(["PERCENTAGE COMPLETED","CREATED DATE", "WRITE API KEY", "READ API KEY", "LAST ENTRY"],
                                [["%" + str(self.channel_dict['ranking']), self.channel_dict['created_at'],self.write_api_key, self.read_api_key, self.channel_dict['last_entry_id']]])
        return table

    # Method to update channel fields
    def update_channels_information(self):

        message = 'Channel information updated'
        str_modify_message = "\nExample\n" \
                            "ts> name:NEW CHANNEL NAME,tags:tag1,tag2,tag3,description:This is the new description"

        i = Utils.endless_terminal(message=str_modify_message, menu=self.channel_name, only_string=True)

        # CHECK INPUT VALUES
        input_values = i.split(',')
        flag = True
        for value in input_values:
            if ':' in value:
                v = value.split(':')[0]
                # input(v)
                if v not in self.valid_channel_information_fields:
                    flag = False

        if flag:
            tags_list = []
            tags_end_valid_word = ''
            input_string_tags_removed = ''
            updated_information = {"api_key": self.user_api_key}
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

                if tags_end_valid_word: # Si hay un valid word despues de las tags es que hay mas valores
                    second_part = i.split(tags_end_valid_word)[1]

                input_string_tags_removed = first_part + tags_end_valid_word + second_part

                # SI SOLO HAY TAGS
                if input_string_tags_removed == '': # Solamente se ha introducido tags
                    updated_information['tags'] = ','.join(tags_list)
                else: # hay mas cosas aparte de tags
                    if second_part == '':
                        input_string_tags_removed = input_string_tags_removed.rstrip(',')

                    entries = input_string_tags_removed.split(",")
                    for entry in entries:
                        key, value = entry.split(":", 1)
                        key = key.strip()  # Asegúrate de que no haya espacios en blanco
                        value = value.strip()  # Asegúrate de que no haya espacios en blanco

                        if key in self.valid_channel_information_fields:
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

                    if key in self.valid_channel_information_fields:
                        updated_information[key] = value
                    else:
                        return False

            req = ThingSpeak.update_channel_information(self.id, updated_information)
            if req.status_code == 200:
                self.channel_dict = ThingSpeak.get_channel_settings(self.id, self.user_api_key).json()
                Utils.give_response(message=message, status=True)
                return ''
            else:
                Utils.give_response(message=message, status=False)
        else:
            Utils.give_response(message=message + '. You entered some name value wrong.', status=False)
            return ''


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
    

    # Method to clear all the data from all channel fields
    def clear_data_from_all_fields(self):
        message = 'Channel data deleted'
        Utils.clear()
        i = Utils.endless_terminal("Are you sure you want to delete the data from all fields? [y/n] ", tty=False)
        if i == 'y':
            res = ThingSpeak.clear_data_from_all_fields(self.id, self.user_api_key)
            if res.status_code == 200:
                Utils.give_response(message=message, clear=True, status=True)
                return 'reset'
            else:
                Utils.give_response(message=message, clear=True, status=False)
        else:
            return 'n'

    # Method to delet the channel
    def delete_channel(self):
        message = f'Channel {self.channel_name} deleted'
        i = Utils.endless_terminal("Are you sure you want to delete the channel? [y/n] ",clear=True, tty=False)
        if i == "y":
            req = ThingSpeak.remove_channel(self.id, self.user_api_key)
            if req.status_code == 200:
                Utils.give_response(message=message, clear=True, status=True)
                return 'reset'
            else:
                Utils.give_response(message=message, clear=True, status=False)