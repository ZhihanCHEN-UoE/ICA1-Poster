import pandas as pd
from plotnine import ggplot, aes, geom_line, geom_point, geom_bar, labs, theme_classic, theme

# ============================================================================
# DEMO DATA
# ============================================================================
charge = [10, 15, 20, 18, 22, 19, 25, 21, 23, 20]
discharge = [5, 8, 12, 15, 14, 18, 20, 16, 19, 18]

charge_vaccinated = [8, 12, 15, 14, 18, 15, 20, 18, 19, 17]
discharge_vaccinated = [5, 8, 12, 15, 14, 18, 20, 16, 19, 18]

# ============================================================================
# STEP 01: CALCULATE WARD OCCUPANCY
# ============================================================================
def calculate_the_ward_occupancy(charge, discharge):
    if len(charge) != len(discharge):
        print("Error: charge and discharge lists must be the same length.")
        return None
    
    occupancy = [0] * len(charge)
    occupancy[0] = charge[0] - discharge[0]
    for i in range(1, len(charge)):
        occupancy[i] = occupancy[i-1] + charge[i] - discharge[i]
    return occupancy

def step_01():
    print("\n" + "="*70)
    print("STEP 01: WARD OCCUPANCY ANALYSIS")
    print("="*70)
    
    occupancy = calculate_the_ward_occupancy(charge, discharge)
    print(f"\nWard Occupancy by Day: {occupancy}")
    
    data = pd.DataFrame({
        'Day': range(1, len(charge) + 1),
        'Occupancy': occupancy
    })
    
    plot = (ggplot(data, aes(x='Day', y='Occupancy'))
            + geom_line(color='#BFDFD2', size=1.5)
            + geom_point(color='#4198DC', size=3)
            + labs(title='Ward Occupancy Over Time', y='Number of Patients', x='Day')
            + theme_classic())
    
    input("Press Enter to view the occupancy plot...")
    plot.show()

# ============================================================================
# STEP 02: INFECTION WAVE ANALYSIS
# ============================================================================
def infection_wave(data):
    diff = [0] * (len(data) - 1)
    for i in range(1, len(data)):
        diff[i-1] = data[i] - data[i-1]
    return diff

def find_peak(data):
    result = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            result.append([i, data[i]])
    
    if len(result) == 0:
        return [len(data), data[-1]]
    elif len(result) == 1:
        return result[0]
    else:
        result.sort(key=lambda x: x[1], reverse=True)
        return result[0]

def step_02():
    print("\n" + "="*70)
    print("STEP 02: INFECTION WAVE ANALYSIS")
    print("="*70)
    
    occupancy = calculate_the_ward_occupancy(charge, discharge)
    infection_wave_data = infection_wave(occupancy)
    peak = find_peak(infection_wave_data)
    
    print(f"\nDaily Change in Occupancy: {infection_wave_data}")
    print(f"Peak infection wave at Day {peak[0]} with magnitude {peak[1]}")

# ============================================================================
# STEP 03: VACCINATION EFFECTIVENESS
# ============================================================================
def step_03():
    print("\n" + "="*70)
    print("STEP 03: VACCINATION EFFECTIVENESS")
    print("="*70)
    
    occupancy_unvaccinated = calculate_the_ward_occupancy(charge, discharge)
    occupancy_vaccinated = calculate_the_ward_occupancy(charge_vaccinated, discharge_vaccinated)
    
    data = pd.DataFrame({
        'Day': range(1, len(charge) + 1),
        'Unvaccinated': occupancy_unvaccinated,
        'Vaccinated': occupancy_vaccinated
    })
    
    print("\nComparison Data:")
    print(data.to_string(index=False))
    
    plot = (ggplot(data, aes(x='Day'))
            + geom_line(aes(y='Unvaccinated'), color='#FF6B6B', size=1.5, linetype='dashed')
            + geom_line(aes(y='Vaccinated'), color='#4198DC', size=1.5)
            + labs(title='Ward Occupancy: Vaccinated vs Unvaccinated', 
                   y='Number of Patients', x='Day')
            + theme_classic())
    
    input("Press Enter to view the occupancy plot...")
    plot.show()

# ============================================================================
# STEP 05: DUAL WARD OCCUPANCY (MILD & SEVERE)
# ============================================================================
def track_dual_ward_occupancy(admissions, discharges, transfers):
    n_days = len(admissions)
    if not (n_days == len(discharges) == len(transfers)):
        raise ValueError("All input lists must have the same length.")
    
    mild_occ = [0] * n_days
    severe_occ = [0] * n_days
    
    mild_occ[0], severe_occ[0] = admissions[0]
    
    for i in range(1, n_days):
        m_in, s_in = admissions[i]
        d_out = discharges[i]
        t = transfers[i]
        
        curr_m = mild_occ[i-1] + m_in
        curr_s = severe_occ[i-1] + s_in
        
        curr_m = max(0, curr_m - d_out)
        
        if t > 0:
            actual_t = min(t, curr_m)
            curr_m -= actual_t
            curr_s += actual_t
        elif t < 0:
            actual_t = min(-t, curr_s)
            curr_s -= actual_t
            curr_m += actual_t
        
        mild_occ[i] = curr_m
        severe_occ[i] = curr_s
    
    df = pd.DataFrame({
        'Day': range(1, n_days + 1),
        'Mild': mild_occ,
        'Severe': severe_occ,
        'Total': [m + s for m, s in zip(mild_occ, severe_occ)]
    })
    
    df_plot = df.melt(id_vars='Day', value_vars=['Mild', 'Severe'], 
                      var_name='Ward_Type', value_name='Patients')
    
    plot = (ggplot(df_plot, aes(x='Day', y='Patients', fill='Ward_Type'))
            + geom_bar(stat='identity', position='stack', width=0.6)
            + labs(title='Ward Occupancy by Severity', x='Day', y='Number of Patients')
            + theme_classic())
    
    input("Press Enter to view the occupancy plot...")
    plot.show()
    return df

def step_05():
    print("\n" + "="*70)
    print("STEP 05: DUAL WARD OCCUPANCY (MILD & SEVERE)")
    print("="*70)
    
    daily_admissions = [[15, 5], [20, 8], [18, 6], [22, 7], [19, 9], [25, 10], [21, 8]]
    daily_discharges = [10, 12, 15, 14, 18, 20, 16]
    daily_transfers = [3, 5, -2, 8, 4, 6, -1]
    
    result = track_dual_ward_occupancy(daily_admissions, daily_discharges, daily_transfers)
    print("\nDetailed Results:")
    print(result.to_string(index=False))

# ============================================================================
# MAIN PRESENTATION
# ============================================================================
if __name__ == "__main__":
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  HOSPITAL WARD OCCUPANCY & VACCINATION ANALYSIS".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    step_01()
    step_02()
    step_03()
    step_05()
    
    print("\n" + "█"*70)
    print("Analysis Complete!".center(70))
    print("█"*70 + "\n")