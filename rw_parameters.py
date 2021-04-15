#
# @file <rw_parameters.py>
#
# @author Fernando Mendiburu - <fernando.mendiburu@ee.ufcg.edu.br>
#

import argparse

from common import Common


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


class ReadParametersFiles:
    def __init__(self):
        self.update_parameters()

    def update_parameters(self):
        self.config_params = Common.read_params(Common.CONFIG_FILE)
        self.stats_params = Common.read_params(Common.STATS_FILE)


class WriteParametersStatFile:
    def write_parameters(self, dict_stat):
        Common.write_dict_file(Common.STATS_FILE, dict_stat)


if __name__ == '__main__':
    pass
