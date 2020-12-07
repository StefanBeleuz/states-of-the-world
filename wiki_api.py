from flask import Flask, jsonify, request, abort
import repos.country_repo as repo

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def get_json(countries):
    return jsonify([c.to_json() for c in countries])


@app.route('/')
def get_all_countries():
    countries = repo.get_all_countries()
    return get_json(countries)


@app.route('/top-<int:limit>-countries-<field>')
@app.route('/top-<int:limit>-countries-<field>-<order>')
def get_top_countries(limit, field, order='desc'):
    countries = repo.get_top_countries(limit, field, order)
    if countries is None:
        return abort(404)
    return get_json(countries)


@app.route('/filter-countries')
def get_filtered_countries():
    # accept gt, lt: population=gt-100000
    countries = repo.get_filtered_countries(request.args)
    if countries is None:
        return abort(404)
    return get_json(countries)


if __name__ == '__main__':
    app.run(debug=True)
