#
# @file <common.py>
#
# @author Fernando Mendiburu - <fernando.mendiburu@ee.ufcg.edu.br>
#

import sys

from notifypy import Notify
from read_parameters import ReadParametersFile


class Common:
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
            message += f'{dev_value[0]}: {dev_value[1]}{unit}, '
        message = Common.fix_string(message)
        return message

    @staticmethod
    def notification_send(title, message, is_sound):
        params_file = ReadParametersFile()
        notification = Notify()
        notification.title = title
        notification.message = message
        notification.icon = params_file.params['PATH_NOTIF_ICON']
        if is_sound:
            notification.audio = params_file.params['PATH_NOTIF_SOUND']
        notification.send()


if __name__ == '__main__':
    pass
