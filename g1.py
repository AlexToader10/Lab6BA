import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(42)
n_claims = 500
claim_types = ['Auto', 'Home', 'Health']
data = {
    'Claim_ID': range(n_claims),
    'Claim_Type': np.random.choice(claim_types, n_claims, p=[0.4, 0.3, 0.3]),
    'Processing_Time': []
}
for claim_type in data['Claim_Type']:
    if claim_type == 'Auto':
        # Faster, less variable
        time = np.random.normal(loc=7, scale=2)
    elif claim_type == 'Home':
        # Slower, more variable
        time = np.random.normal(loc=15, scale=5)
    else: # Health
        # Bimodal - some fast, some complex/slow
        time = np.random.choice([np.random.normal(loc=5, scale=1.5),
                                 np.random.normal(loc=20, scale=4)])
    data['Processing_Time'].append(max(1, round(time))) # Ensure positive time

df_claims_q1 = pd.DataFrame(data)
df_claims_q1.to_csv('claims_data.csv', index=False)

plt.figure(figsize=(10, 6))
sns.violinplot(data=df_claims_q1, x='Claim_Type', y='Processing_Time',
               order=['Auto', 'Home', 'Health'],
               palette='viridis',
               inner='quartile')

plt.title('Distribution of Claim Processing Time by Claim Type')
plt.xlabel('Claim Type')
plt.ylabel('Processing Time (Days)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()