import csv
import requests

# Method to upload a csv data
def upload_csv(pos):
    # Configuración de la solicitud
    channel_id = '2363113'
    url = f'https://api.thingspeak.com/channels/{channel_id}/bulk_update.csv'
    write_api_key = 'WS24QUGUDCF125HG'
    time_format = 'absolute'

    with open('backup.csv', 'r') as file:
        striped_data = [word.strip().split('\t')[2] for word in file.readlines()]

    # Datos de ejemplo del CSV
    # csv_data = '4,1.1,2,0.3,,,6,7.7,0.8,41.2,19.5,100,ok|3,1,2,3,4,5,6,7,8,41.2,25.1,110,rising'
    # csv_data = '4,1,2,3,4,5,6,7,8,41.2,19.5,100,ok|3,1,2,3,4,5,6,7,8,41.2,25.1,110,rising'
    
    string_template = '0,,,,,,,,,,,,ok|'

    bulk_data = ""
    for index, row_data in enumerate(striped_data):
        lista = string_template.split(',')
        lista[0] = str(index)
        lista[pos] = row_data
        temp_template = ','.join(lista)

        bulk_data += temp_template

        if index == len(striped_data) - 1:
            if bulk_data.endswith('|'):
                bulk_data = bulk_data[:-1] # quitar el ultimo caracter que va a ser siempre un |
                break

    # input(bulk_data)
    # Construir cuerpo de la solicitud
    data_to_send = {
        'write_api_key': write_api_key,
        'time_format': time_format,
        'updates': bulk_data,
    }

    # Realizar la solicitud POST
    response = requests.post(url, data=data_to_send)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        print('Datos subidos correctamente a ThingSpeak.')
    else:
        print('Error al subir datos a ThingSpeak.')
        print('Código de estado HTTP:', response.status_code)
        print('Respuesta del servidor:', response.text)

upload_csv(1)
