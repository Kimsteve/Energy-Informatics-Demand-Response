import numpy as np

class appliance:
    # name = ""
    # total_energy_constraint = 0.0
    # power_level_constraint_max = 0.0
    # power_level_constraint_min = 0.0
    # shiftable = True
    # operation_time = np.zeros(24)
    

    def __init__(self,  name, total_energy_constraint = 0.0, power_level_constraint_max = 0.0, power_level_constraint_min = 0.0, shiftable = True):
        """Creates an appliance

        Keyword arguments:
        name -- the name of an appliance
        total_energy_constraint -- total energy consumption per day
        power_level_constraint_max -- maximum power level
        power_level_constraint_min -- minimum power level (default 0.0)
        shiftable -- whether the appliance is shiftable or not
        """
        self.name = "{0}¦".format(name)
        self.total_energy_constraint = total_energy_constraint
        self.power_level_constraint_max = power_level_constraint_max
        self.power_level_constraint_min = power_level_constraint_min
        self.shiftable = shiftable
        self.operation_time = np.zeros(24)
        self.operation_time[:] = power_level_constraint_max

    def set_operation_time(self, beginning, end):
        if beginning < end:
            self.operation_time = np.zeros(24)
            self.operation_time[beginning:end] = self.power_level_constraint_max
        else:
            self.operation_time[:] = self.power_level_constraint_max
            self.operation_time[end:beginning] = 0.0
            print("")



if __name__ == '__main__':
    a1 = appliance("Object appliance 1", 9, 3.0)
    print(a1.operation_time)

    a1.set_operation_time(18,22)
    print(a1.operation_time)

    a1.set_operation_time(22,3)
    print(a1.operation_time)