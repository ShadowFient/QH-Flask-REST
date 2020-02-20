from flask_restful import Resource
import pandas as pd
import mysql.connector as sql
import credentials


class PSR(Resource):
    @staticmethod
    def get():
        # connect to the database
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database='quantum',
                           port=3306)

