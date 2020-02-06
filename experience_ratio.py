from flask_restful import Resource, reqparse
import mysql.connector as sql
import pandas as pd
import credentials

class ExperienceRatio(Resource):

    @staticmethod
    def get():
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        cursor = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument('pod')
        args = parser.parse_args()
        print(args)
        pod_id = args["pod"]
        stmt = "select EXP_RATIO from pods where POD = " + pod_id
        cursor.execute(stmt)
        result = cursor.fetchone()
        conn.close()
        return {'experience_ratio': result}

