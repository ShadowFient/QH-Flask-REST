from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
import mysql.connector as sql

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

with open("dbcredential") as db_file:
    ip = db_file.readline().strip()
    password = db_file.readline()

db = sql.connect(host=ip,
                 user="hyyyy",
                 passwd=password,
                 database="quantum")


class HelloWorld(Resource):

    def get(self):
        cursor = db.cursor()
        stmt = "select msg from test where msg_id=1;"
        cursor.execute(stmt)
        result = cursor.fetchone()
        return {'hello': result}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
