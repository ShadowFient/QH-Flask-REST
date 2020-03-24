from flask_restful import Resource
import mysql.connector as sql
import credentials
from flask_restful import reqparse


class ClientPSR(Resource):

    @staticmethod
    def format(data):
        formatted_data = {}
        for idx, val in enumerate(data):
            formatted_data[val[0]] = [val[1],val[2]]
        return formatted_data

    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument("config_name", default="Initial Config")
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        cursor = conn.cursor()
        stmt = ("SELECT m.Group_Name, m.PRED_PHONE_VOLUME, m.PERC_TOTAL_PSR_PHONE"
                " FROM"
                " (SELECT Group_Name, sum(PRED_PHONE_VOLUME) PRED_PHONE_VOLUME, sum(PERC_TOTAL_PSR_PHONE) PERC_TOTAL_PSR_PHONE"
                " FROM quantum.model_output_data GROUP BY Group_Name) m"
                " INNER JOIN quantum.pods_clients_map p WHERE m.Group_Name = p.Group_Name;")
        cursor.execute(stmt)
        result = cursor.fetchall()
        conn.close()

        return ClientPSR.format(result)
