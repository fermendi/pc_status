#
# @file <common.py>
#
# @author Fernando Mendiburu - <fernando.mendiburu@ee.ufcg.edu.br>
#

import sys
import os
import json

from notifypy import Notify


class Common:
    STATS_FILE = os.path.expanduser('~') + '/pc_status/config/stats_output.txt'
    CONFIG_FILE = os.path.expanduser('~') + '/pc_status/config/config.txt'

    SEPARATOR = "-" * 80
    UNITS = ["", "K", "M", "G", "T", "P"]
    BYTES = 1024

    @staticmethod
    def credits():
        print(Common.SEPARATOR)
        print('pc_status: Display the status of your computer.')
        print('Fernando Mendiburu - 2021')
        print(Common.SEPARATOR)

    @staticmethod
    def convert_units(bytes):
        try:
            for unit in Common.UNITS:
                if bytes < Common.BYTES:
                    return f'{bytes:.2f}{unit}B'
                bytes /= Common.BYTES
        except ZeroDivisionError:
            print('factor should be different of zero!')
            sys.exit()

    @staticmethod
    def fix_string(string):
        return string[0:-2]

    @staticmethod
    def generate_message(list_dev_value, unit):
        message = ''
        for dev_value in list_dev_value:
            message += f'{dev_value[0]}: {dev_value[1]}{unit}\n'
        message = Common.fix_string(message)
        return message

    @staticmethod
    def notification_send(title, message, config_dict, b_sound):
        notification = Notify()
        notification.title = title
        notification.message = message
        notification.icon = config_dict['PATH_NOTIF_ICON']
        if b_sound:
            notification.audio = config_dict['PATH_NOTIF_SOUND']
        notification.send()

    @staticmethod
    def write_params(file, data_dict):
        with open(file, 'w') as fp:
            json.dump(data_dict, fp)

    @staticmethod
    def read_params(file):
        try:
            with open(file, 'r') as fp:
                dict_params = json.load(fp)
                dict_params = Common.verify_paths(dict_params)
                return dict_params
        except FileNotFoundError:
            print(f'ERROR: File {file} not found!\nExit program!')
            sys.exit()
        except ValueError:
            print(f'ERROR: Probably a problem in the data format of file {fp.name}!\nExit program!')

    @staticmethod
    def verify_paths(params):
        for (key, value) in params.items():
            try:
                if value[0] == '~':
                    params[key] = os.path.expanduser('~') + value[1:]
            except:
                pass
        return params

    @staticmethod
    def write_dict_file(file, dict):
        Common.write_params(file, dict)


if __name__ == '__main__':
    pass
