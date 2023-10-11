class Channel:
    def __init__(self, u, index, channel_dict):
        self.u = u
        self.id = channel_dict["1"]
        self.name = channel_dict["2"]
        self.print_channel(index, channel_dict)

    def __str__(self):
        return

    # Method to print channels
    def print_channel(self, index, channel_dict):
            self.u.printFormatedTable([" Nº ", "Id", "Name", "Description", "Latitude", "Longitude",
                                       "Created at", "Elevation"], [[f" CANAL {index} ", channel_dict['id'], channel_dict['name'],
                                                                     channel_dict['description'], channel_dict['latitude'], channel_dict['longitude'],
                                                                     channel_dict['elevation'], channel_dict['created_at']]])
            print("\n\nOPTIONS")