#
# @file <system_all.py>
#
# @author Fernando Mendiburu - <fernando.mendiburu@ee.ufcg.edu.br>
#

from system import System, CPU, Memory, Disk, Network, Battery, Temperature


class Sensor:
    def __init__(self, params_obj):
        self.battery = Battery(params_obj)
        self.memory = Memory(params_obj)
        self.temperature = Temperature(params_obj)
        self.cpu = CPU(params_obj)
        self.system = System(params_obj)
        self.disk = Disk(params_obj)
        self.network = Network(params_obj)

    def update(self):
        self.battery.update()
        self.memory.update()
        self.temperature.update()
        self.cpu.update()
        self.disk.update()
        self.network.update()

    def set_parameters(self, params_obj):
        self.battery.set_parameters(params_obj)
        self.memory.set_parameters(params_obj)
        self.temperature.set_parameters(params_obj)
        self.cpu.set_parameters(params_obj)
        self.system.set_parameters(params_obj)
        self.disk.set_parameters(params_obj)
        self.network.set_parameters(params_obj)

    def run(self):
        self.system.run()
        self.cpu.run()
        self.memory.run()
        self.disk.run()
        self.network.run()
        self.battery.run()
        self.temperature.run()


if __name__ == '__main__':
    pass
