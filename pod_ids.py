from flask_restful import Resource, reqparse
import mysql.connector as sql
import pandas as pd
import credentials

class FetchPodIds(Resource):

    @staticmethod
    def get():
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        cursor = conn.cursor()
        # parser = reqparse.RequestParser()
        # args = parser.parse_args()
        # print(args)
        # pod_id = args["pod"]
        stmt = "select POD from pods"
        cursor.execute(stmt)
        result = cursor.fetchall()
        conn.close()
        return {'ids': result}

