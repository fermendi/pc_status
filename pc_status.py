#
# @file <pc_status.py>
#
# @author Fernando Mendiburu - <fernando.mendiburu@ee.ufcg.edu.br>
#

from system import Network
from system import Battery
from system import Memory
from system import System
from system import Status
from system import Disk
from system import Temperature

from read_parameters import ReadParametersCMD, ReadParametersFile
from common import Common



if __name__ == '__main__':

    try:
        Common.credits()
        parser = ReadParametersCMD()
        params_file = ReadParametersFile()
        args = parser.get_params()

        battery = Battery()
        memory = Memory()
        temperature = Temperature()
        status = Status()

        b_loop = False
        if parser.is_loop():
            b_loop = True

        while True:
            if parser.is_notification():
                if battery.is_unplugged() and params_file.is_notification_battery():
                    battery.alarm_unplugged(parser.is_sound())
                if memory.is_high_usage() and params_file.is_notification_memory():
                    memory.alarm(parser.is_sound())
                if status.is_cpu_high_usage() and params_file.is_notification_cpu():
                    status.alarm(parser.is_sound())
                if temperature.is_high_temperature() and params_file.is_notification_temperature():
                    temperature.alarm(parser.is_sound())

            if parser.is_full():
                system = System()
                status = Status()
                disk = Disk()
                network = Network()

                print(Common.SEPARATOR)
                system.run()
                status.run()
                memory.run()
                disk.run()
                network.run()
                battery.run()
                temperature.run()
                print(Common.SEPARATOR)

            elif parser.is_status():
                print(Common.SEPARATOR)
                print(status.get_usage_msg())
                print(temperature.get_temperature_msg('current'))
                print(memory.get_mem_swap_msg())
                print(battery.get_percentage_msg())
                print(Common.SEPARATOR)

            if not b_loop:
                break

    except KeyboardInterrupt:
        print('\nExit program!')