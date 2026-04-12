import pandas as pd
from plotnine import *

'''
test data
charge:[28, 32, 25, 30, 27, 35, 29]
discharge:[22, 26, 19, 24, 21, 30, 25]
'''

# read the test data
charge = [28, 32, 25, 30, 27, 35, 29]
discharge = [22, 26, 19, 24, 21, 30, 25]

def calculate_the_ward_occupancy(charge, discharge):
    # check the length of the charge and discharge lists
    if len(charge) != len(discharge):
        print("The length of charge and discharge lists must be the same.")
        return None

    occupancy = [0] * len(charge)
    occupancy[0] = charge[0] - discharge[0]
    for i in range(1, len(charge)):
        occupancy[i] = occupancy[i-1] + charge[i] - discharge[i]
    return occupancy
occupancy = calculate_the_ward_occupancy(charge, discharge)
print("Ward Occupancy:", occupancy)

# create a dataframe for plotting
data = pd.DataFrame({
    'Day': range(1, len(charge) + 1),
    'Occupancy': occupancy
}) 
# plot the occupancy over time
data = pd.DataFrame({
    'Day': range(1, len(charge) + 1),
    'Occupancy': occupancy
})

# plot the occupancy
plot = (ggplot(data, aes(x='Day', y='Occupancy'))
        + geom_line(color='#BFDFD2', size=1.5)
        + geom_point(color='#4198DC', size = 3)
        + labs(title='Ward Occupancy', y='Number of Patients', x='Day')
        + theme_classic())

plot.show()