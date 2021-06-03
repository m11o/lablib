from sys import path
path.append('/app')

import matplotlib.pyplot as plt
import pandas as pd

import utils.constant as const


def label_diff(x, y, text):
    plt.annotate(text, xy=(x - .1, y * 1.05), zorder=10)


plt.rcParams["font.size"] = 22
plt.figure(figsize=(25, 10))

engram_df = pd.read_csv('./results/sulfur/engram_event_rates.csv', header=0, index_col=0)
engram_x = engram_df.columns.to_numpy()
engram_y = engram_df.loc['mean', :].to_numpy()
engram_error = engram_df.loc['sem', :].to_numpy()

non_engram_df = pd.read_csv('./results/sulfur/non_engram_event_rates.csv', header=0, index_col=0)
non_engram_x = non_engram_df.columns.to_numpy()
non_engram_y = non_engram_df.loc['mean', :].to_numpy()
non_engram_error = non_engram_df.loc['sem', :].to_numpy()

plt.errorbar(engram_x, engram_y, yerr=engram_error, capsize=2)
plt.plot(engram_x, engram_y, marker="s", markersize=12, markeredgewidth=3, label='engram cell', color='royalblue')

plt.errorbar(non_engram_x, non_engram_y, yerr=non_engram_error, capsize=2)
plt.plot(non_engram_x, non_engram_y, marker="s", markersize=12, markeredgewidth=3, label='non-engram cell', color='tomato')
plt.legend()

diff_texts = pd.read_csv('./results/sulfur/diff_for_event_rates.csv', header=0, index_col=0)
for index, context in enumerate(const.CONTEXTS):
    engram_value = engram_df.loc['mean', context]
    non_engram_value = non_engram_df.loc['mean', context]

    engram_error_value = engram_df.loc['sem', context]
    non_engram_error_value = non_engram_df.loc['sem', context]
    label_diff(index, max(engram_value, non_engram_value) + max(engram_error_value, non_engram_error_value), diff_texts.loc['diff', context])

plt.ylim(0, 2.0)
plt.ylabel('Calcium Event Rate (Hz)')
plt.tight_layout()
plt.savefig('results/sulfur/engram_compared_event_rate_figure.png')
