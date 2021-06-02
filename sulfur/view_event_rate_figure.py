import matplotlib.pyplot as plt
import pandas as pd


def build_event_rate_figure(type):
    df = pd.read_csv('./results/sulfur/%s.csv' % type)
    x = df.columns[1:].to_numpy()
    y = df.iloc[10, 1:].to_numpy()
    error = df.iloc[12, 1:].to_numpy()

    plt.rcParams["font.size"] = 22

    plt.figure(figsize=(25, 10))
    plt.errorbar(x, y, yerr=error, capsize=2)
    plt.plot(x, y, marker="s", markersize=12, markeredgewidth=3, color='royalblue')
    plt.ylim(0, 2.0)
    plt.ylabel('Calcium Event Rate (Hz)')
    plt.tight_layout()
    plt.savefig('results/sulfur/%s_figure.png' % type)


build_event_rate_figure('event_rates')
build_event_rate_figure('engram_event_rates')
build_event_rate_figure('non_engram_event_rates')



