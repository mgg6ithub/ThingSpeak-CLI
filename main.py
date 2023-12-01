from src.thingspeak import ThingSpeak
from src.utils import Utils
from src.canal import Channel
from src.field import Field

from colorama import Fore, init
import signal
import sys
import re

#RAMA DEVELOP CREADA

# u = Utils()
init()


# Method to handle the exit of the program when ctrl + c is pressed
def signal_handler(signum=None, frame=None):
    # ctrl + c
    if signum == signal.SIGINT:
        Utils.clear()
        sys.exit(0)
    # ctrl + l
    # elif signum == signal.SIGINFO:
    #     Utils.clear()
    else:
        sys.exit(0)


# MORE SIGNALS
signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGINFO, signal_handler)


# Method to check the user-api-token
def checkUserApyKey(user_api_key):
    Utils.clear()
    init()
    req = Utils.make_request(method="GET",
                            url=f"https://api.thingspeak.com/channels.json?api_key={user_api_key}")

    if req.status_code == 200:
        return True
    elif req.status_code == 401:
        return False


# Method to login
def login():
    while True:
        Utils.clear()
        str_banner = "1. login in with ThingSpeak web page CREDENTIALS.\n\n" \
                    "2. login with APY KEY.\n\n" \
                    "CTRL + C to exit the program at any time.\n"

        option = Utils.endless_terminal(str_banner, "1", "2")
        Utils.clear()

        if option == "2":
            user_api_key = input("Enter your api key: ")

            if checkUserApyKey(user_api_key):
                print(Fore.GREEN + "Successfull " + Fore.WHITE + "APY KEY provided.")
                Utils.wait_animation(1)
                main_menu(user_api_key)
            else:
                print(Fore.RED + "Wrong " + Fore.WHITE + "APY KEY provided.")
                Utils.wait_animation(1)


# Method to control de flow of a selected field
def field_menu(ts, channel, index, field_name):
    field = Field(index, field_name, channel.id, channel.write_api_key, channel.read_api_key)
    field.read_data_from_field()

    str_field_menu_help = "rename\trename the field\n" \
                        "upload\tupload data to the current field\n" \
                        "upload csv\tupload the data of a csv file to the field\n" \
                        "download data\tdownload data from the current field\n" \
                        "clear field\tclear all the data from this field\n" \
                        "delete field\tremove the field and all his data\n" \

    options_dict = {
        "upload": field.subir_datos,
        "upload csv": field.upload_csv,
        "download data": field.download_data,
        "clear field": field.clear_field_data, # LA API DE THINGSPEAK NO PROPORCIONA UNA RUTA PARA ESTO
        "delete field": field.delete_field # LA API DE THINGSPEAK NO PROPORCIONA UNA RUTA PARA ESTO
    }
    
    while True:
        option = Utils.endless_terminal(field.field_data_table, *list(options_dict.keys()), help_message=str_field_menu_help, menu=channel.channel_name, menu1=field_name, clear=True)
    
        if option == 'b':
            break

        field_operation = options_dict[option]()
        if field_operation == 'actualizar':
            field.read_data_from_field()


def fields_selector(ts, channel):
    pattern = re.compile(r"^[1-8]$")

    str_field_list_commands_help = "create field\tTo create a new field. Up to 8 fields in total.\n" \
    "rename field\tRename a field and give it a new name.\n" \
    "clear fields\tClear all the data from all the fields.\n" \
    "delete field\tDelete a existing field.\n" \
    "delete all fields\tDelete all existing field and their data.\n"

    options_dict = {
        "create field": channel.create_one_field, # OK
        "rename field": channel.rename_field_name, # OK
        "clear fields": channel.clear_data_from_all_fields, # OK
        "delete field": channel.delete_one_field, # LA API DE THINGSPEAK NO PROPORCIONA UNA FORMA DE BORRA UN SOLO CANAL
        "delete all fields": channel.delete_all_fields # LA API DE THINGSPEAK NO PROPORCIONA UNA FORMA DE BORRA UN SOLO CANAL
    }
    
    while True:
        o = channel.print_channel_fields()

        if o == 'b':
            break
        
        if o == 'refresh':
            continue

        valid_options = list(options_dict.keys()) + channel.valid_field_indexes

        field_menu_option = Utils.endless_terminal(channel.table_of_fields, *valid_options, help_message=str_field_list_commands_help, menu=channel.channel_name)

        if field_menu_option == 'b':
            break

        # field has been selected
        if pattern.match(field_menu_option):
            field_menu(ts, channel, field_menu_option, channel.get_field_name(int(field_menu_option)))

        # option in field list has been selected (help, create field, delete field, ...)
        if field_menu_option in options_dict:
            options_dict[field_menu_option]()


