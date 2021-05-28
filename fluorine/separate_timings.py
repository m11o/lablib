import pandas as pd
import re

import fluorine.constant as const


class SeparateTiming:
    def __init__(self, path):
        self.path = path
        print(path)

    def exec(self):
        df = pd.read_csv(self.path, header=None, low_memory=False)
        header = df.iloc[2, :]
        context_rows = df.iloc[:, 1]
        for context in const.CONTEXTS:
            print(context)
            context_indexes = context_rows[context_rows == context].index
            context_data = df.iloc[context_indexes[0]:(context_indexes[-1]+1), :]
            context_data.columns = header

            csv_filename = re.sub('\.csv', '_%s.csv' % context, self.path)
            context_data.to_csv(csv_filename)


