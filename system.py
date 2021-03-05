#
# @file <system.py>
#
# @author Fernando Mendiburu - <fernando.mendiburu@ee.ufcg.edu.br>
#

import psutil
import platform

from common import Common
from datetime import datetime


class System:
    def __init__(self, params_obj):
        self.uname = platform.uname()
        self.bt = datetime.fromtimestamp(psutil.boot_time())
        self.params_obj = params_obj

    def print_info(self):
        print(Common.SEPARATOR)
        print(f'System: {self.uname.system}')
        print(f'Node Name: {self.uname.node}')
        print(f'Release: {self.uname.release}')
        print(f'Version: {self.uname.version}')
        print(f'Machine: {self.uname.machine}')
        print(f'Processor: {self.uname.processor}')
        print(Common.SEPARATOR)

    def print_boot_time(self):
        print(Common.SEPARATOR)
        print(f'Boot Time: {self.bt.day:02d}/{self.bt.month:02d}/{self.bt.year} ' \
                         f'{self.bt.hour:02d}:{self.bt.minute:02d}:{self.bt.second:02d}')
        print(Common.SEPARATOR)

    def set_parameters(self, params_obj):
        self.params_obj = params_obj

    def run(self):
        self.print_info()
        self.print_boot_time()


class CPU:
    def __init__(self, params_obj):
        self.uname = platform.uname()
        self.cpufreq = psutil.cpu_freq()
        self.params_obj = params_obj
        self.update()

    def update(self):
        self.cpu_usage = psutil.cpu_percent()
        self.cores_usage = psutil.cpu_percent(percpu=True, interval=1)

    def print_info(self):
        print(Common.SEPARATOR)
        print(f'Physical Cores: {psutil.cpu_count(logical=False)}')
        print(f'Total Cores: {psutil.cpu_count(logical=True)}')
        print(f'Max Frequency: {self.cpufreq.max:.2f}Mhz')
        print(f'Min Frequency: {self.cpufreq.min:.2f}Mhz')
        print(f'Current Frequency: {self.cpufreq.current:.2f}Mhz')
        print(Common.SEPARATOR)

    def print_usage(self):
        print(self.get_usage_msg())

    def get_usage_msg(self):
        dev_usage_list = self.get_total_usage()
        usage_msg = Common.generate_message(dev_usage_list, '%')
        return usage_msg

    def get_cpu_usage_list(self):
        return [('CPU', self.cpu_usage)]

    def get_cpu_usage(self):
        return self.cpu_usage

    def get_cores_usage_list(self):
        dev_usage_list = []
        for i, percentage in enumerate(self.cores_usage):
            dev_usage_list.append((f'Core{i}', percentage))
        return dev_usage_list

    def get_total_usage(self):
        return self.get_cpu_usage_list() + self.get_cores_usage_list()

    def alarm(self, is_sound):
        Common.notification_send('CPU',
                                 f'The CPU usage has reached {self.get_usage_msg()}!',
                                 self.params_obj.config_params,
                                 is_sound)

    def is_cpu_high_usage(self):
        usage_list = self.get_total_usage()
        for device in usage_list:
            if device[1] >= self.params_obj.config_params['HIGH_USAGE_CPU']:
                return True
        return False

    def set_parameters(self, params_obj):
        self.params_obj = params_obj

    def is_notification_cpu(self):
        return self.params_obj.config_params['NOTIFICATION_CPU'] == 'yes'

    def run(self):
        self.print_info()
        self.print_usage()


