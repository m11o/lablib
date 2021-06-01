import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.size"] = 22

labels = np.array(['1h', '24h'])
freezing_rate_Ret = np.array([54.51666667, 43.0625])
freezing_rate_EXT = np.array([22.3625, 10.70416667])
freezing_rate_EM = np.array([28.89166667, 16.04166667])

error_Ret = np.array([5.635268405, 4.419377444])
error_EXT = np.array([2.665680156, 4.175071384])
error_EM = np.array([5.354655728, 7.339815632])

left = np.arange(len(freezing_rate_Ret))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 10), dpi=200)

ax.bar(x=left - width, height=freezing_rate_Ret, yerr=error_Ret, capsize=2, width=width, label='Ret', align='center', color='royalblue')
ax.bar(x=left, height=freezing_rate_EXT, yerr=error_EXT, capsize=2, width=width, label='Ext', align='center', color='tomato')
ax.bar(x=left + width, height=freezing_rate_EM, yerr=error_EM, capsize=2, width=width, label='EM', align='center', color='yellow')
ax.set_xticks(left)
ax.set_xticklabels(labels=labels)
plt.ylim(0, 100)
plt.xlim(-0.5, 1.5)
ax.set_ylabel('Freezing Rate(%)')
ax.legend()

plt.tight_layout()
plt.savefig('[fluorine]FreezingRateFigure.png')
