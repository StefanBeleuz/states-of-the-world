"""This module is responsible for creating a REST API for having access to database.

It uses Flask for creating a web server.
"""

from flask import Flask, jsonify, request, abort
import repos.country_repo as repo

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def get_json(countries):
    """ Return a JSON of a list of Country object that were also converted to JSON.

    Parameters
    ----------
    countries : list
        the list of countries to be converted to JSON.

    Returns
    -------
    dict
        a JSON formatted list of countries.
    """
    return jsonify([c.to_json() for c in countries])


@app.route('/')
def get_all_countries():
    """ Return a JSON containing all countries from database.

    Returns
    -------
    dict
        a JSON formatted list of countries.
    """
    countries = repo.get_all_countries()
    return get_json(countries), 200


@app.route('/top-<int:limit>-countries-<field>')
@app.route('/top-<int:limit>-countries-<field>-<order>')
def get_top_countries(limit, field, order='desc'):
    """ Return a JSON containing a top of countries from database, based on the specified filed and order.

    Parameters
    ----------
    limit: int
        the number of countries in top.
    field: str
        the Country attribute to be compared in top.
    order: str
        the order in which the top to be displayed (by default is descending).

    Returns
    -------
    dict
        a JSON formatted list of countries.
    error code 404
        if passed field is an unknown attribute of Country.
    """
    countries = repo.get_top_countries(limit, field, order)
    if countries is None:
        return abort(404)
    return get_json(countries)


@app.route('/filter-countries')
def get_filtered_countries():
    """ Return a JSON containing a list of countries from database, filtered by a set of rules.
    The rules are passed in the query string
    and accept one of the following comparators: eq, gt, lt (eq is the default).
    ex: /filter-countries?population=lt-20000 will return the countries with population less than 20000.

    Returns
    -------
    dict
        a JSON formatted list of countries.
    error code 404
        if one of the passed fields is an unknown attribute of Country.
    """
    countries = repo.get_filtered_countries(request.args)
    if countries is None:
        return abort(404)
    return get_json(countries)


if __name__ == '__main__':
    app.run(debug=True)
