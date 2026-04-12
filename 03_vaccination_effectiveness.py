# read the test data without vaccination
import pandas as pd
from plotnine import *


charge = [28, 32, 25, 30, 27, 35, 29]
discharge = [22, 26, 19, 24, 21, 30, 25]

# read the test data with vaccination
charge_vaccinated = [20, 25, 18, 22, 19, 28, 24]
discharge_vaccinated = [18, 22, 15, 20, 17, 25, 21]

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

# calculate the ward occupancy for both scenarios
occupancy_unvaccinated = calculate_the_ward_occupancy(charge, discharge)
occupancy_vaccinated = calculate_the_ward_occupancy(charge_vaccinated, discharge_vaccinated)    

# create a dataframe for plotting
data = pd.DataFrame({
    'Day': range(1, len(charge) + 1),
    'Unvaccinated': occupancy_unvaccinated,
    'Vaccinated': occupancy_vaccinated
})

# plot the occupancy over time
plot = (ggplot(data, aes(x='Day'))
        + geom_line(aes(y='Unvaccinated'), color='#BFDFD2', size=1.5)
        + geom_line(aes(y='Vaccinated'), color='#4198DC', size=1.5)
        + labs(title='Ward Occupancy: Vaccinated vs Unvaccinated', y='Number of Patients', x='Day')
        + theme_classic())

plot.show()
# create a stacked bar chart
data_stacked = data.melt(id_vars='Day', var_name='Group', value_name='Occupancy')

plot_stacked = (ggplot(data_stacked, aes(x='Day', y='Occupancy', fill='Group'))
                + geom_bar(stat='identity')
                + labs(title='Ward Occupancy: Vaccinated vs Unvaccinated', y='Number of Patients', x='Day')
                + theme_classic())

plot_stacked.show()
