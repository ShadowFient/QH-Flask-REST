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
        member_query = "select INITIAL_POD, output.Group_Name, Members " \
                       "from pods_clients_map map " \
                       "inner join model_output_data output " \
                       "on map.Group_Name = output.Group_Name " \
                       "where map.INITIAL_POD = {} " \
                       "and map.Config_Name='{}';"
        pods_df: pd.DataFrame = pd.read_sql(pods_query, conn)
        pods_df = pods_df.drop_duplicates()

        member_df: pd.DataFrame = pd.DataFrame()
        for row in pods_df.itertuples():
            each_df = pd.read_sql(member_query.format(row.POD, config_name),
                                  conn)
            each_df = each_df.drop_duplicates()
            each_df["POD"] = row.POD
            member_df = member_df.append(each_df, ignore_index=True)

        conn.close()

        # return member_df.to_dict('record')
        table = member_df.pivot_table(index="INITIAL_POD", columns="Group_Name",
                                      values="Members", aggfunc='first')

        res = table.to_dict(orient="index")

        for pod, client in list(res.items()):
            client_total = 0
            for key, value in list(client.items()):
                if value != value:
                    del res[pod][key]
                else:
                    client_total = client_total + int(value)
            res[pod]["Total"] = client_total

        return res

