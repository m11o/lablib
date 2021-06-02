from sys import path
path.append('/app')
path.append('/app/OASIS')

import pandas as pd
import re

from OASIS.oasis.functions import deconvolve

import utils.constant as const

for context_name in const.CONTEXTS:
    print('context: %s' % context_name)
    for animal_number in const.ANIMAL_NUMBERS:
        animal_name = 'ID181106Cre%s' % animal_number
        print('animal name: %s' % animal_name)

        csv_file_path = './resources/ID181106Cre/%s_Processed/%s_Longitudinal_Traces_%s.csv' % (animal_name, animal_name, context_name)
        df = pd.read_csv(csv_file_path, header=[0, 1], low_memory=False)

        for column_names, items in df.iteritems():
            column_name = column_names[-1]
            if not re.match('\s?C[0-9]{3}', column_name):
                continue

            if items.isnull().all():
                continue

            items = items.astype(float)
            std = items.std(skipna=False)
            items /= std
            items = items.to_numpy()

            print('context: %s, animal: %s, column_name: %s' % (context_name, animal_name, column_name))
            print('items')
            print(items)
            _c, spikes, _b, _g, _lam = deconvolve(items, g=(None, None), penalty=1)

            print('spikes')
            print(spikes)
            df.loc[:, column_names] = spikes

        saved_csv_file_path = re.sub('\.csv', '_spikes.csv', csv_file_path)
        print('saved csv path: %s' % saved_csv_file_path)
        df.to_csv(saved_csv_file_path)
