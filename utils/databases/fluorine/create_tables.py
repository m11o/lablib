from sqlalchemy import Table, Column, Integer, String, Boolean, Float, create_engine, MetaData, DECIMAL, DATETIME

import fluorine.constant as const

url = const.DATABASE_URL
engine = create_engine(url)
meta = MetaData(engine)

Table(
    'experiments', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), index=True, unique=True)
)
Table(
    'animals', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('experiment_id', Integer, nullable=False, index=True),
    Column('identification', String(255), nullable=False, index=True, unique=True)
)
Table(
    'contexts', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('experiment_id', Integer, nullable=False, index=True),
    Column('name', String(255), nullable=False),
    Column('sort_index', Integer, default=0)
)
Table(
    'cells', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('animal_id', Integer, nullable=False, index=True),
    Column('context_id', Integer, nullable=False, index=True),
    Column('name', String(255), nullable=False),
    Column('engram', Boolean, default=False),
    Column('engram_id', Integer, nullable=True, default=None)
)
Table(
    'fluorescences', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('cell_id', Integer, nullable=False, index=True),
    Column('value', Float, nullable=False),
    Column('diff_time', Float, nullable=False),
    Column('time', Float, nullable=False)
)

meta.create_all()