# Method to control the flow of a selected channel
# + Selecet a field
# + Remove the channel
def channel_menu(ts, user_api_key, i, indexes, channel_name):
    channel = Channel(user_api_key, i, indexes[i], channel_name)

    str_channel_help = "\n\nCHANNEL OPTIONS\n" \
                            "------------------\n\n" \
                            "1 -- Channel information and settings\n\n" \
                            "2 -- Channel fields.\n\n" \
                            "3 -- Clear all channel data.\n\n" \
                            "4 -- Delete the channel.\n\n" \
                            "Enter \"b\" to go backwards"

    options_dict = {
        "1": channel.doNothing,
        "2": channel.get_channel_fields,
        "3": channel.clear_data_from_all_fields,
        "4": channel.delete_channel
    }

    while True:

        option = Utils.endless_terminal(channel.create_channel_resume_table() + str_channel_help, *list(options_dict.keys()), menu=channel.channel_name, clear=True)

        if option == '1':
            
            more_info_table = ''

            while True:

                str_help_channel_info = "more info\tKeys of the channel.\n" \
                                        "update info\tUpdate a the channel information. Name, tags, etc..."
                
                update_menu_options_dict = {
                    "more info": channel.display_more_channel_info,
                    "update info": channel.update_channels_information
                }

                update_option = Utils.endless_terminal(channel.generate_channel_information_table() + '\n' + more_info_table, 
                                                       *list(update_menu_options_dict.keys()),
                                                        help_message=str_help_channel_info, 
                                                        menu=channel.channel_name, clear=True)

                if update_option == 'b':
                    break

                more_info_table = update_menu_options_dict[update_option]()

        if option == 'b':
            break
        elif option == '2':
            fields_selector(ts, channel)
        
        channel_option = options_dict[option]()

        # Refresh
        if option == '3' or option == '4' and channel_option == 'reset':
            input("Reseting")
            ts.get_account_info()
            break


# ThingSpeak menu Method
def main_menu(user_api_key):
    ts = ThingSpeak(user_api_key)

    while True:
        if ts.hayCanales:
            str_banner = "1 -- PUBLIC CHANNELS.\n\n" \
                        "2 -- PRIVATE CHANNELS.\n\n" \
                        "3 -- ALL CHANNELS.\n\n" \
                        "4 -- Create a new channel.\n" \

            option = Utils.endless_terminal(str_banner, "1", "2", "3", "4", clear="yes")

            if option.__eq__("b"):
                signal_handler()

            if option == "1":
                indexes = ts.print_channel_index(ts.public_channels)
            elif option == "2":
                indexes = ts.print_channel_index(ts.private_channels)
            elif option == "3":
                indexes = ts.print_channel_index(ts.all_channels)
            elif option == "4":
                ts.create_channel(user_api_key)
                ts.get_account_info()
                continue

            i = Utils.endless_terminal("\nSelect a channel.\nOr enter \"b\" to go backwards.", *indexes.keys())

            if i.__eq__('b'):
                continue

            channel_menu(ts, user_api_key, i, indexes, ts.get_channel_name(int(i)))
        else:
            i = Utils.endless_terminal("You dont have any channels in this account.\nDo you want to create one? [y/n] ",
                                tty=False, clear=True)
            if i.__eq__("y"):
                ts.create_channel(user_api_key)
                ts.get_account_info()


"0WX1WIYR7G3QMKUR"
if __name__ == '__main__':
    # login()
    main_menu('0WX1WIYR7G3QMKUR')
