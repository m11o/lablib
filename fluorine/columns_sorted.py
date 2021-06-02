from sys import path
path.append('/app')

import pandas as pd
import re

import utils.constant as const

for animal_number in const.ANIMAL_NUMBERS:
    animal_name = 'ID181106Cre%s' % animal_number

    for context_name in const.CONTEXTS:
        file_path = './resources/ID181106Cre/%s_Processed/%s_Longitudinal_Traces_%s_spikes.csv' % (animal_name, animal_name, context_name)

        df = pd.read_csv(file_path, header=[0, 1])
        df = df.sort_index(axis='columns', level=1, na_position='first')
        saved_csv_file_path = re.sub('\.csv', '_sorted.csv', file_path)
        df.to_csv(saved_csv_file_path)
