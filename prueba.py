import csv
import requests
import re
from tabulate import tabulate

# # Method to upload a csv data
# def upload_csv(pos):
#     # Configuración de la solicitud
#     channel_id = '2363113'
#     url = f'https://api.thingspeak.com/channels/{channel_id}/bulk_update.csv'
#     write_api_key = 'WS24QUGUDCF125HG'
#     time_format = 'absolute'

#     with open('backup.csv', 'r') as file:
#         striped_data = [word.strip().split('\t')[2] for word in file.readlines()]

#     # Datos de ejemplo del CSV
#     # csv_data = '4,1.1,2,0.3,,,6,7.7,0.8,41.2,19.5,100,ok|3,1,2,3,4,5,6,7,8,41.2,25.1,110,rising'
#     # csv_data = '4,1,2,3,4,5,6,7,8,41.2,19.5,100,ok|3,1,2,3,4,5,6,7,8,41.2,25.1,110,rising'
    
#     string_template = '0,,,,,,,,,,,,ok|'

#     bulk_data = ""
#     for index, row_data in enumerate(striped_data):
#         lista = string_template.split(',')
#         lista[0] = str(index)
#         lista[pos] = row_data
#         temp_template = ','.join(lista)

#         bulk_data += temp_template

#         if index == len(striped_data) - 1:
#             if bulk_data.endswith('|'):
#                 bulk_data = bulk_data[:-1] # quitar el ultimo caracter que va a ser siempre un |
#                 break

#     # input(bulk_data)
#     # Construir cuerpo de la solicitud
#     data_to_send = {
#         'write_api_key': write_api_key,
#         'time_format': time_format,
#         'updates': bulk_data,
#     }

#     # Realizar la solicitud POST
#     response = requests.post(url, data=data_to_send)

#     # Verificar el estado de la respuesta
#     if response.status_code == 200:
#         print('Datos subidos correctamente a ThingSpeak.')
#     else:
#         print('Error al subir datos a ThingSpeak.')
#         print('Código de estado HTTP:', response.status_code)
#         print('Respuesta del servidor:', response.text)

# upload_csv(1)

# cadena = """
# ╭───┬────────────┬──────────┬──────╮
# │ 1 │ 2023-12-01 │ 18:18:39 │  1.9 │
# ├───┼────────────┼──────────┼──────┤
# │ 2 │ 2023-12-01 │ 18:18:55 │  6.6 │
# ├───┼────────────┼──────────┼──────┤
# │ 3 │ 2023-12-01 │ 18:19:10 │ 13.1 │
# ╰───┴────────────┴──────────┴──────╯
# """


# pattern = r"│\s*(\d+)\s*│\s*(\d{4}-\d{2}-\d{2})\s*│\s*(\d{2}:\d{2}:\d{2})\s*│\s*(\d+\.\d+)\s*│"

# coincidencias = re.findall(pattern, cadena)

# all_rows = []
# for index, date, time, value in coincidencias:
#     row = []
#     row.append(index)
#     row.append(date + 'T' + time)
#     row.append(value)
#     all_rows.append(row)

# new_string = tabulate(all_rows, tablefmt='rounded_grid')

# print(new_string)



# with open('todo.csv', 'r') as file:
#     pattern = r"(\d+)[\s\,\|\-]+(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})[\s\,\|\-]+(\d+(\.\d+)?)"
    
#     for row in file:
#         match = re.match(pattern, row)
#         print(match.groups.)
    # for row in file.readlines():

@staticmethod
def print_help_template(help_dict):
    help_str = ""
    for entri in help_dict:
        help_str += f"{entri:<20}{help_dict[entri]}\n"
    return help_str

help_dict = {
    "rename": "Change the field name.",
    "upload": "Upload data to the current field.",
    "upload csv": "Upload the data of a csv file to the field.",
    "download data": "Download the data from the current field to a file.(xlsx, txt, csv)"
}
        

print(print_help_template(help_dict))