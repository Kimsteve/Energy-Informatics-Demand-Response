import numpy as np
import appliance as ap
import pulp as p
import pandas as pd
import matplotlib.pyplot as plt
import random

np.set_printoptions(suppress=True)

class household:

    def __init__(self, name):
        """Creates an household

        Keyword arguments:
        name -- the name of an appliance
        """
        self.__name = name
        self.appliances_shiftable = []
        self.appliances_non_shiftable = []
        self.no_appliances_shiftable = 0
        self.no_appliances_non_shiftable = 0
        self.non_shiftable_appliances_load = np.zeros(24)
        self.pricing = []
        self.my_opt_problem = p.LpProblem(sense = p.LpMinimize)

    def add_new_appliance(self, appliance):
        
        if appliance.shiftable:
            self.appliances_shiftable.append(appliance)
            self.no_appliances_shiftable += 1
        else:
            self.non_shiftable_appliances_load = np.add(self.non_shiftable_appliances_load,appliance.operation_time)
            self.appliances_non_shiftable.append(appliance)
            self.no_appliances_non_shiftable += 1
        
    
    def set_pricing(self, pricing):
        self.pricing = pricing
    
    def set_max_power_loads(self,loads):
        self.max_power_loads = loads
    
    def add_shiftable_appliances(self, owns_electric_vehicle = True):
        # Shiftable appliances
        dishwasher = ap.appliance("~Dishwasher", total_energy_constraint = 1.44, power_level_constraint_max = 1.44, shiftable = True)
        dishwasher.set_operation_time(9,10)

        washing_machine = ap.appliance("~Laundry_machine", total_energy_constraint = 1.94, power_level_constraint_max = 1.94, shiftable = True)
        washing_machine.set_operation_time(0,10)

        cloth_dryer = ap.appliance("~Cloth_dryer", total_energy_constraint = 2.50, power_level_constraint_max = 2.50, shiftable = True)
        cloth_dryer.set_operation_time(0,10)

        if owns_electric_vehicle:
            electric_vehicle = ap.appliance("~Electric_vehicle", total_energy_constraint = 9.9, power_level_constraint_max = 3.3, shiftable = True)
            electric_vehicle.set_operation_time(0,10)
            self.add_new_appliance(electric_vehicle)

        self.add_new_appliance(dishwasher)
        self.add_new_appliance(washing_machine)
        self.add_new_appliance(cloth_dryer)
        

    def add_non_shiftable_appliances(self):
        lighting = ap.appliance("Lighting", power_level_constraint_max = 0.15, shiftable = False)
        lighting.set_operation_time(10,20)

        heating = ap.appliance("Heating", power_level_constraint_max = 0.40, shiftable = False)
        heating.set_operation_time(0,24)

        refrigerator_freezer = ap.appliance("Refrigerator", power_level_constraint_max = 0.055, shiftable = False)
        refrigerator_freezer.set_operation_time(0,24)

        electric_stove = ap.appliance("Electric_stove", power_level_constraint_max = 1.95, shiftable = False)
        electric_stove.set_operation_time(17,19)

        tv = ap.appliance("Tv", power_level_constraint_max = 0.12, shiftable = False)
        tv.set_operation_time(17,22)

        computer = ap.appliance("Computer", power_level_constraint_max = 0.06, shiftable = False)
        computer.set_operation_time(10,20)

        self.add_new_appliance(lighting)
        self.add_new_appliance(heating)
        self.add_new_appliance(refrigerator_freezer)
        self.add_new_appliance(electric_stove)
        self.add_new_appliance(tv)
        self.add_new_appliance(computer)
    
    def add_random_appliances(self):
        #coffee maker, ceiling fan, hair dryer, toaster, microwave, router, cellphone charger, cloth iron, separate freezer
        random_appliances = list()
        
        #coffee maker- morning
        coffee_maker1 = ap.appliance("*~Coffee_maker_morning", total_energy_constraint = 1.20, power_level_constraint_max = 1.20, shiftable = True)
        coffee_maker1.set_operation_time(6,10)
        random_appliances.append(coffee_maker1)

        #coffee maker- evening
        coffee_maker2 = ap.appliance("*~Coffee_maker_evening", total_energy_constraint = 1.20, power_level_constraint_max = 1.20, shiftable = True)
        coffee_maker2.set_operation_time(16,20)
        random_appliances.append(coffee_maker2)

        #ceiling fan
        ceiling_fan = ap.appliance("*Ceiling_fan", power_level_constraint_max = 0.05, shiftable = False)
        ceiling_fan.set_operation_time(8,23)
        random_appliances.append(ceiling_fan)

        #hair dryer
        hair_dryer = ap.appliance("*~Hair_dryer", total_energy_constraint = 2.0, power_level_constraint_max = 2.0, shiftable = True)
        hair_dryer.set_operation_time(6,8)
        random_appliances.append(hair_dryer)

        #toaster
        toaster = ap.appliance("*Toaster", power_level_constraint_max = 1.20, shiftable = False)
        toaster.set_operation_time(8,9)
        random_appliances.append(toaster)
        
        #microwave
        microwave = ap.appliance("*~Microwave", total_energy_constraint = 3.0, power_level_constraint_max = 1.50, shiftable = True)
        microwave.set_operation_time(17,19)
        random_appliances.append(microwave)
        
        #router
        router = ap.appliance("*Router", power_level_constraint_max = 0.01, shiftable = False)
        router.set_operation_time(0,24)
        random_appliances.append(router)
        
        #cellphone charger
        cellphone_charger = ap.appliance("*~Cellphone_charger", total_energy_constraint =0.14, power_level_constraint_max = 0.07, shiftable = True)
        cellphone_charger.set_operation_time(17,24)
        random_appliances.append(cellphone_charger)
        
        
        #cloth iron
        cloth_iron = ap.appliance("*~Cloth_iron", total_energy_constraint =1.0, power_level_constraint_max = 1.0, shiftable = True)
        cloth_iron.set_operation_time(17,24)
        random_appliances.append(cloth_iron)
        
        #separate freezer
        separate_freezer = ap.appliance("*Separate_freezer", power_level_constraint_max = 0.4, shiftable = False)
        separate_freezer.set_operation_time(0,24)
        random_appliances.append(separate_freezer)

        all_app = len(random_appliances)                    #number of all
        amount = random.sample(range(2, all_app), 1)        #get a number from 2 - "number of all"
        draw = random.sample(range(0, all_app), amount[0])  #choose a random combination
        
        for i in range(len(draw)):
            self.add_new_appliance(random_appliances[draw[i]])



    def calculate_minimum_energy_cost(self):

        hour_limits = []
        total_costs = p.pulp.LpAffineExpression()
        # e.g.: total_costs = 0.41702*Dw0 + 0.72032*Dw1 + 0.41919*Dw10 + [...] + 0.18626*Wm6 + 0.34556*Wm7 + 0.39677*Wm8 + 0.53882*Wm9
        


        for appl_id, appliance in enumerate(self.appliances_shiftable):
            hour_limits.append(list())
            for hour in range(24):
                hour_up_limit = float(appliance.operation_time[hour])

                hour_low_limit = appliance.power_level_constraint_min if hour_up_limit > 0.0 else 0.0     #for tests
            
                hour_name = "{0}0{1}¦{2}¦{3}".format(appliance.name,hour,hour_up_limit,self.pricing[hour]) if hour <= 9 else "{0}{1}¦{2}¦{3}".format(appliance.name,hour,hour_up_limit,self.pricing[hour])

                #if hour_low_limit > 0.0:
                    #print(hour_name)

                limit_for_hour = p.LpVariable(hour_name, lowBound = hour_low_limit, upBound=hour_up_limit, cat='Continuous')
                hour_limits[appl_id].append( np.array(limit_for_hour) )
                total_costs.addterm(limit_for_hour, self.pricing[hour])

        self.my_opt_problem += total_costs


        for appl_id, appliance in enumerate(self.appliances_shiftable):
            self.my_opt_problem += np.ones(24).dot(hour_limits[appl_id]) == appliance.total_energy_constraint
            # e.g.: "x0 + x1 + ... + x22 + x23 = 9.9"
        


        if hasattr(self, "max_power_loads"):
            for i in range(24):
                max_load = self.max_power_loads[i]                      # the load for each hour
                other_load = self.non_shiftable_appliances_load[i]      # the load of no shiftable appliances
                self.my_opt_problem += np.ones(self.no_appliances_shiftable).dot(np.array(hour_limits).T[i]) <= (max_load - other_load)

        
        self.my_opt_problem.solve()


    def get_solution_report(self, plot_location = "Reports", create_excell = True):
        shiftable_names = [ appliance.name.replace("¦","") for appliance in self.appliances_shiftable]
        non_shiftable_names = [ appliance.name.replace("¦","") for appliance in self.appliances_non_shiftable]
        all_names = shiftable_names
        all_names += non_shiftable_names
        
        no_rows = (self.no_appliances_shiftable + self.no_appliances_non_shiftable)
        result = { row_name : [0.0] * 24 for row_name in all_names }

        for variable in self.my_opt_problem.variables():
            params = variable.name.split("¦")
            name = params[0]
            hour = int(params[1])
            value = round(variable.varValue,5)
            result[name][hour] = value
        


        non_shiftables =  { appliance.name.replace("¦","") : appliance.operation_time.tolist() for appliance in self.appliances_non_shiftable }

        for key, value in non_shiftables.items():
            result[key] = value



        total_energy_cost = 0.0
        for key, row in result.items():
            total_energy_cost += self.pricing.T.dot(row)
        
        result = pd.DataFrame(result)

        # Save plot to file
        plt.style.use('bmh')
        result.plot.bar(stacked=True)

        if hasattr(self, "max_power_loads"):
            plt.plot((self.max_power_loads),color='red',label='Maximum power load', linestyle='dashed')
        
        plt.plot(self.pricing, color= "black", label = "Price", linestyle='dashed')
        
        plt.title("Optimization result: {0}".format(p.LpStatus[self.my_opt_problem.status]))
        plt.xlabel("Time")
        plt.ylabel("Load")
        lgd = plt.legend(loc=2, bbox_to_anchor=(1.05, 1)) 
        plt.grid('on')

        plt.savefig("{0}/{1}".format(plot_location, self.__name), bbox_extra_artists=(lgd,), bbox_inches='tight')
        
        result = result.T
        pricing = pd.DataFrame(self.pricing).T
        result.loc["Pricing"] = pricing.loc[0]

        # Save results to excell
        if create_excell:
            writer = pd.ExcelWriter("Reports/{0}.xlsx".format(self.__name))
            result.to_excel(writer,'Sheet1')
            writer.save()

        return result, round(total_energy_cost,5)
        




if __name__ == '__main__':
    h1 = household("Household 1")

    washing_machine = ap.appliance("Wm", total_energy_constraint = 1.94, power_level_constraint_max = 1.94, shiftable = True)
    washing_machine.set_operation_time(8,11)

    dishwasher = ap.appliance("Dw", total_energy_constraint = 1.44, power_level_constraint_max = 1.44, shiftable = True)
    electric_vehicle = ap.appliance("Ev", total_energy_constraint = 9.90, power_level_constraint_max = 3.30,  shiftable = True)

    h1.add_new_appliance(washing_machine)
    h1.add_new_appliance(dishwasher)
    h1.add_new_appliance(electric_vehicle)

    np.random.seed(1)
    prices = np.random.uniform(low=0.0, high=1, size=(24,))
    prices = np.round(prices,5)
    h1.set_pricing(prices)

    h1.calculate_minimum_energy_cost()
    h1.get_solution_report()