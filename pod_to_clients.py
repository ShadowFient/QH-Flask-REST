from flask_restful import Resource
import mysql.connector as sql
import credentials
from flask_restful import reqparse


class PodToClient(Resource):

    # from pods 1 to 27, some numbers may be excluded - should i account for
    # this?
    # format = {pod#:[clients]}
    # index 0 = pod, index 2 = client
    @staticmethod
    def format_result(res,sz):
        keys = list(range(1, sz+1))
        pcm = {key: [] for key in keys}
        for li in res:
            pcm[li[0]].append([li[2], li[1]])   # [group_id, group_name]
        return pcm

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", default="Initial Config")
        config_name = parser.parse_args()["name"].replace("\'", "\"")
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        cursor = conn.cursor()
        stmt = "SELECT * FROM quantum.pods_clients_map where Config_Name='{}';"\
            .format(parser.parse_args()["name"])
        stmt1="select POD from pods where Config_Name='{}';"\
            .format(config_name)
        cursor.execute(stmt)
        result = cursor.fetchall()
        cursor.execute(stmt1)
        sz=len(cursor.fetchall())
        conn.close()
        return self.format_result(result, sz)
