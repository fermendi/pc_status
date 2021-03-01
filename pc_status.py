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

from rw_parameters import ReadParametersCMD, ReadParametersFiles, WriteParametersStatFile
from common import Common


if __name__ == '__main__':

    try:
        Common.credits()
        parser = ReadParametersCMD()
        params_obj = ReadParametersFiles()
        write_obj = WriteParametersStatFile()
        args = parser.get_params()

        battery = Battery(params_obj)
        memory = Memory(params_obj)
        temperature = Temperature(params_obj)
        status = Status(params_obj)

        b_loop = False
        if parser.is_loop():
            b_loop = True

        while True:
            params_obj.update_parameters()
            battery.set_parameters(params_obj)
            memory.set_parameters(params_obj)
            status.set_parameters(params_obj)
            temperature.set_parameters(params_obj)

            if parser.is_notification():
                if battery.is_discharging() and battery.is_notification_battery():
                    battery.alarm_discharging(parser.is_sound())
                if memory.is_high_usage() and memory.is_notification_memory():
                    memory.alarm(parser.is_sound())
                if status.is_cpu_high_usage() and status.is_notification_cpu():
                    status.alarm(parser.is_sound())
                if temperature.is_high_temperature() and temperature.is_notification_temperature():
                    temperature.alarm(parser.is_sound())

            if parser.is_full():
                system = System(params_obj)
                disk = Disk(params_obj)
                network = Network(params_obj)

                system.set_parameters(params_obj)
                disk.set_parameters(params_obj)
                network.set_parameters(params_obj)

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

        # generate dict:
        dict_stats_params = {"BATTERY_STATUS": battery.get_percentage(),
                             "CPU_STATUS": status.get_cpu_usage(),
                             "MEMORY_STATUS": memory.get_memory_usage(),
                            }

        write_obj.write_parameters(dict_stats_params)

    except KeyboardInterrupt:
        print('\nExit program!')
