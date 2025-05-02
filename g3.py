import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(123)
branches = ['Bucuresti', 'Cluj', 'Iasi', 'Brasov']
claim_types = ['Auto', 'Home', 'Health']
branch_perf_data = []

for branch in branches:
    for claim_type in claim_types:
        if branch == 'Bucuresti' and claim_type == 'Home':
            avg_time = np.random.normal(loc=20, scale=3) 
        elif branch == 'Cluj' and claim_type == 'Auto':
            avg_time = np.random.normal(loc=5, scale=1) 
        elif claim_type == 'Auto':
            avg_time = np.random.normal(loc=8, scale=2)
        elif claim_type == 'Home':
            avg_time = np.random.normal(loc=16, scale=4)
        else:
            avg_time = np.random.normal(loc=12, scale=3)
        if branch == 'Cluj': avg_time *= 1.1 
        if branch == 'Iasi': avg_time *= 0.9 

        branch_perf_data.append({
            'Branch': branch,
            'Claim_Type': claim_type,
            'Average_Processing_Time': max(1, round(avg_time))
        })

df_branch_perf_q3 = pd.DataFrame(branch_perf_data)
df_branch_perf_q3.to_csv('branch_performance_data.csv', index=False)


plt.figure(figsize=(12, 7))
sns.barplot(data=df_branch_perf_q3, x='Branch', y='Average_Processing_Time',
            hue='Claim_Type', palette='muted', 
            order=['Bucuresti', 'Cluj', 'Iasi', 'Brasov']) 

plt.title('Average Claim Processing Time by Branch and Claim Type')
plt.xlabel('Branch Location')
plt.ylabel('Average Processing Time (Days)')
plt.legend(title='Claim Type', bbox_to_anchor=(1.02, 1), loc='upper left') 
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout() 
plt.show()