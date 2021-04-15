#
# @file <pc_status.py>
#
# @author Fernando Mendiburu - <fernando.mendiburu@ee.ufcg.edu.br>
#

from sensor import Sensor
from rw_parameters import ReadParametersCMD, ReadParametersFiles, WriteParametersStatFile
from common import Common

if __name__ == '__main__':

    try:
        Common.credits()
        parser = ReadParametersCMD()
        params_obj = ReadParametersFiles()
        write_obj = WriteParametersStatFile()

        sensor = Sensor(params_obj)

        b_loop = False
        if parser.is_loop():
            b_loop = True

        while True:
            params_obj.update_parameters()
            sensor.update()
            sensor.set_parameters(params_obj)

            if parser.is_notification():
                if sensor.battery.is_discharging_below_threshold() and sensor.battery.is_notification_battery():
                    sensor.battery.alarm_discharging(parser.is_sound())
                if sensor.memory.is_high_usage() and sensor.memory.is_notification_memory():
                    sensor.memory.alarm(parser.is_sound())
                if sensor.cpu.is_cpu_high_usage() and sensor.cpu.is_notification_cpu():
                    sensor.cpu.alarm(parser.is_sound())
                if sensor.temperature.is_high_temperature() and sensor.temperature.is_notification_temperature():
                    sensor.temperature.alarm(parser.is_sound())

            if parser.is_full():
                print(Common.SEPARATOR)
                sensor.run()
                print(Common.SEPARATOR)

            elif parser.is_status():
                print(Common.SEPARATOR)
                print(sensor.cpu.get_usage_msg())
                print(Common.SEPARATOR)
                print(sensor.temperature.get_temperature_string())
                print(Common.SEPARATOR)
                print(sensor.memory.get_mem_swap_msg())
                print(sensor.battery.get_percentage_msg())
                print(Common.SEPARATOR)

            if not b_loop:
                break

        # generate dict:
        dict_stats_params = {"BATTERY_STATUS": sensor.battery.get_percentage(),
                             "CPU_STATUS": sensor.cpu.get_cpu_usage(),
                             "MEMORY_STATUS": sensor.memory.get_memory_usage(),
                             }

        write_obj.write_parameters(dict_stats_params)

    except KeyboardInterrupt:
        print('\nExit program!')
