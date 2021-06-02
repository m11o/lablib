
from sys import path
path.append('/app')
path.append('/app/OASIS')

import pandas as pd

from matplotlib import pyplot as plt
from OASIS.oasis.functions import deconvolve
from OASIS.oasis.plotting import simpleaxis

csv_file_path = './resources/ID181106Cre/ID181106CreA_Processed/ID181106CreA_Longitudinal_Traces_HC1.csv'
df = pd.read_csv(csv_file_path, header=[0, 1], low_memory=False)

cell_data = df.iloc[:, 4]
cell_data = cell_data.astype(float)

std = cell_data.std(skipna=False)
cell_data = cell_data / std

cell_data = cell_data.to_numpy()

c, s, b, g, lam = deconvolve(cell_data, g=(None, None), penalty=1)

plt.figure(figsize=(20, 4))
plt.subplot(211)
plt.plot(b + c, lw=2, label='denoised')
plt.plot(cell_data, label='data', zorder=-12, c='y')
plt.legend(ncol=3, frameon=False, loc=(.02, .85))
simpleaxis(plt.gca())
plt.subplot(212)
plt.plot(s, lw=2, label='deconvolved', c='g')
plt.ylim(0, 10.0)
plt.legend(ncol=3, frameon=False, loc=(.02, .85))
simpleaxis(plt.gca())
plt.savefig('spike_data.png')



