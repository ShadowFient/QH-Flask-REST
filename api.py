from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
import mysql.connector as sql
import credentials
import experience_ratio
import fetch_data

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

# api.add_resource(experience_ratio.ExperienceRatio, '/experience_ratio')
api.add_resource(fetch_data.FetchData, '/fetch_data')


if __name__ == '__main__':
    app.run(debug=True)
