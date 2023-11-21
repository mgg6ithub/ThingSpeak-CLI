import csv
import requests

# Method to upload a csv data
def upload_csv():
    # Configuración de la solicitud
    channel_id = '2353273'
    url = f'https://api.thingspeak.com/channels/{channel_id}/bulk_update.csv'
    write_api_key = 'PEEBLQNCAXTAWHQW'
    time_format = 'relative'
    
    # Datos de ejemplo del CSV
    csv_data = '4,1.1,2,0.3,,,6,7.7,0.8,41.2,19.5,100,ok|3,1,2,3,4,5,6,7,8,41.2,25.1,110,rising'

    # Construir cuerpo de la solicitud
    data_to_send = {
        'write_api_key': write_api_key,
        'time_format': time_format,
        'updates': csv_data,
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

upload_csv()
