from sys import path
path.append('/app')

import pandas as pd
import re

import utils.constant as const

indexes = ['spikes', 'times', 'event_rate']
event_rates = pd.DataFrame(index=indexes, columns=const.CONTEXTS)
event_rates.fillna(0.0, inplace=True)
for index, context in enumerate(const.CONTEXTS):
    for animal_number in const.ANIMAL_NUMBERS:
        animal_name = 'ID181106Cre%s' % animal_number

        file_path = './resources/ID181106Cre/%s_Processed/%s_Longitudinal_Traces_%s_spikes.csv' % (animal_name, animal_name, context)
        df = pd.read_csv(file_path, header=[0, 1])

        for column_names, items in df.iteritems():
            column_name = column_names[-1]
            if not re.match('\s?C[0-9]{3}', column_name):
                continue

            if items.isnull().all():
                continue

            seconds = len(items) / 10.0
            event_count = len(items[items > 0.0])

            event_rates.at['spikes', context] += event_count
            event_rates.at['times', context] += seconds

    events_by_context = event_rates.iloc[:, index]
    event_mean_by_context = events_by_context['spikes'] / float(events_by_context['times'])

    event_rates.at['event_rate', context] = event_mean_by_context

    print(event_rates)

event_rates.to_csv('event_rates_all_cell.csv')
