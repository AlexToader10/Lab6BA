import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(42)
branches = ['Sibiu', 'Bucuresti', 'Timisoara', 'Constanta', 'Iasi', 'Cluj', 'Brasov']
n_claims_per_branch = np.random.randint(50, 400, len(branches))

branch_data = []
for i, branch in enumerate(branches):
    volume = n_claims_per_branch[i]
    base_satisfaction = np.random.uniform(3.5, 4.8)
    volume_effect = -0.01 * max(0, volume - 150)
    avg_score = np.clip(base_satisfaction + volume_effect + np.random.normal(0, 0.15), 1, 5)

    branch_data.append({
        'Branch': branch,
        'Claim_Volume': volume,
        'Avg_Feedback_Score': avg_score
    })

df_branches_q2 = pd.DataFrame(branch_data)
df_branches_q2.to_csv('branches_data.csv', index=False)


plt.figure(figsize=(10, 6))
sns.regplot(data=df_branches_q2, x='Claim_Volume', y='Avg_Feedback_Score',
            scatter_kws={'s': 80, 'alpha': 0.7}, 
            line_kws={'color': 'red', 'linestyle': '--'}, 
            ci=95)

plt.title('Branch Claim Volume vs. Average Customer Satisfaction')
plt.xlabel('Total Claim Volume')
plt.ylabel('Average Customer Feedback Score (1-5)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.ylim(1, 5.2)
plt.xlim(left=min(df_branches_q2['Claim_Volume']) - 20)
plt.show()