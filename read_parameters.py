#
# @file <read_parameters.py>
#
# @author Fernando Mendiburu - <fernando.mendiburu@ee.ufcg.edu.br>
#

import argparse
import json
import os
import sys


class ReadParametersCMD:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='pc_status information')
        self.parser.add_argument('--info', '--i', '-i', dest='info',
                                 type=str, default='status',
                                 choices=['full', 'status'],
                                 help='System info.')
        self.parser.add_argument('--loop', '--l', '-l', dest='loop',
                                 type=str, default='n',
                                 choices=['y', 'n'],
                                 help='Give the values continuously.')
        self.parser.add_argument('--notifications', '--n', '-n', dest='notifications',
                                 type=str, default='y',
                                 choices=['y', 'n'],
                                 help='Pop-up notifications.')
        self.parser.add_argument('--sound', '--s', '-s', dest='sound',
                                 type=str, default='n',
                                 choices=['y', 'n'],
                                 help='Sound of the notifications.')
        self.args = self.parser.parse_args()

    def get_params(self):
        return self.args

    def is_full(self):
        return self.args.info == 'full'

    def is_status(self):
        return self.args.info == 'status'

    def is_loop(self):
        return self.args.loop == 'y'

    def is_sound(self):
        return self.args.sound == 'y'

    def is_notification(self):
        return self.args.notifications == 'y'


class ReadParametersFile:
    def __init__(self):
        # load parameters:
        self.params = self.get_params_from_file()

    def verify_paths(self, params):
        for (key,value) in params.items():
            try:
                if value[0] == '~':
                    params[key] = os.path.expanduser('~') + value[1:]
            except:
                pass
        return params

    def get_params_from_file(self):
        params = {}
        try:
            with open(os.path.expanduser('~') + '/pc_status/config/config.txt', 'r') as json_file:
                params = self.load_params(json_file)
                params = self.verify_paths(params)
                return params
        except FileNotFoundError:
            print("ERROR: Parameters file 'config.txt' not found!\nExit program!")
            sys.exit()

    def load_params(self, file):
        try:
            params = json.load(file)
            return params
        except:
            print("ERROR: Problem in the data format of file 'config.txt'!\nExit program!")
            sys.exit()

    def is_notification_battery(self):
        return self.params['NOTIFICATION_BATTERY'] == 'yes'

    def is_notification_cpu(self):
        return self.params['NOTIFICATION_CPU'] == 'yes'

    def is_notification_memory(self):
        return self.params['NOTIFICATION_MEMORY'] == 'yes'

    def is_notification_temperature(self):
        return self.params['NOTIFICATION_TEMPERATURE'] == 'yes'


#-------------------------------------------------------------------------------------------
#------------------------------------------Main---------------------------------------------
#-------------------------------------------------------------------------------------------

if __name__ == '__main__':
    pass

