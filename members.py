from flask_restful import Resource, reqparse
import mysql.connector as sql
import credentials
import pandas as pd


class Members(Resource):

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
        member_query = "select INITIAL_POD, output.GroupID, Members " \
                       "from pods_clients_map map " \
                       "inner join model_output_data output " \
                       "on map.GroupID = output.GroupID " \
                       "where map.INITIAL_POD = {} " \
                       "and map.Config_Name='{}';"
        pods_df: pd.DataFrame = pd.read_sql(pods_query, conn)
        pods_df = pods_df.drop_duplicates()

        member_df: pd.DataFrame = pd.DataFrame()
        for row in pods_df.itertuples():
            each_df = pd.read_sql(member_query.format(row.POD, config_name),
                                  conn)
            each_df = each_df.drop_duplicates();
            each_df["POD"]=row.POD
            member_df = member_df.append(each_df, ignore_index=True)

        conn.close()

        # return member_df.to_dict('record')
        table=member_df.pivot_table(index="INITIAL_POD",columns="GroupID",values="Members",aggfunc='first')

        res=table.to_dict(orient="index")

        for pod, client in list(res.items()):
            clientTotal=0;
            for key, value in list(client.items()):
                if(value != value):
                    del res[pod][key]
                else:
                    clientTotal = clientTotal + int(value)
            res[pod]["Total"]=clientTotal

        return res
        # return result.to_json(orient="index")

        # pods_query = "select POD from pods "
        # member_query = "select `INITIAL_POD`, " \
        #                  " output.GroupID, " \
        #                  " PCG_FOLLOWUP_ACTS_LIKE, " \
        #                  " PCG_NEWALERT_ACTS_LIKE, " \
        #                  " PCG_PAC_ACTS_LIKE, " \
        #                  " PCG_PDC_ACTS_LIKE, " \
        #                  " PCG_REF_ACTS_LIKE, " \
        #                  " PCG_TERM_ACTS_LIKE," \
        #                  " PCG_EMPGRP_ACTS_LIKE," \
        #                  " PSR_PHONE_ACTS_LIKE_MEM" \
        #                  " from `pods_clients_map` map" \
        #                  " inner join `model_output_data` output" \
        #                  " on map.`GroupID` = output.`GroupID`" \
        #                  " where map.`INITIAL_POD` = {}" \
        #                  " and map.`Config_Name` = '{}';"
        #
        # pods_df: pd.DataFrame = pd.read_sql(pods_query, conn)
        # pods_df = pods_df.drop_duplicates()
        #
        # member_df: pd.DataFrame = pd.DataFrame()
        #
        # for row in pods_df.itertuples():
        #     each_df = pd.read_sql(member_query.format(row.POD, config_name),
        #                           conn)
        #     each_mem: pd.Series = each_df.sum(axis=0)
        #     each_mem.drop("INITIAL_POD", inplace=True)
        #     each_mem.drop("GroupID", inplace=True)
        #     each_mem["Total"]=each_mem.sum()
        #     each_mem["Total_PCG"]=each_mem["Total"]-each_mem["PSR_PHONE_ACTS_LIKE_MEM"]
        #     each_mem["INITIAL_POD"] = row.POD
        #     member_df = member_df.append(each_mem, ignore_index=True)
        #
        # conn.close()
        # member_df.set_index("INITIAL_POD", inplace=True)
        # return member_df.to_dict(orient="index")