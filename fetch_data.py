from flask_restful import Resource
import mysql.connector as sql
import credentials
import pandas as pd


class FetchData(Resource):

    @staticmethod
    def get():
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        stmt = "select POD, EXP_RATIO from pods"
        result = pd.read_sql(stmt, conn)
        result.set_index("POD", inplace=True)
        conn.close()
        return result.to_dict(orient="index")
