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

    def to_json(self):
        return {
            'name': self.name, 'capital': self.capital, 'population': self.population, 'density': self.density,
            'area': self.area, 'neighbours': self.neighbours, 'language': self.language, 'time_zone': self.time_zone,
            'government': self.government
        }
