from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from workload import Workload
from activity import Activity
from pod_to_clients import PodToClient
from config import Config, CurrentConfigs
from psr import PSR
import fetch_data

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

api.add_resource(fetch_data.FetchData, '/fetch_data')
api.add_resource(Workload, '/workload')
api.add_resource(Activity, "/activity")
api.add_resource(PodToClient, '/pod_to_clients')
api.add_resource(Config, '/config')
api.add_resource(CurrentConfigs, '/current_configs')
api.add_resource(PSR, '/psr')

if __name__ == '__main__':
    app.run(debug=True)
