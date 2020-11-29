from flask import Flask
from flask_restful import Resource, Api
import repos.country_repo as repo

app = Flask(__name__)
api = Api(app)


class Countries(Resource):
    @staticmethod
    def get():
        countries = repo.get_all_countries()
        return repr(countries), 200


api.add_resource(Countries, '/')

if __name__ == '__main__':
    app.run(debug=True)
