from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.country_model import Country

engine = create_engine('mysql+mysqlconnector://root@localhost/states-of-the-world')
session = sessionmaker(bind=engine)()


def get_all_countries():
    return session.query(Country).all()


def get_top_countries(limit, field, order):
    try:
        if order == 'asc':
            return session.query(Country).order_by(getattr(Country, field)).limit(limit).all()
        else:
            return session.query(Country).order_by(getattr(Country, field).desc()).limit(limit).all()
    except AttributeError:
        return None


def get_filtered_countries(dict_filters):
    try:
        filters = []
        for key, value in dict_filters.items():
            if key == 'language' or key == 'government':
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
    print('Inserting countries into database...')
    session.add_all(countries)
    session.commit()
    print('Done!')
