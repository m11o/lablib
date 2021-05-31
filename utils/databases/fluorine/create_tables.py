import sys
import pathlib
current_directory = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_directory) + '/../../../')

from sqlalchemy import Column, Integer, String, Boolean, Float, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from utils.databases.fluorine.settings import DATABASE_URL, ENGINE

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class Experiment(Base):
    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, unique=True)

    animals = relationship('Animal', backref='experiments')
    contexts = relationship('Context', backref='experiments')

    def __repr__(self):
        return "<Experiment(id = %d, name = '%s')>" % (self.id, self.name)

    @classmethod
    def find_or_create_by(cls, name):
        with Session(ENGINE) as session:
            experiment = session.query(Experiment).filter(Experiment.name == name).first()
            if experiment is None:
                print('ok')
                experiment = Experiment()
                experiment.name = name
                session.add(experiment)
                session.commit()

                session.refresh(experiment)

            return experiment


class Animal(Base):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    experiment_id = Column(Integer, ForeignKey('experiments.id'), nullable=False, index=True)
    identification = Column(String(255), nullable=False, index=True, unique=True)

    cells = relationship('Cell', backref='animals')

    def __repr__(self):
        return "<Animal(id = %d, experiment_id = %d, identification = '%s')>" % (self.id, self.experiment_id, self.identification)

    @classmethod
    def find_or_create_by(cls, experiment_id, identification):
        with Session(ENGINE) as session:
            animal = session.query(Animal).filter(Animal.identification == identification, Animal.experiment_id == experiment_id).first()
            if animal is None:
                animal = Animal()
                animal.experiment_id = experiment_id
                animal.identification = identification
                session.add(animal)
                session.commit()

                session.refresh(animal)

            return animal


class Context(Base):
    __tablename__ = 'contexts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    experiment_id = Column(Integer, ForeignKey('experiments.id'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    sort_index = Column(Integer, default=0)

    fluorescences = relationship('Fluorescence', backref='contexts')

    def __repr__(self):
        return "<Context(id = %d, experiment_id = %d, name = '%s')>" % (self.id, self.experiment_id, self.name)

    @classmethod
    def find_or_create_by(cls, experiment_id, name):
        with Session(ENGINE) as session:
            context = session.query(Context).filter(Context.experiment_id == experiment_id, Context.name == name).first()
            if context is None:
                context = Context()
                context.experiment_id = experiment_id
                context.name = name
                session.add(context)
                session.commit()

                session.refresh(context)

            return context


class Cell(Base):
    __tablename__ = 'cells'

    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey('animals.id'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    engram = Column(Boolean, default=False)
    engram_id = Column(Integer, nullable=True, default=None)

    fluorescences = relationship('Fluorescence', backref='cells')

    def __repr__(self):
        return "<Cell(id = %d, animal_id = %d, name = '%s', engram = %s)>" % (self.id, self.animal_id, self.name, self.engram)

    @classmethod
    def find_or_create_by(cls, animal_id, cell_name, engram):
        with Session(ENGINE) as session:
            cell = session.query(Cell).filter(Cell.animal_id == animal_id, Cell.name == cell_name).first()
            if cell is None:
                cell = Cell()
                cell.animal_id = animal_id
                cell.name = cell_name
                cell.engram = engram != '#N/A'
                cell.engram_id = engram if cell.engram else None
                session.add(cell)
                session.commit()


class Fluorescence(Base):
    __tablename__ = 'fluorescences'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cell_id = Column(Integer, ForeignKey('cells.id'), nullable=False, index=True)
    context_id = Column(Integer, ForeignKey('contexts.id'), nullable=False, index=True)
    value = Column(Float, nullable=False)
    diff_time = Column(Float, nullable=False)
    time = Column(Float, nullable=False)

    def __repr__(self):
        return "<Fluorescence(id = %d, cell_id = %d, value = %f, diff_time = %f, time = %f)>" % (self.id, self.cell_id, self.value, self.diff_time, self.time)


Base.metadata.create_all(engine)
