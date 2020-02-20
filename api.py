from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from psr import PSR

app = Flask(__name__)
api = Api(app)
cors = CORS(app)


api.add_resource(PSR, '/psr')


if __name__ == '__main__':
    app.run(debug=True)
