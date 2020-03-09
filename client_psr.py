from flask_restful import Resource
import mysql.connector as sql
import credentials
from flask_restful import reqparse


class client_psr(Resource):
    def format(self,data):
        formatted_data = {}
        for idx, val in enumerate(data):
            formatted_data[val[0]] = [val[1],val[2]]
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
        stmt = "SELECT m.Group_Name, m.PERC_TOTAL_PSR_PHONE, p.INITIAL_POD FROM (SELECT Group_Name, sum(PERC_TOTAL_PSR_PHONE) PERC_TOTAL_PSR_PHONE FROM quantum.model_output_data GROUP BY Group_Name) m INNER JOIN quantum.pods_clients_map p WHERE m.Group_Name = p.Group_Name;"
        cursor.execute(stmt)
        result = cursor.fetchall()
        conn.close()

        #return self.format(result)
        return self.format(result)
