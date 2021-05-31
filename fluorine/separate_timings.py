import pandas as pd
import re

import utils.constant as const


class SeparateTiming:
    def __init__(self, path):
        self.path = path
        print(path)

    def exec(self):
        df = pd.read_csv(self.path, header=[1, 2], low_memory=False)
        context_rows = df.iloc[:, 1]
        for context in const.CONTEXTS:
            print(context)
            context_indexes = context_rows[context_rows == context].index
            context_data = df.iloc[context_indexes[0]:(context_indexes[-1]+1), :]

            self.optimize(context_data)

            csv_filename = re.sub('\.csv', '_%s.csv' % context, self.path)
            context_data.to_csv(csv_filename)

    @staticmethod
    def optimize(context_data):
        for column_names, items in context_data.iteritems():
            column_name = column_names[-1]
            if not re.match('\s?C[0-9]{3}', column_name):
                continue

            items = items.astype(float)
            std = items.std(skipna=False)
            items /= std

            context_data.loc[:, column_names] = items
