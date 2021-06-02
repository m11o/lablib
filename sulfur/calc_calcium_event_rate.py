from sys import path
path.append('/app')

import pandas as pd
import numpy as np
import re
import math

import utils.constant as const


def calc_statics_data_by_context(df, context_index, context):
    df_by_context = df.iloc[:, context_index]
    mean = df_by_context.mean()
    std = df_by_context.std()
    sem = std / math.sqrt(len(const.ANIMAL_NUMBERS))

    df.at['mean', context] = mean
    df.at['s.d', context] = std
    df.at['sem', context] = sem


indexes = const.ANIMAL_NUMBERS.copy()
indexes.extend(['mean', 's.d', 'sem'])
event_rates = pd.DataFrame(index=const.ANIMAL_NUMBERS, columns=const.CONTEXTS)
engram_event_rates = pd.DataFrame(index=const.ANIMAL_NUMBERS, columns=const.CONTEXTS)
non_engram_event_rates = pd.DataFrame(index=const.ANIMAL_NUMBERS, columns=const.CONTEXTS)
for index, context in enumerate(const.CONTEXTS):
    for animal_number in const.ANIMAL_NUMBERS:
        animal_name = 'ID181106Cre%s' % animal_number

        file_path = './resources/ID181106Cre/%s_Processed/%s_Longitudinal_Traces_%s_spikes.csv' % (animal_name, animal_name, context)

        print('exec: %s' % file_path)
        df = pd.read_csv(file_path, header=[0, 1])

        event_rate_by_cells = np.array([])
        engram_event_rate_by_cells = np.array([])
        non_engram_event_rate_by_cells = np.array([])
        for column_names, items in df.iteritems():
            column_name = column_names[-1]
            engram = column_names[0] != '#N/A'
            if not re.match('\s?C[0-9]{3}', column_name):
                continue

            if items.isnull().all():
                continue

            seconds = len(items) / 10.0
            event_count = len(items[items > 0.0])

            calcium_event_rate = event_count / seconds
            event_rate_by_cells = np.append(event_rate_by_cells, calcium_event_rate)

            if engram:
                engram_event_rate_by_cells = np.append(engram_event_rate_by_cells, calcium_event_rate)
            else:
                non_engram_event_rate_by_cells = np.append(non_engram_event_rate_by_cells, calcium_event_rate)

        event_rates.at[animal_number, context] = np.mean(event_rate_by_cells)
        engram_event_rates.at[animal_number, context] = np.mean(engram_event_rate_by_cells)
        non_engram_event_rates.at[animal_number, context] = np.mean(non_engram_event_rate_by_cells)

    calc_statics_data_by_context(event_rates, index, context)
    calc_statics_data_by_context(engram_event_rates, index, context)
    calc_statics_data_by_context(non_engram_event_rates, index, context)

event_rates.to_csv('event_rates.csv')
engram_event_rates.to_csv('engram_event_rates.csv')
non_engram_event_rates.to_csv('non_engram_event_rates.csv')
