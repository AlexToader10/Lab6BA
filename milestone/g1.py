import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

csv_file_path = 'monthly_business_performance_dynamic.csv'
df = pd.read_csv(csv_file_path, parse_dates=['MonthYear'])

df = df.sort_values('MonthYear')

fig, ax1 = plt.subplots(figsize=(16, 9))
sns.set_style("darkgrid")

color_active = 'royalblue'
ax1.set_xlabel('Luna-An', fontsize=13)
ax1.set_ylabel('Abonamente Active', color=color_active, fontsize=13)
line1, = ax1.plot(df['MonthYear'], df['Active_Subscribed_Facilities'], color=color_active, marker='o', linestyle='-', linewidth=2.5, markersize=6, label='Abonamente Active')
ax1.tick_params(axis='y', labelcolor=color_active, labelsize=11)
ax1.tick_params(axis='x', labelsize=11)
ax1.grid(True, axis='y', linestyle=':', alpha=0.7)

ax2 = ax1.twinx()
color_signup = 'forestgreen'
color_churn = 'orangered'
color_net = 'purple' 

bar1 = ax2.bar(df['MonthYear'], df['New_Facility_Signups'], color=color_signup, alpha=0.75, width=20, label='Abonari Noi (Lunar)')
line2, = ax2.plot(df['MonthYear'], df['Churned_Facilities'], color=color_churn, marker='.', linestyle='--', linewidth=2.5, markersize=8, label='Renuntari Facilitati (Lunar)')

df['Net_Growth'] = df['New_Facility_Signups'] - df['Churned_Facilities']
line3, = ax2.plot(df['MonthYear'], df['Net_Growth'], color=color_net, linestyle=':', linewidth=3, marker='^', markersize=7, label='Crestere Neta Lunara')

ax2.set_ylabel('Abonari Noi / Renuntari / Crestere Neta', color='black', fontsize=13)
ax2.tick_params(axis='y', labelcolor='black', labelsize=11)
ax2.set_ylim(bottom=min(0, df['Net_Growth'].min() - 2), top=df['New_Facility_Signups'].max() + 5) 
ax2.axhline(0, color='grey', linestyle='--', linewidth=1.2)

plt.title('Dinamica Afacerii', fontsize=18, pad=20)
fig.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.xticks(rotation=45, ha="right")

legend_handles = [line1, bar1, line2, line3]
legend_labels = [h.get_label() for h in legend_handles]
ax1.legend(legend_handles, legend_labels, loc='upper left', fontsize=11, frameon=True, facecolor='white', framealpha=0.8)

plt.show()