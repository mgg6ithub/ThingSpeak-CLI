class Channel:
    def __init__(self, u, index, channel_dict):
        self.u = u
        self.id = channel_dict['id']
        self.name = channel_dict['name']
        self.print_channel(index, channel_dict)
        self.channel_menu()

    def __str__(self):
        return

    # Method to print channels
    def print_channel(self, index, channel_dict):
        self.u.clear()
        self.u.printFormatedTable(["Nº", "NAME", "ID", "Created Date", "Description"], [[f" Channel {index} ", channel_dict['name'],
                                                                                        channel_dict['id'], channel_dict['created_at'], channel_dict['description']]])
        self.u.printFormatedTable(["LATITUDE", "LONGITUDE", "ELEVATION", "LAST ENTRY"], [[channel_dict['latitude'], channel_dict['longitude'],
                                                                                          channel_dict['elevation'], channel_dict['last_entry_id']]])
        self.u.printFormatedTable(["WRITE API KEY", "READ API KEY"], [[channel_dict['api_keys'][0]['api_key'], channel_dict['api_keys'][1]['api_key']]])

    # Channel options
    def channel_menu(self):
        str_channel_banner = "OPCIONES DEL CANAL\n" \
                             "------------------\n\n" \
                             "1 -- Modificar canal\n\n" \
                             "2 -- Modificar canal\n\n\n" \
                             "Enter \"back\" to go backwards"

        option = self.u.endless_terminal(str_channel_banner, "1", "2", c="c")

        if option.__eq__("back"):
            return
        elif option.__eq__("1"):
            print("HAS PRESIONADO LA OPCION 1 DEL CANAL")
        elif option.__eq__("2"):
            print("HAS PRESIONADO LA OPCION 2 DEL CANAL")
        i = input()
