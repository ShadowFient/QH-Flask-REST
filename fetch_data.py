from flask_restful import Resource
import mysql.connector as sql
import credentials


class FetchData(Resource):

    @staticmethod
    def get():
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        cursor = conn.cursor()
        stmt = "select POD, EXP_RATIO from pods"
        cursor.execute(stmt)
        result = cursor.fetchall()
        conn.close()
        return {'data': result}
