from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String

Base = declarative_base()


class Country(Base):
    __tablename__ = 'countries'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    capital = Column('capital', String)
    population = Column('population', Integer)
    density = Column('density', Float)
    area = Column('area', Float)
    neighbours = Column('neighbours', String)
    language = Column('language', String)
    time_zone = Column('time_zone', String)
    government = Column('government', String)

    def __repr__(self):
        return self.name
