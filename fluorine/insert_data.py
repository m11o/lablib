import pandas as pd
import re
import sqlalchemy as sa
from sqlalchemy.orm import Session

import utils.constant as const
from utils.databases.fluorine.create_tables import Experiment, Animal, Context, Cell, Fluorescence
from utils.databases.fluorine.settings import ENGINE, DATABASE_URL


class InsertData:
    def __init__(self, animal_name, experiment_name):
        self.experiment = Experiment.find_or_create_by(experiment_name)
        self.animal = Animal.find_or_create_by(self.experiment.id, animal_name)

        self.path = "./resources/%s/%s_Processed/%s_Longitudinal_Traces.csv" % (experiment_name, animal_name, animal_name)
        self.engine = sa.create_engine(DATABASE_URL)
        self.df = pd.read_csv(self.path, header=[1, 2], low_memory=False)

    def exec(self):
        for engram, cell_name in self.df.columns:
            print('debug: create cell')
            print(cell_name)
            match_obj = re.match('\s?(C[0-9]{3})', cell_name)
            if not match_obj:
                continue

            cell_name = match_obj.group(1)
            Cell.find_or_create_by(self.animal.id, cell_name, engram)

        context_rows = self.df.iloc[:, 1]
        for context_name in const.CONTEXTS:
            print('start context: %s' % context_name)

            context = Context.find_or_create_by(self.experiment.id, context_name)
            context_indexes = context_rows[context_rows == context_name].index
            context_data = self.df.iloc[context_indexes[0]:(context_indexes[-1] + 1), :]

            for index, row in context_data.iterrows():
                diff_time = float(row[0])
                time = float(row[2])

                print('diff_time: %f' % diff_time)
                print('time: %f' % time)

                for column_names, value in row.iteritems():
                    cell_name = column_names[-1]
                    match_obj = re.match('\s?(C[0-9]{3})', cell_name)
                    if not match_obj:
                        continue

                    cell_name = match_obj.group(1)
                    print('cell_name: %s' % cell_name)
                    with Session(ENGINE) as session:
                        cell = session.query(Cell).filter(Cell.animal_id == self.animal.id, Cell.name == cell_name).first()
                        if cell is None:
                            continue

                        fluorescence = session.query(Fluorescence.id).filter(Fluorescence.cell_id == cell.id, Fluorescence.context_id == context.id, Fluorescence.time == time).first()
                        if fluorescence is not None:
                            continue

                        fluorescence = Fluorescence()
                        fluorescence.cell_id = cell.id
                        fluorescence.context_id = context.id
                        fluorescence.value = float(0) if re.match('\s?nan', str(value)) else float(value)  # 一旦、nanは0で登録
                        fluorescence.diff_time = float(diff_time)
                        fluorescence.time = float(time)
                        session.add(fluorescence)
                        session.commit()
