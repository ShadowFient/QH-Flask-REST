from flask_restful import Resource, reqparse
import mysql.connector as sql
import credentials
import pandas as pd


class FetchData(Resource):

    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument("name", default="Initial Config")
        config_name = parser.parse_args()["name"].replace("\'", "\"")
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        stmt = "select POD, EXP_RATIO, PSR_EXP_RATIO from pods" \
               " where Config_Name='{}'"\
            .format(config_name)
        result = pd.read_sql(stmt, conn)
        result.set_index("POD", inplace=True)
        conn.close()
        return result.to_dict(orient="index")
