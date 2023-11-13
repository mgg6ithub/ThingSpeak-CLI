from src.utils import Utils
from src.thingspeak import ThingSpeak

import time
import psutil
from tabulate import tabulate
from progress.bar import IncrementalBar
from tqdm import tqdm
import keyboard

# 'feeds': [{'created_at': '2023-11-08T22:48:56Z', 'entry_id': 1, 'field1': '0.1', 'field2': None}, 
#            {'created_at': '2023-11-08T22:49:12Z', 'entry_id': 2, 'field1': '0.4', 'field2': None}, 
#            {'created_at': '2023-11-08T22:49:27Z', 'entry_id': 3, 'field1': '0.4', 'field2': None}, 
#            {'created_at': '2023-11-08T22:49:43Z', 'entry_id': 4, 'field1': '0.3', 'field2': None}, 
#            {'created_at': '2023-11-08T22:49:59Z', 'entry_id': 5, 'field1': '0.2', 'field2': None}, 
#            {'created_at': '2023-11-08T22:50:14Z', 'entry_id': 6, 'field1': '0.2', 'field2': None}, 
#            {'created_at': '2023-11-08T22:50:30Z', 'entry_id': 7, 'field1': '0.2', 'field2': None}, 
#            {'created_at': '2023-11-09T16:13:33Z', 'entry_id': 8, 'field1': None, 'field2': '0.1'}, 
#            {'created_at': '2023-11-09T16:13:49Z', 'entry_id': 9, 'field1': None, 'field2': '0.3'}, 
#            {'created_at': '2023-11-09T16:14:04Z', 'entry_id': 10, 'field1': None, 'field2': '0.2'}, 
#            {'created_at': '2023-11-09T16:14:20Z', 'entry_id': 11, 'field1': None, 'field2': '0.3'}, 
#            {'created_at': '2023-11-09T16:14:35Z', 'entry_id': 12, 'field1': None, 'field2': '0.4'}, 
#            {'created_at': '2023-11-09T16:14:51Z', 'entry_id': 13, 'field1': None, 'field2': '0.2'}, 
#            {'created_at': '2023-11-09T16:15:06Z', 'entry_id': 14, 'field1': None, 'field2': '0.2'}]}

class Field:

    def __init__(self, field_index, channel_id, write_key, read_key):
        self.field_index = field_index
        self.channel_id = channel_id
        self.write_key = write_key
        self.read_key = read_key


    def update_date(self, index, name, data):
        self.index = index

    
    # Method to get the feeds from a field
    def get_data_from_field(self):
        res = ThingSpeak.get_feeds_from_field(self.channel_id, self.field_index, self.read_key)
        if res.status_code == 200:
            return res.json()['feeds']

    # Method to read data from a especific field
    def read_data_from_field(self):
        
        field_values = self.get_data_from_field()

        field_entries = []
        cont = 1
        for entri in field_values:
            value = entri[f'field{self.field_index}']
            if value is not None:
                e = []
                e.append(cont)
                datetime = Utils.format_date(entri['created_at'])
                date, time = datetime.split(" ")
                e.append(date)
                e.append(time)
                e.append(value)
                field_entries.append(e)
                cont += 1

        return tabulate(field_entries, tablefmt="rounded_grid")


    def subir_datos(self):
        i = 0
        # print("Press q to stop de upload.")
        while i < 200:
            # if keyboard.is_pressed('q'):
            #     break
            cpu = psutil.cpu_percent()  # USO DE LA CPU
            vm = psutil.virtual_memory()
            ram = vm.percent  # USO DE LA RAM

            self.mostrar_recursos_hardware(cpu, ram, size=30)
            i += 1
            time.sleep(0.5)
            Utils.make_request(method="post", url="https://api.thingspeak.com/update.json", json={
                "api_key": self.write_key,
                "field" + self.field_index: cpu
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


    # Method to download the data of a given field
    # download filw formats
    #   .xlsx
    #   .cvs
    #   .txt
    def download_data(self):
        file_name = str(input("Enter the file name: "))

        format_options = {
            "xlsx": Utils.create_xlsx,
            "csv": Utils.create_csv,
            "txt": Utils.create_txt
        }

        str_banner_choose_format = "Choose file format for downloading the data.\n\n" \
                                    "1 -- xlsx\n" \
                                    "2 -- csv\n" \
                                    "3 -- txt\n"
        selected_option = Utils.endless_terminal(str_banner_choose_format, *list(format_options.keys()))

        format_options[selected_option](file_name, self.get_data_from_field(), self.field_index)


    # Method to clear all the data of the field
    def clear_field_data():
        pass


    # Method to delete the current field
    def delete_field():
        pass