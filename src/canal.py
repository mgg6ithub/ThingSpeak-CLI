from src.thingspeak import ThingSpeak

import time


class Channel:
    def __init__(self, user_api_key, u, index, channel_dict):
        self.user_api_key = user_api_key
        self.u = u
        self.index = index
        self.channel_dict = channel_dict
        self.id = channel_dict['id']
        self.print_channel(index, channel_dict)

        # self.valid_fields = [
        #     "description",
        #     "field1",
        #     "latitude",
        #     "longitude",
        #     "elevation",
        #     "metadata",
        #     "name",
        #     "public_flag",
        #     "tags",
        #     "url"
        # ]

    def __str__(self):
        return

    # Method to print channels
    def print_channel(self, index, channel_dict):
        self.u.clear()
        self.u.printFormatedTable(["Nº", "NAME", "ID", "Created Date", "Description"],
                                  [[f" Channel {index} ", channel_dict['name'],
                                    channel_dict['id'], channel_dict['created_at'], channel_dict['description']]])
        self.u.printFormatedTable(["LATITUDE", "LONGITUDE", "ELEVATION", "LAST ENTRY"],
                                  [[channel_dict['latitude'], channel_dict['longitude'],
                                    channel_dict['elevation'], channel_dict['last_entry_id']]])
        self.u.printFormatedTable(["WRITE API KEY", "READ API KEY"],
                                  [[channel_dict['api_keys'][0]['api_key'], channel_dict['api_keys'][1]['api_key']]])
        self.channel_menu()

    # Channel options
    def channel_menu(self):
        str_channel_banner = "OPCIONES DEL CANAL\n" \
                             "------------------\n\n" \
                             "1 -- Modificar canal\n\n" \
                             "2 -- Modificar canal\n\n" \
                             "3 -- Delete the channel.\n\n" \
                             "Enter \"back\" to go backwards"

        option = self.u.endless_terminal(str_channel_banner, "1", "2", "3", c="c")

        if option.__eq__("back"):
            return
        elif option.__eq__("1"):
            self.update_channels_fields()
        elif option.__eq__("2"):
            print("HAS PRESIONADO LA OPCION 2 DEL CANAL")
        elif option.__eq__("3"):
            i = input("Are you sure you want to delete the channel? y/n")
            if i == "y":
                req = ThingSpeak.remove_channel(self.id, self.user_api_key)
                if req == 200:
                    print("Channel successfully deleted!")
        i = input()

    # Method to update channel fields
    def update_channels_fields(self):
        api_url = f"https://api.thingspeak.com/channels/{self.id}.json"
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

        body = {"api_key": self.user_api_key}
        print("Enter the field/s value you want to change(Enter \"ok\" to finish).")
        while True:
            i = self.u.endless_terminal("Type a field: ", *valid_fields, c="c")

            if i.__eq__("ok"):
                break

            new_value = input(f"Type a new value for {i}: ")
            body[i] = new_value

        i = self.u.make_request(method="PUT", url=api_url, json=body)

        if i.status_code == 200:
            # self.print_channel(self.index, )
            self.channel_dict = ThingSpeak.get_channel_settings(self.id, self.user_api_key).json()
            self.print_channel(self.index, self.channel_dict)