class Memory:
    def __init__(self, params_obj):
        self.svmem = psutil.virtual_memory()
        self.swap = psutil.swap_memory()
        self.params_obj = params_obj
        self.update()
        self.PERCENTAGE_MEM_SWAP = f'Memory Usage: {self.get_memory_usage()}% (Swap: {self.get_swap_usage()}%)'

    def update(self):
        self.available_memory = self.svmem.total
        self.used_memory = self.svmem.used
        self.memory_percent = self.svmem.percent
        self.available_memory_swap = self.swap.free
        self.used_memory_swap = self.swap.used
        self.memory_percent_swap = self.swap.percent

    def get_usage_msg(self):
        return f'Memory Usage: {self.get_memory_usage()}% (Swap: {self.get_swap_usage()}%)'

    def virtual_mem(self):
        print(Common.SEPARATOR)
        print(f'Memory: {Common.convert_units(self.svmem.total)}')
        print(f'Available Memory: {Common.convert_units(self.available_memory)}')
        print(f'Used Memory: {Common.convert_units(self.used_memory)}')
        print(f'Memory Usage: {self.memory_percent}%')
        print(Common.SEPARATOR)

    def swap_mem(self):
        print(Common.SEPARATOR)
        print(f'Swap Memory: {Common.convert_units(self.swap.total)}')
        print(f'Free Swap Memory: {Common.convert_units(self.available_memory_swap)}')
        print(f'Used Swap Memory: {Common.convert_units(self.used_memory_swap)}')
        print(f'Swap Memory Usage: {self.memory_percent_swap}%')
        print(Common.SEPARATOR)

    def is_high_usage(self):
        if self.get_memory_usage() >= self.params_obj.config_params['HIGH_USAGE_MEM']:
            return True
        else:
            return False

    def get_memory_usage(self):
        return self.memory_percent

    def get_swap_usage(self):
        return self.memory_percent_swap

    def get_mem_swap_msg(self):
        return f'Memory: {self.get_memory_usage()}% (swap: {self.get_swap_usage()}%)'

    def alarm(self, is_sound):
        Common.notification_send('Memory',
                                 f'The memory usage has reached {self.get_memory_usage()}%!',
                                 self.params_obj.config_params,
                                 is_sound)

    def set_parameters(self, params_obj):
        self.params_obj = params_obj

    def is_notification_memory(self):
        return self.params_obj.config_params['NOTIFICATION_MEMORY'] == 'yes'

    def run(self):
        self.virtual_mem()
        self.swap_mem()


class Disk:
    def __init__(self, params_obj):
        self.disk_partition_list = []
        self.params_obj = params_obj
        self.update()

    def update(self):
        self.partitions = psutil.disk_partitions()
        self.disk_io = psutil.disk_io_counters()

    def info(self):
        self.read_since_boot = f'Total read since boot: {Common.convert_units(self.disk_io.read_bytes)}'
        self.write_since_boot = f'Total write since boot: {Common.convert_units(self.disk_io.write_bytes)}'

        for partition in self.partitions:
            self.disk_partition_list.append(f'Device: {partition.device}')
            self.disk_partition_list.append(f'\tMountpoint: {partition.mountpoint}')
            self.disk_partition_list.append(f'\tFile system type: {partition.fstype}')

            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue

            self.disk_partition_list.append(f'\tTotal Size part: {Common.convert_units(partition_usage.total)}')
            self.disk_partition_list.append(f'\tUsed part: {Common.convert_units(partition_usage.used)}')
            self.disk_partition_list.append(f'\tFree part: {Common.convert_units(partition_usage.free)}')
            self.disk_partition_list.append(f'\tOccupancy part: {partition_usage.percent}%')

        print(Common.SEPARATOR)
        for partition in self.disk_partition_list:
            print(partition)
        print(self.read_since_boot)
        print(self.write_since_boot)
        print(Common.SEPARATOR)

    def set_parameters(self, params_obj):
        self.params_obj = params_obj

    def run(self):
        self.info()


class Network:
    def __init__(self, params_obj):
        self.interfaces = []
        self.params_obj = params_obj
        self.update()

    def update(self):
        self.if_addrs = psutil.net_if_addrs()
        self.net_io = psutil.net_io_counters()

    def info(self):
        self.bytes_received = f'Total bytes received: {Common.convert_units(self.net_io.bytes_recv)}'
        self.bytes_send = f'Total bytes sent: {Common.convert_units(self.net_io.bytes_sent)}'

        for interface_name, interface_addresses in self.if_addrs.items():
            for address in interface_addresses:
                self.interfaces.append(f'Interface: {interface_name}')
                if str(address.family) == 'AddressFamily.AF_INET':
                    self.interfaces.append(f'\tIP Address: {address.address}')
                    self.interfaces.append(f'\tIP Netmask: {address.netmask}')
                    self.interfaces.append(f'\tBroadcast IP: {address.broadcast}')
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    self.interfaces.append(f'\tMAC Address: {address.address}')
                    self.interfaces.append(f'\tIP Netmask: {address.netmask}')
                    self.interfaces.append(f'\tBroadcast MAC: {address.broadcast}')

        print(Common.SEPARATOR)
        for interface in self.interfaces:
            print(interface)
        print(self.bytes_send)
        print(self.bytes_received)
        print(Common.SEPARATOR)

    def set_parameters(self, params_obj):
        self.params_obj = params_obj

    def run(self):
        self.info()


