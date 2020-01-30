from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
import mysql.connector as sql
import credentials

app = Flask(__name__)
api = Api(app)
cors = CORS(app)


class HelloWorld(Resource):

    def get(self):
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        cursor = conn.cursor()
        stmt = "select msg from test where msg_id=1;"
        cursor.execute(stmt)
        result = cursor.fetchone()
        conn.close()
        return {'hello': result}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
