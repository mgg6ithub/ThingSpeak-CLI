from src.utils import Utils

class ThingSpeak:
    def __init__(self, user_apy_key):
        self.user_apy_key = user_apy_key
        self.hayCanales = False
        self.get_account_info()

    # def __str__(self):
    #     return str(self.all_channels)

    # Method to print the overall information of a channel
    # Name  Id
    def print_channel_index(self, channels):
        Utils.clear()
        indexes = {}
        cont = 1
        print("Nº\t\t\tID\t\t\tNOMBRE CANAL")
        print("- \t\t\t--\t\t\t------------")
        for c in channels:
            print(str(cont) + "\t\t\t" + str(c['id']) + "\t\t\t" + c['name'] + "\n")
            indexes[str(cont)] = c
            cont += 1
        return indexes

    # Method to obtain all the channels from the logged account
    # {'id': 2299146, 'name': 'Canal1', 'description': 'Esta es la descripcion del canal 1',
    # 'latitude': '0.0', 'longitude': '0.0', 'created_at': '2023-10-10T19:58:50Z', 'elevation': '',
    # 'last_entry_id': None, 'public_flag': False, 'url': None, 'ranking': 50, 'metadata': '',
    # 'license_id': 0, 'github_url': None, 'tags': [], 'api_keys': [{'api_key': 'ZCRD02RYHN5Y8CXT',
    # 'write_flag': True}, {'api_key': '97NQ78KHK1PK7RP7', 'write_flag': False}]}
    def get_account_info(self):
        req = self.get_channels_list()

        channels = req.json()
        channel_number = len(req.json())

        if req.status_code == 200 and channel_number is not 0:
            self.hayCanales = True

            public_channels = []
            private_channels = []

            for c in req.json():
                if c['public_flag']:
                    public_channels.append(c)
                else:
                    private_channels.append(c)

            self.len_all_channels = channel_number
            self.all_channels = channels
            self.len_public_channels = len(public_channels)
            self.public_channels = public_channels
            self.len_private_channels = len(private_channels)
            self.private_channels = private_channels
        else:
            self.hayCanales = False

    # Method to know how many private and public channels there are
    def get_channels_length(self):
        return len(self.get_channels_list().json())

    # Method to get the list of all existing channels
    def get_channels_list(self):
        req = Utils.make_request(method="GET",
                                url=f"https://api.thingspeak.com/channels.json?api_key={self.user_apy_key}")
        return req

    # Method to know how many public channels are there
    def get_public_channels_length(self):
        return len(self.get_public_channels().json())

    # Method to get the list of all public channels
    def get_public_channels(self):
        req = Utils.make_request(method="GET",
                                url="https://api.thingspeak.com/users/mwa0000031155118/channels.json")
        return req

    # Method to obtain all private channels
    def get_private_channels(self):
        pass

    # Metodo para obtener los objetos json de los canales a partir de la lista
    def get_channels_json(self, list):
        pass

    @staticmethod
    # Method to retrieve the settings of a channel giving the id
    def get_channel_settings(id, user_api_key):
        req = Utils.make_request(method="GET",
                                url=f"https://api.thingspeak.com/channels/{id}.json?api_key={user_api_key}")
        return req

    # Method to remove a channel
    @staticmethod
    def remove_channel(id, user_api_key):
        body = {"api_key": user_api_key}
        req = Utils.make_request(method="DELETE", url=f"https://api.thingspeak.com/channels/{id}.json", json=body)
        return req

    # Method to create a channel
    @staticmethod
    def create_channel(user_api_key):
        nombre = input("Enter the new channel name: ")
        body = {"api_key": user_api_key, 'id': 2299146, 'name': f'{nombre}',
                'description': 'Esta es la descripcion del canal 1',
                'latitude': '0.0', 'longitude': '0.0', 'created_at': '2023-10-10T19:58:50Z', 'elevation': '',
                'last_entry_id': None, 'public_flag': False, 'url': None, 'ranking': 50, 'metadata': '',
                'license_id': 0, 'github_url': None, 'tags': [], 'api_keys': [{'api_key': 'ZCRD02RYHN5Y8CXT',
                                                                            'write_flag': True},
                                                                            {'api_key': '97NQ78KHK1PK7RP7',
                                                                            'write_flag': False}]}

        r = Utils.make_request(method="POST", url="https://api.thingspeak.com/channels.json", json=body)

        print(r.status_code)
        print(r.json())

        i = input()

    # Method to update information of the channel
    @staticmethod
    def update_channel_information(channel_id, updated_information):
        update_channel_information_url = f"https://api.thingspeak.com/channels/{channel_id}.json"
        return Utils.make_request(method="PUT", url=update_channel_information_url, json=updated_information)

    # Method to retrieve a channel fields
    @staticmethod
    def get_channel_fields(channel_id, api_key):
        return Utils.make_request(method="GET",
                                url=f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={api_key}")
