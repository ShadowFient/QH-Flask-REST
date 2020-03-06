from flask_restful import Resource
import mysql.connector as sql
import credentials
from flask_restful import reqparse


class client_psr(Resource):
    def format(self,data):
        formatted_data = []
        for idx, val in enumerate(data):
            formatted_data.append({val[0]:val[1]})
        return formatted_data

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("config_name", default="Initial Config")
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        cursor = conn.cursor()
        #NEEDS TO BE CHANGED
        stmt = "SELECT Group_Name,sum(PERC_TOTAL_PSR_PHONE) AS total_psr FROM quantum.model_output_data GROUP BY Group_Name"
        cursor.execute(stmt)
        result = cursor.fetchall()
        conn.close()

        #return self.format(result)
        return self.format(result)
