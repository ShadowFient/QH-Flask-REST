from flask_restful import Resource, reqparse
import pandas as pd
import mysql.connector as sql
import credentials


class PSR(Resource):
    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument("name", default="Initial Config")
        config_name = parser.parse_args()["name"].replace("\'", "\"")
        # connect to the database
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database='quantum',
                           port=3306)

        pods_stmt = "select POD from pods where Config_Name = '{}'"
        psr_stmt = "select INITIAL_POD, output.GroupID," \
                   "PERC_TOTAL_PSR_PHONE," \
                   "PRED_PHONE_VOLUME," \
                   "SUCC_TIME_PSR_PHONE," \
                   "PSR_PHONE_ACTS_LIKE_MEM " \
                   "from pods_clients_map map " \
                   "inner join model_output_data output " \
                   "on map.GroupID = output.GroupID " \
                   "where map.INITIAL_POD = {} " \
                   "and map.Config_Name = '{}';"

        pods_df: pd.DataFrame = pd.read_sql(pods_stmt.format(config_name), conn)
        psr_df: pd.DataFrame = pd.DataFrame()

        for row in pods_df.itertuples():
            each = pd.read_sql(psr_stmt.format(row.POD, config_name), conn)
            each["Total_PSR_Phone_Call_Hours"] = \
                each["PRED_PHONE_VOLUME"] * each["SUCC_TIME_PSR_PHONE"]/60
            each_psr: pd.Series = each.sum(axis=0)
            each_psr["INITIAL_POD"] = row.POD
            each_psr.drop("GroupID", inplace=True)
            psr_df = psr_df.append(each_psr, ignore_index=True)

        conn.close()
        psr_df.set_index("INITIAL_POD", inplace=True)
        return psr_df.to_dict(orient="index")
