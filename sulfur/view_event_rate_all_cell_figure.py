import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('./results/sulfur/event_rates_all_cell.csv')
x = df.columns[1:].to_numpy()
y = df.iloc[2, 1:].to_numpy()

plt.rcParams["font.size"] = 22

plt.figure(figsize=(25, 10))
plt.plot(x, y, marker="s", markersize=12, markeredgewidth=3)
plt.ylim(0, 2.0)
plt.tight_layout()
plt.savefig('results/sulfur/event_rate_figure_all_cell.png')
