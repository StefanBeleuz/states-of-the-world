"""This module is responsible for modeling a Country from a SQL object to a Python object.

It uses SQLAlchemy as on ORM.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String

Base = declarative_base()


class Country(Base):
    """
    A class used to represent a Country, modeled from database

    Attributes
    ----------
    id : int
        un unique id having the role of primary key in database
    name : str
        the name of the country
    capital: str
        the capital of the country
    population: int
        the population of the country
    density: float
        the density of the country
    area: float
        the area of the country
    neighbours: str
        the neighbours of the country, separated by comma
    language: str
        the official languages of the country, separated by comma if there are more
    time_zone: str
        the time zone of the country
    government: str
        the government of the country

    Methods
    -------
    to_json()
        Returns the Country's attributes stored in a dictionary
    """

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

    def __init__(self, name, capital, population, density, area, neighbours, language, time_zone, government):
        self.name = name
        self.capital = capital
        self.population = population
        self.density = density
        self.area = area
        self.neighbours = neighbours
        self.language = language
        self.time_zone = time_zone
        self.government = government

    def to_json(self):
        """ Returns the Country's attributes stored in a dictionary """
        return {
            'name': self.name, 'capital': self.capital, 'population': self.population, 'density': self.density,
            'area': self.area, 'neighbours': self.neighbours, 'language': self.language, 'time_zone': self.time_zone,
            'government': self.government
        }
