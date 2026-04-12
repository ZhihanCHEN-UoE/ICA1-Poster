import pandas as pd
from plotnine import *

def track_dual_ward_occupancy(admissions, discharges, transfers):
    n_days = len(admissions)
    if not (n_days == len(discharges) == len(transfers)):
        raise ValueError("All input lists must have the same length.")
        
    mild_occ = [0]*n_days
    severe_occ = [0]*n_days

    mild_occ[0], severe_occ[0] = admissions[0]
    
    for i in range(1,n_days):
        m_in, s_in = admissions[i]
        d_out = discharges[i]
        t = transfers[i]
        
        # 1. Add new admissions
        curr_m = mild_occ[i-1] + m_in
        curr_s = severe_occ[i-1] + s_in
        
        # 2. Process discharges (mild ward only)
        curr_m = max(0, curr_m - d_out)
        
        # 3. Process transfers (clamped to available patients)
        if t > 0:  # Mild -> Severe
            actual_t = min(t, curr_m)
            curr_m -= actual_t
            curr_s += actual_t
        elif t < 0:  # Severe -> Mild
            actual_t = min(-t, curr_s)
            curr_s -= actual_t
            curr_m += actual_t
            
        mild_occ[i]=(curr_m)
        severe_occ[i]=(curr_s)
        
    # Build result DataFrame
    df = pd.DataFrame({
        'Day': range(1, n_days + 1),
        'Mild': mild_occ,
        'Severe': severe_occ,
        'Total': [m + s for m, s in zip(mild_occ, severe_occ)]
    })
    
    # Generate stacked bar chart
    df_plot = df.melt(id_vars='Day', value_vars=['Mild', 'Severe'], 
                      var_name='Ward_Type', value_name='Patients')
    
    plot = (ggplot(df_plot, aes(x='Day', y='Patients', fill='Ward_Type'))
            + geom_bar(stat='identity', position='stack', width=0.6)
            + labs(title='Daily Ward Occupancy by Severity',
                   x='Day', y='Number of Patients', fill='Ward Type')
            + theme_classic()
            + theme(legend_position='top'))
    plot.show()
    
    return df

# === Example Usage for Demo ===

# Format: [[mild_in, severe_in], ...]
daily_admissions = [[15, 5], [20, 8], [18, 6], [22, 7], [19, 9], [25, 10], [21, 8]]
daily_discharges = [10, 12, 15, 14, 18, 20, 16]  # Applied to mild ward only
daily_transfers  = [3, 5, -2, 8, 4, 6, -1]       # +: mild->severe, -: severe->mild
    
result = track_dual_ward_occupancy(daily_admissions, daily_discharges, daily_transfers)
print(result)