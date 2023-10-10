class ThingSpeak:

    def __init__(self, user_apy_key, u):
        self.user_apy_key = user_apy_key
        self.u = u

    def __str__(self):
        print(f"Tu apy key es: {self.user_apy_key}")

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
