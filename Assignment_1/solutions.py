import numpy as np
import household as hh
import appliance as ap
import random
import pandas as pd



# Assignment 1_1
# We have a simple household that only has three appliances: a washing machine, an EV and a dishwasher.
# We assume the time-of-Use (ToU) pricing scheme: 1NOK/KWh for peak hour and 0.5NOK/KWh for off-peak hours.
# Peak hours are in the range of 5:00pm-8:00pm while all other timeslots are off-peak hours. 
# Design the strategy to use these appliances to have minimum energy cost. 
# 
# Note: We need a strategy, not just the amount of the minimal energy cost. 
# For example, you may need to consider some exemplary questions. 
# Is it reasonable to use all three appliances at the same time, e.g., 2:00am which has the low energy price? 
# How should we distribute the power load more reasonably in the timeline?



# We have a simple household that only has three appliances: a washing machine, an EV and a dishwasher.
print("Part 1.")
h1 = hh.household("A simple household")

#loads = np.ones(24) * 2.5
#h1.set_max_power_loads(loads)


washing_machine = ap.appliance("~Laundry_machine", total_energy_constraint = 1.94, power_level_constraint_min = 0.0, power_level_constraint_max = 1.94, shiftable = True)
washing_machine.set_operation_time(0,10)

electric_vehicle = ap.appliance("~Electric_vehicle", total_energy_constraint = 9.9, power_level_constraint_max = 3.30, shiftable = True)
electric_vehicle.set_operation_time(0,10)

dishwasher = ap.appliance("~Dishwasher", total_energy_constraint = 1.44, power_level_constraint_max = 1.44, shiftable = True)
dishwasher.set_operation_time(0,10)

h1.add_new_appliance(washing_machine)
h1.add_new_appliance(dishwasher)
h1.add_new_appliance(electric_vehicle)

# We assume the time-of-Use (ToU) pricing scheme: 1NOK/KWh for peak hour and 0.5NOK/KWh for off-peak hours.
# Peak hours are in the range of 5:00pm-8:00pm while all other timeslots are off-peak hours.

prices = np.ones(24) * 0.5
prices[17:20] = np.ones(3) # 5:00pm-8:00pm price is 1
h1.set_pricing(prices)


h1.calculate_minimum_energy_cost()
solution, min_energy_cost = h1.get_solution_report()

print("Solution:{0}".format(solution))
print("Minimum energy cost: {0} NOK".format(min_energy_cost))



# Q: Is it reasonable to use all three appliances at the same time, e.g., 2:00am which has the low energy price?
# A: No
#
# Q: How should we distribute the power load more reasonably in the timeline?
# by setting up an operation time: e.g.: "washing_machine.set_operation_time(0,10)" 
# or setting up maximum power load for particular hours e.g.: "h1.set_max_power_loads(loads)"

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Assignment 1_2
# We have a household with all non-shiftable appliances and all shiftable appliances (see the two lists aforementioned). 
# In addition to these, please choose a random combination of appliances such as 
# coffee maker, ceiling fan, hair dryer, toaster, microwave, router, cellphone charger, cloth iron, separate freezer(s), etc., for the household. 
# Please refer to [2] to add typical energy consumption values for the appliances.
#  
# Please use Real-Time Pricing (RTP) scheme. The RTP model is followed: using a random function to generate the pricing curve in a day.
# The pricing curve should consider higher price in the peak- hours and lower price in the off-peak hours.
#  
# Compute the best strategy to schedule the use of the appliances and write a program in order to minimize energy cost.

print("\n\nPart 2.")
h2 = hh.household("A household")

loads = np.ones(24) * 6.0
h2.set_max_power_loads(loads)

h2.add_shiftable_appliances()

h2.add_non_shiftable_appliances()

# In addition to these, please choose a random combination of appliances such as 
# coffee maker, ceiling fan, hair dryer, toaster, microwave, router, cellphone charger, cloth iron, separate freezer(s), etc., for the household. 
# Please refer to [2] to add typical energy consumption values for the appliances.
h2.add_random_appliances()


# Please use Real-Time Pricing (RTP) scheme. The RTP model is followed: using a random function to generate the pricing curve in a day.
# The pricing curve should consider higher price in the peak- hours and lower price in the off-peak hours.
pricing =  np.random.uniform(low=0.1, high=1, size=(24,))
pricing[17:20] = np.random.uniform(low=1.0, high=2.0, size=(3))
pricing = np.round(pricing,5)
#print(pricing)
h2.set_pricing(pricing)


# Compute the best strategy to schedule the use of the appliances and write a program in order to minimize energy cost.
h2.calculate_minimum_energy_cost()
solution, min_energy_cost = h2.get_solution_report()

print("Solution:{0}".format(solution))
print("Minimum energy cost: {0} NOK".format(min_energy_cost))

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Assignment 1_3
# We consider a small neighborhood that has 30 households. 
# Each household has the same setting as that in question 2. But, we assume that only a fraction of the households owns an EV. 
# 
# Please use Real-Time Pricing (RTP) scheme: using random function to generate the pricing curve in a day. 
# The pricing curve should consider higher price in the peak-hours and lower price in the off-peak hours. 
# 
# Compute the best strategy for scheduling the appliances and write a program in order to minimize energy cost in the neighborhood.



# We consider a small neighborhood that has 30 households.
households = list()
solutions = list()
households_energy_costs = 0.0


# Please use Real-Time Pricing (RTP) scheme: using random function to generate the pricing curve in a day.
# The pricing curve should consider higher price in the peak-hours and lower price in the off-peak hours.
#  
# !!! One pricing strategy for all households in the neighborhood
#  
pricing =  np.random.uniform(low=0.1, high=1, size=(24,))
pricing[17:20] = np.random.uniform(low=1.0, high=2.0, size=(3))
pricing = np.round(pricing,5)

writer = pd.ExcelWriter("Reports/neighborhood/neighborhood.xlsx")

for i in range(30):
    hh_name = "Household{0}".format(i)
    households.append(hh.household(hh_name))
    hhn = households[i]

    loads = np.ones(24) * 6.0
    hhn.set_max_power_loads(loads)

    # Each household has the same setting as that in question 2. But, we assume that only a fraction of the households owns an EV.
    has_ev = (random.randint(0,10) > 4) #probability 50%
    hhn.add_shiftable_appliances(owns_electric_vehicle=has_ev)

    hhn.add_non_shiftable_appliances()

    hhn.add_random_appliances()

    hhn.set_pricing(pricing)


    # Compute the best strategy for scheduling the appliances and write a program in order to minimize energy cost in the neighborhood.
    hhn.calculate_minimum_energy_cost()
    solution, min_energy_cost = hhn.get_solution_report(plot_location="Reports/neighborhood",create_excell=False)
    solution.to_excel(writer, hh_name)
    
    solutions.append(solution)
    households_energy_costs += min_energy_cost

writer.save()
print("Minimum energy cost for the neighborhood: {0} NOK".format(households_energy_costs))














