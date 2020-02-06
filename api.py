from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
import mysql.connector as sql
import credentials
import experience_ratio
import pod_ids

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

api.add_resource(experience_ratio.ExperienceRatio, '/experience_ratio')
api.add_resource(pod_ids.FetchPodIds, '/get_pod_ids')


if __name__ == '__main__':
    app.run(debug=True)
