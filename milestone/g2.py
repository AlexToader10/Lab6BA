import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


csv_file_path = 'monthly_business_performance_dynamic.csv'
df = pd.read_csv(csv_file_path, parse_dates=['MonthYear'])

df['An'] = df['MonthYear'].dt.year

sns.set_theme(style="whitegrid", rc={"axes.facecolor": (0, 0, 0, 0)})
g = sns.FacetGrid(df, row="An", hue="An", aspect=5, height=1.0, palette="viridis_r")
g.map_dataframe(sns.kdeplot, x="New_Facility_Signups", fill=True, alpha=0.7, linewidth=1.5)
g.map_dataframe(sns.kdeplot, x="New_Facility_Signups", color="w", linewidth=2)
def label(x, color, label):
    ax = plt.gca()
    ax.text(0.02, 0.2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)

g.map(label, "New_Facility_Signups")
g.figure.subplots_adjust(hspace=-0.65)
g.set_titles("")
g.set(yticks=[])
g.despine(bottom=True, left=True)

plt.xlabel("Numar Abonari Noi Lunare", fontsize=13)
g.fig.suptitle('Distributia Lunara a Abonarilor Noi, pe Ani', y=0.98, fontsize=16) # Main title

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout
plt.show()