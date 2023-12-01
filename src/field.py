from src.utils import Utils
from src.thingspeak import ThingSpeak

import time
import psutil
from tabulate import tabulate
from progress.bar import IncrementalBar
from tqdm import tqdm
import keyboard
import csv
import re

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

    def __init__(self, field_index, field_name, channel_id, write_key, read_key):
        self.field_index = field_index
        self.field_name = field_name
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

        self.field_data_table = tabulate(field_entries, tablefmt="rounded_grid")


    def subir_datos(self):
        i = 0
        # print("Press q to stop de upload.")
        while i < 500:
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

# # BUILT THE QUERY STRING
        # query_string = '&'.join([f'field{self.field_index}={value}' for value in data_values])
        # response = ThingSpeak.upload_data_from_csv_file(self.write_key, query_string)
        # write_api_key=KKRLJNAXF86OLCPI&time_format=absolute&updates=2023-11-11 17:42:11,0.3,,,,,,,,|
        # 2023-11-11 17:42:27,0.3,,,,,,,,|2023-11-11 17:42:42,0.3,,,,,,,,|
        # 2023-11-11 17:42:58,0.3,,,,,,,,|2023-11-11 17:43:13,0.4,,,,,,,,|
        # 2023-11-11 17:43:29,0.3,,,,,,,,|2023-11-11 17:43:45,0.4,,,,,,,,|
        # 2023-11-11 17:44:00,0.3,,,,,,,,|2023-11-11 17:44:15,0.4,,,,,,,,|
        # 2023-11-11 17:44:31,0.2,,,,,,,,

    # Method to upload a csv data
    def upload_csv(self):
        path_file = input('Enter the csv file path: ')

        # check the date defualt no dateformat absolute

        with open(path_file, 'r') as file:
            # csv_reader = csv.reader(file, delimiter='\t')
            # next(csv_reader)

            # updates = ''
            # for row in csv_reader:
            #     timestamp = f'{row[0]} {row[1]}'
            #     field2_value = row[2]
            #     updates += f'{timestamp},{field2_value},,,,,,,,|'
            
            striped_data = [word.strip().split('\t')[2] for word in file.readlines()]

            # Crear la cadena de actualización para ThingSpeak
            string_template = '0,,,,,,,,,,,,ok|'

            bulk_data = ""
            for index, row_data in enumerate(striped_data):
                lista = string_template.split(',')
                lista[0] = str(index)
                lista[int(self.field_index)] = row_data
                temp_template = ','.join(lista)

                bulk_data += temp_template

                if index == len(striped_data) - 1:
                    if bulk_data.endswith('|'):
                        bulk_data = bulk_data[:-1] # quitar el ultimo caracter que va a ser siempre un |
                        break

            # Datos para enviar en la solicitud POST
            data_to_send = {
                'write_api_key': self.write_key,
                'time_format': 'relative',
                'updates': bulk_data #.rstrip('|')  # Eliminar el último carácter '|' para evitar problemas
            }

            input(data_to_send)
            # Convertir datos a formato adecuado para el cuerpo de la solicitud
            # body_data = '&'.join([f'{key}={value}' for key, value in data_to_send.items()])
            ThingSpeak.upload_data_from_csv_file(self.channel_id, data_to_send)
            return 'actualizar'


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
        Utils.clear()
        file_name = str(input("Enter the file name: "))

        date_format = str(input('Select the date format: \n'\
            '1 -> 2018-06-14T12:12:22\n' \
            '2 -> 2018-06-14 12:12:22\n'
        ))

        format_options = {
            "1": Utils.create_xlsx,
            "2": Utils.create_csv,
            "3": Utils.create_txt
        }

        str_banner_choose_format = "Choose file format for downloading the data:\n\n" \
                    "1 -> xlsx\n" \
                    "2 -> csv\n" \
                    "3 -> txt\n"
        selected_option = Utils.endless_terminal(str_banner_choose_format, *list(format_options.keys()), clear=True)

        pattern = r"│\s*(\d+)\s*│\s*(\d{4}-\d{2}-\d{2})\s*│\s*(\d{2}:\d{2}:\d{2})\s*│\s*(\d+\.\d+)\s*│"
        coincidencias = re.findall(pattern, self.field_data_table)

        data = []
        for index, date, time, value in coincidencias:
            row = []
            row.append(index)
            if date_format == '1':
                row.append(date + 'T' + time)
            else:
                row.append(date)
                row.append(time)
            row.append(value)
            data.append(row)
        input(data)
        format_options[selected_option](data, file_name, self.field_index, date_format)


    # Method to clear all the data of the field
    def clear_field_data():
        pass


    # Method to delete the current field
    def delete_field():
        pass