from flask_restful import Resource, reqparse
import mysql.connector as sql
import credentials
import pandas as pd


class Activity(Resource):

    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument("name", default="Initial Config")
        config_name = parser.parse_args()["name"].replace("\'", "\"")

        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")

        pods_query = "select POD from pods"
        activity_query = "select `INITIAL_POD`, output.`GroupID`," \
                         " output.Group_Name, Month, " \
                         " PCGPDC_TIME_HOURS_SUCC," \
                         " PCGPDC_TIME_HOURS_UNSUCC, " \
                         " PCGPAC_TIME_HOURS_SUCC," \
                         " PCGPAC_TIME_HOURS_UNSUCC, " \
                         " PCGFLLUP_TIME_HOURS_SUCC," \
                         " PCGFLLUP_TIME_HOURS_UNSUCC, " \
                         " PCGNEWALERT_TIME_HOURS_SUCC," \
                         " PCGNEWALERT_TIME_HOURS_UNSUCC, " \
                         " PCGREF_TIME_HOURS_SUCC," \
                         " PCGREF_TIME_HOURS_UNSUCC, " \
                         " PCGTERM_TIME_HOURS_SUCC," \
                         " PCGTERM_TIME_HOURS_UNSUCC, " \
                         " PCGEMPGRP_TIME_HOURS_SUCC," \
                         " PCGEMPGRP_TIME_HOURS_UNSUCC," \
                         " PSR_PHONE_ACTS_LIKE_MEM, " \
                         " PCG_FOLLOWUP_ACTS_LIKE, " \
                         " PCG_NEWALERT_ACTS_LIKE, " \
                         " PCG_PAC_ACTS_LIKE, " \
                         " PCG_PDC_ACTS_LIKE, " \
                         " PCG_REF_ACTS_LIKE, " \
                         " PCG_TERM_ACTS_LIKE, " \
                         " PCG_EMPGRP_ACTS_LIKE, " \
                         " Members" \
                         " from `pods_clients_map` map" \
                         " inner join `model_output_data` output" \
                         " on map.`GroupID` = output.`GroupID`" \
                         " where map.`INITIAL_POD` = {}" \
                         " and map.`Config_Name` = '{}';"

        pods_df: pd.DataFrame = pd.read_sql(pods_query, conn)
        pods_df = pods_df.drop_duplicates()

        activity_df: pd.DataFrame = pd.DataFrame()

        for row in pods_df.itertuples():
            each_df = pd.read_sql(activity_query.format(row.POD, config_name),
                                  conn)
            each_df["INITIAL_POD"] = row.POD
            activity_df = activity_df.append(each_df, ignore_index=True)

        conn.close()

        return activity_df.to_dict('records')