from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models.country_model as model

engine = create_engine('mysql+mysqlconnector://root@localhost/states-of-the-world')
session = sessionmaker(bind=engine)()


def get_all_countries():
    return session.query(model.Country).all()


def insert_country(country):
    session.add(country)
    session.commit()