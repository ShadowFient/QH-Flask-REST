from flask_restful import Resource
import mysql.connector as sql
import credentials


class Activity(Resource):

    @staticmethod
    def get():
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        cursor = conn.cursor()
        stmt = ("select GroupID, Group_Name, Month, PCGPDC_TIME_HOURS_SUCC,"
                " PCGPDC_TIME_HOURS_UNSUCC, PCGPAC_TIME_HOURS_SUCC,"
                " PCGPAC_TIME_HOURS_UNSUCC, PCGFLLUP_TIME_HOURS_SUCC,"
                " PCGFLLUP_TIME_HOURS_UNSUCC, PCGNEWALERT_TIME_HOURS_SUCC,"
                " PCGNEWALERT_TIME_HOURS_UNSUCC, PCGREF_TIME_HOURS_SUCC,"
                " PCGREF_TIME_HOURS_UNSUCC, PCGTERM_TIME_HOURS_SUCC,"
                " PCGTERM_TIME_HOURS_UNSUCC, PCGEMPGRP_TIME_HOURS_SUCC,"
                " PCGEMPGRP_TIME_HOURS_UNSUCC from model_output_data ;")
        stmt1 = "select INITIAL_POD, GroupID from pods_clients_map;"

        # get POD and Group ID
        cursor.execute(stmt1)
        pod = cursor.fetchall()
        group = {}
        num0 = cursor.rowcount
        # match POD and Group ID
        for i in range(0, num0):
            group[pod[i][1]] = pod[i][0]

        # get data
        cursor.execute(stmt)
        data = cursor.fetchall()
        num = cursor.rowcount
        result_list = []
        cmp = ["POD","GroupID", "Group_Name", "Month", "PCGPDC_TIME_HOURS_SUCC",
               "PCGPDC_TIME_HOURS_UNSUCC", "PCGPAC_TIME_HOURS_SUCC",
               "PCGPAC_TIME_HOURS_UNSUCC", "PCGFLLUP_TIME_HOURS_SUCC",
               "PCGFLLUP_TIME_HOURS_UNSUCC",
               "PCGNEWALERT_TIME_HOURS_SUCC", "PCGNEWALERT_TIME_HOURS_UNSUCC",
               "PCGREF_TIME_HOURS_SUCC",
               "PCGREF_TIME_HOURS_UNSUCC", "PCGTERM_TIME_HOURS_SUCC",
               "PCGTERM_TIME_HOURS_UNSUCC",
               "PCGEMPGRP_TIME_HOURS_SUCC", "PCGEMPGRP_TIME_HOURS_UNSUCC"]
        for i in range(0, num):
            result = {}
            for j in range(0, len(cmp)):
                if j == 0:
                    result[cmp[j]] = group[data[i][j]]
                    j = j+1
                result[cmp[j]] = data[i][j-1]
            result_list.append(result)
        conn.close()

        return result_list
