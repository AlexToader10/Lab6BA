import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

csv_file_path = 'monthly_business_performance_dynamic.csv'
df = pd.read_csv(csv_file_path, parse_dates=['MonthYear'])
df = df.sort_values('MonthYear').reset_index(drop=True)
df['Active_Subscribed_Facilities_Start_of_Month'] = df['Active_Subscribed_Facilities'].shift(1)

if pd.isna(df.loc[0, 'Active_Subscribed_Facilities_Start_of_Month']):
    df.loc[0, 'Active_Subscribed_Facilities_Start_of_Month'] = (
        df.loc[0, 'Active_Subscribed_Facilities'] -
        df.loc[0, 'New_Facility_Signups'] +
        df.loc[0, 'Churned_Facilities']
    )
df['Active_Subscribed_Facilities_Start_of_Month'] = df['Active_Subscribed_Facilities_Start_of_Month'].apply(
    lambda x: max(x, 1) if pd.notna(x) else 1 
)

df['Rata_Renuntari_Calculata'] = (df['Churned_Facilities'] / df['Active_Subscribed_Facilities_Start_of_Month']) * 100
df['Rata_Renuntari_Calculata'] = df['Rata_Renuntari_Calculata'].fillna(0).replace([np.inf, -np.inf], 0)
df_corr_selected = df[[
    'New_Facility_Signups',
    'Active_Subscribed_Facilities',
    'Service_Reputation',
    'Rata_Renuntari_Calculata', 
    'Operational_Capacity_Units'
]].copy()

df_corr_selected.columns = [
    'Abonari Noi',
    'Abonamente Active',
    'Reputatie Serviciu',
    'Rata Renuntari (%)',
    'Capacitate Operationala'
]

correlation_matrix = df_corr_selected.corr()
plt.figure(figsize=(10, 8))
sns.set_theme(style="whitegrid")
cmap = 'coolwarm'

sns.heatmap(correlation_matrix,
            annot=True,
            fmt=".2f",
            cmap=cmap,
            square=True,
            linewidths=.5,
            linecolor='gray',
            cbar_kws={"shrink": .82, "label": "Coeficient de Corelatie Pearson", "orientation": "vertical"},
            vmin=-1, vmax=1, center=0)

plt.title('Heatmap Corelatii intre Indicatori Cheie', fontsize=16, pad=20)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(rotation=0, fontsize=10)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()