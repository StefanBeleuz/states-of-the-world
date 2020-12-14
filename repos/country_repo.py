"""This module is responsible for inserting and getting data from database.

It uses SQLAlchemy as on ORM.
"""

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from models.country_model import Country

engine = create_engine('mysql+mysqlconnector://root@localhost/states-of-the-world')
session = sessionmaker(bind=engine)()


def get_all_countries():
    """Returns all countries stored in the database.

    Returns
    -------
    list
        a list of all countries in the database
    """
    return session.query(Country).all()


def get_top_countries(limit, field, order):
    """Returns first countries from database sorted by field in a specific order.

    Parameters
    ----------
    limit : int
        the number of countries returned.
    field: str
        the attribute of the Country to filter countries by.
    order: str
        specify the order in which the countries are sorted.
        If order is 'asc' then countries are listed ascending, else countries are listed descending.

    Returns
    -------
    list
        a list of countries based on the passed in parameters.
    None
        if an unknown Country attribute is passed in as a parameter.
    """
    try:
        attr = getattr(Country, field)
        if order == 'asc':
            return session.query(Country).filter(attr.isnot(None)).order_by(attr).limit(limit).all()
        else:
            return session.query(Country).filter(attr.isnot(None)).order_by(attr.desc()).limit(limit).all()
    except AttributeError:
        return None


def get_filtered_countries(dict_filters):
    """Returns countries from database filtered by a number of filters.

    Parameters
    ----------
    dict_filters : dict
        the filters to be applied.
        key   = Country attribute
        value = filter value

    Returns
    -------
    list
        a list of filtered countries based on the passed in parameters.
    None
        if an unknown Country attribute is passed.
    """
    try:
        filters = []
        for key, value in dict_filters.items():
            if key == 'language' or key == 'government' or key == 'time_zone' or key == 'neighbours':
                if key == 'time_zone' and value == 'UTC':
                    filters.append(or_(getattr(Country, key) == 'UTC', getattr(Country, key).like('UTC+0')))
                else:
                    filters.append(getattr(Country, key).like('%{}%'.format(value)))
            else:
                op = 'eq'
                if value[2] == '-':
                    op, value = value.split('-')
                if op == 'gt':
                    filters.append(getattr(Country, key) > value)
                elif op == 'lt':
                    filters.append(getattr(Country, key) < value)
                else:
                    filters.append(getattr(Country, key) == value)
        return session.query(Country).filter(*filters)
    except AttributeError:
        return None


def insert_countries(countries):
    """Inserts a list of countries into database.

    Parameters
    ----------
    countries : list
        the list of countries to be stored into database.
    """
    print('Inserting countries into database...')
    session.add_all(countries)
    session.commit()
    print('Done!')
