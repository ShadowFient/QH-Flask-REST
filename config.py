from flask_restful import Resource
from flask_restful import reqparse
import mysql.connector as sql
import credentials
import json

from pod_to_clients import PodToClient


class Config(Resource):

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        parser.add_argument("config", required=True)
        parser.add_argument("exp_ratios", required=True)

        json_str = (parser.parse_args()["config"]).replace("\'", "\"")
        config = json.loads(json_str)
        name = (parser.parse_args()["name"]).replace("\'", "\"")
        json_str = (parser.parse_args()["exp_ratios"]).replace("\'", "\"")
        exp_ratios = json.loads(json_str)

        Config.insert_config(config, exp_ratios, name)

    @staticmethod
    def insert_config(config, exp_ratios, name):
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database='quantum')
        cursor = conn.cursor()
        save_config_stmt_format = ("insert into pods_clients_map"
                                   " (INITIAL_POD, Group_Name,"
                                   " GroupID, Config_Name)"
                                   " values (%s, %s, %s, %s)")
        save_exp_ratio_stmt_format = ("insert into pods"
                                      " (Config_Name, POD, EXP_RATIO,"
                                      " PSR_EXP_RATIO)"
                                      " values (%s, %s, %s, %s)")
        values = []
        exp_values = []
        for pod in config:
            for client in config[pod]:
                values.append((int(pod), client[1], client[0], name))
        for pod in exp_ratios:
            exp_values.append((name,
                               int(pod),
                               exp_ratios[pod]["EXP_RATIO"],
                               exp_ratios[pod]["PSR_EXP_RATIO"]))
        cursor.executemany(save_config_stmt_format, values)
        cursor.executemany(save_exp_ratio_stmt_format, exp_values)
        conn.commit()
        conn.close()

    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        name = (parser.parse_args()["name"]).replace("\'", "\"")
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        cursor = conn.cursor()
        stmt = "SELECT * FROM quantum.pods_clients_map where Config_Name='{}';"
        stmt1 = "select POD from pods where Config_Name='{}';" \
            .format(name)
        cursor.execute(stmt1)
        sz = len(cursor.fetchall())
        cursor.execute(stmt.format(name))
        result = cursor.fetchall()
        conn.close()
        return PodToClient.format_result(result, sz)

    @staticmethod
    def delete():
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        name = (parser.parse_args()["name"]).replace("\'", "\"")

        Config.delete_config(name)

    @staticmethod
    def delete_config(name):
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        cursor = conn.cursor()
        stmt = "delete from `pods_clients_map` where `Config_Name` = '{}';"
        cursor.execute(stmt.format(name))
        stmt = "delete from `pods` where `Config_Name` = '{}';"
        cursor.execute(stmt.format(name))
        conn.commit()
        conn.close()

    @staticmethod
    def put():
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        parser.add_argument("config", required=True)
        parser.add_argument("exp_ratios", required=True)

        json_str = (parser.parse_args()["config"]).replace("\'", "\"")
        config = json.loads(json_str)
        name = (parser.parse_args()["name"]).replace("\'", "\"")
        json_str = (parser.parse_args()["exp_ratios"]).replace("\'", "\"")
        exp_ratios = json.loads(json_str)

        Config.delete_config(name)
        Config.insert_config(config, exp_ratios, name)


class CurrentConfigs(Resource):

    @staticmethod
    def get():
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database='quantum')
        cursor = conn.cursor()
        stmt = "select distinct Config_Name from pods_clients_map"
        cursor.execute(stmt)
        results = cursor.fetchall()
        configs = []
        for config in results:
            configs.append(config[0])
        return configs
