from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from workload import Workload
import fetch_data

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

api.add_resource(fetch_data.FetchData, '/fetch_data')
api.add_resource(Workload, '/workload')

if __name__ == '__main__':
    app.run(debug=True)
