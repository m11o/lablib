import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.size"] = 22
plt.figure(figsize=(25, 10))

engram_df = pd.read_csv('./results/sulfur/engram_event_rates.csv')
engram_x = engram_df.columns[1:].to_numpy()
engram_y = engram_df.iloc[10, 1:].to_numpy()
engram_error = engram_df.iloc[12, 1:].to_numpy()

non_engram_df = pd.read_csv('./results/sulfur/non_engram_event_rates.csv')
non_engram_x = non_engram_df.columns[1:].to_numpy()
non_engram_y = non_engram_df.iloc[10, 1:].to_numpy()
non_engram_error = non_engram_df.iloc[12, 1:].to_numpy()

plt.errorbar(engram_x, engram_y, yerr=engram_error, capsize=2)
plt.plot(engram_x, engram_y, marker="s", markersize=12, markeredgewidth=3, label='engram cell', color='royalblue')

plt.errorbar(non_engram_x, non_engram_y, yerr=non_engram_error, capsize=2)
plt.plot(non_engram_x, non_engram_y, marker="s", markersize=12, markeredgewidth=3, label='non-engram cell', color='tomato')
plt.legend()

plt.ylim(0, 2.0)
plt.ylabel('Calcium Event Rate (Hz)')
plt.tight_layout()
plt.savefig('results/sulfur/engram_compared_event_rate_figure.png')