class Battery:
    def __init__(self, params_obj):
        self.status = psutil.sensors_battery()
        self.params_obj = params_obj
        self.update()

    def update(self):
        self.power_unplugged = self.status.power_plugged
        self.battery_percent = self.status.percent

    def info(self):
        print(Common.SEPARATOR)
        print(self.get_percentage_msg())
        print(Common.SEPARATOR)

    def is_unplugged(self):
        return not self.power_unplugged

    def is_discharging(self):
        return self.is_below_threshold() and self.is_diff_charge_negative()

    def is_below_threshold(self):
        return self.params_obj.config_params['DISCHARGING_BATTERY'] <= self.get_percentage()

    def is_diff_charge_negative(self):
        return Common.is_first_great_second(self.params_obj.stats_params['BATTERY_STATUS'],
                                            self.get_percentage())

    def get_percentage(self):
        return round(self.battery_percent, 2)

    def get_percentage_msg(self):
        return f'Battery percentage: {self.get_percentage():.2f}%'

    def alarm_unplugged(self, is_sound):
        Common.notification_send('Battery',
                                 f'The batery is not pluggged! ({self.get_percentage():0.2f}%)',
                                 self.params_obj.config_params,
                                 is_sound)

    def alarm_discharging(self, is_sound):
        Common.notification_send('Battery',
                                 f'The batery is discharging! ({self.get_percentage():0.2f}%)',
                                 self.params_obj.config_params,
                                 is_sound)

    def is_notification_battery(self):
        return self.params_obj.config_params['NOTIFICATION_BATTERY'] == 'yes'

    def set_parameters(self, params_obj):
        self.params_obj = params_obj

    def run(self):
        self.info()


class Temperature:
    def __init__(self, params_obj):
        self.status = psutil.sensors_temperatures()
        self.params_obj = params_obj
        self.update()

    def update(self):
        self.key_dev = self.status.items()

    def info(self):
        temperatures_current = self.get_temperature_msg('current')
        temperatures_high = self.get_temperature_msg('high')
        temperatures_critical = self.get_temperature_msg('critical')
        print(Common.SEPARATOR)
        print(f'Temp Current:  {temperatures_current}')
        print(f'Temp High:     {temperatures_high}')
        print(f'Temp Critical: {temperatures_critical}')
        print(Common.SEPARATOR)

    def get_temperatures_list(self):
        temp_list = []
        for (key,devices) in self.key_dev:
            for device_temperatures in devices:
                device = self.choose_device(device_temperatures)
                if device is not None:
                    temp_list.append((device, device_temperatures))
        return temp_list

    def pick_temperatures(self, temp_list, temp_type):
        i = 0
        temp = []
        for (dev,temperatures) in temp_list:
            if temperatures.current > 0:
                if dev.find('Core') != -1:
                    if temp_type == 'current':
                        temp.append((f'Core{i}', temperatures.current))
                    elif temp_type == 'high':
                        temp.append((f'Core{i}', temperatures.high))
                    elif temp_type == 'critical':
                        temp.append((f'Core{i}', temperatures.critical))
                    i += 1
                else:
                    if temp_type == 'current':
                        temp.append((f'Core{i}', temperatures.current))
                    elif temp_type == 'high':
                        temp.append((f'Core{i}', temperatures.high))
                    elif temp_type == 'critical':
                        temp.append((f'Core{i}', temperatures.critical))
        return temp

    def get_status(self, temp_list):
        for device in temp_list:
            if device[1].current >= device[1].critical:
                return 'CRITICAL'
            elif device[1].current >= device[1].high:
                return 'HIGH'
        return 'OK'

    def get_temperature_msg(self, temp_type):
        temp_list = self.get_temperatures_list()
        temp = self.pick_temperatures(temp_list, temp_type)
        temp_msg = Common.generate_message(temp, 'º')
        return temp_msg

    def alarm(self, is_sound):
        temp_list = self.get_temperatures_list()
        status = self.get_status(temp_list)
        temp_msg = self.get_temperature_msg('current')
        Common.notification_send('Temperature',
                                 f'Temperature is {status}! ({temp_msg})',
                                 self.params_obj.config_params,
                                 is_sound)

    def is_high_temperature(self):
        return self.get_status(self.get_temperatures_list()) != 'OK'

    def choose_device(self, device_temperatures):
        if not device_temperatures.current == 0:
            if device_temperatures.label == '':
                return 'CPU'
            else:
                return device_temperatures.label

    def set_parameters(self, params_obj):
        self.params_obj = params_obj

    def is_notification_temperature(self):
        return self.params_obj.config_params['NOTIFICATION_TEMPERATURE'] == 'yes'

    def run(self):
        self.info()


if __name__ == '__main__':
    pass
