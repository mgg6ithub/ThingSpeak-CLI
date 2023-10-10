class ThingSpeak:

    def __init__(self, user_apy_key, u):
        self.user_apy_key = user_apy_key
        self.u = u

        account_channels_info = self.get_channel_info()

        if account_channels_info and account_channels_info[0]:
            all_channels, len_public_channels, public_channels, len_private_channels, private_channels = account_channels_info

            self.len_all_channels = len_public_channels + len_private_channels
            self.all_channels = all_channels
            self.len_public_channels = len_public_channels
            self.public_channels = public_channels
            self.len_private_channels = len_private_channels
            self.private_channels = private_channels
        else:
            print("No tienes canales ¿Deseas crear un canal?")

    def __str__(self):
        return str(self.all_channels)

    # Method to obtain all the channels from the logged account
    def get_channel_info(self):
        req = self.get_channels_list()

        if req.status_code == 200 and req.json() is not None:
            public_channels = []
            private_channels = []

            for c in req.json():
                if c['public_flag']:
                    public_channels.append(c)
                else:
                    private_channels.append(c)
            return req.json(), len(public_channels), public_channels, len(private_channels), private_channels
        else:
            return None

    # Method to print all the public channels
    def print_public_channels(self):
        for c in self.public_channels:
            self.u.printFormatedTable(["Id", "Name", "Description", "Latitude", "Longitude",
                                       "Created at", "Elevation"], [[c['id'], c['name'],
                                                                     c['description'], c['latitude'], c['longitude'],
                                                                     c['elevation'], c['created_at']]])

    # Method to print all the private channels
    # En el bucle c imprime rl diccionario del canal asi:
    # {'id': 2299146, 'name': 'Canal1', 'description': 'Esta es la descripcion del canal 1',
    # 'latitude': '0.0', 'longitude': '0.0', 'created_at': '2023-10-10T19:58:50Z', 'elevation': '',
    # 'last_entry_id': None, 'public_flag': False, 'url': None, 'ranking': 50, 'metadata': '',
    # 'license_id': 0, 'github_url': None, 'tags': [],
    # 'api_keys': [{'api_key': 'ZCRD02RYHN5Y8CXT', 'write_flag': True}, {'api_key': '97NQ78KHK1PK7RP7', 'write_flag': False}]}
    def print_private_channels(self):
        for c in self.private_channels:
            self.u.printFormatedTable(["Id", "Name", "Description", "Latitude", "Longitude",
                                       "Created at", "Elevation"], [[c['id'], c['name'],
                                                                     c['description'], c['latitude'], c['longitude'],
                                                                     c['elevation'], c['created_at']]])

    def print_all_channels(self):
        for c in self.all_channels:
            self.u.printFormatedTable(["Id", "Name", "Description", "Latitude", "Longitude",
                                       "Created at", "Elevation"], [[c['id'], c['name'],
                                                                     c['description'], c['latitude'], c['longitude'],
                                                                     c['elevation'], c['created_at']]])

    # Method to know how many private and public channels there are
    def get_channels_length(self):
        return len(self.get_channels_list().json())

    # Method to get the list of all existing channels
    def get_channels_list(self):
        req = self.u.make_request(method="GET",
                                  url=f"https://api.thingspeak.com/channels.json?api_key={self.user_apy_key}")
        return req

    # Method to know how many public channels are there
    def get_public_channels_length(self):
        return len(self.get_public_channels().json())

    # Method to get the list of all public channels
    def get_public_channels(self):
        req = self.u.make_request(method="GET",
                                  url="https://api.thingspeak.com/users/mwa0000031155118/channels.json")
        return req

    # Method to obtain all private channels
    def get_private_channels(self):
        pass

    # Metodo para obtener los objetos json de los canales a partir de la lista
    def get_channels_json(self, list):
        pass

    # Metodo que obtiene los datos de un canal pasandole su id
    def get_channel_settings(self, id):
        req = self.u.make_request(method="GET",
                                  url=f"https://api.thingspeak.com/channels/{id}.json?api_key={self.user_apy_key}")

        return req
