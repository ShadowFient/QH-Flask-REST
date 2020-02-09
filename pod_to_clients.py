from flask_restful import Resource
import mysql.connector as sql
import credentials


class PodToClient(Resource):

    # from pods 1 to 27, some numbers may be excluded - should i account for
    # this?
    # format = {pod#:[clients]}
    # index 0 = pod, index 2 = client
    @staticmethod
    def format(res):
        keys = list(range(1, 25))
        pcm = {key: [] for key in keys}
        for li in res:
            pcm[li[0]].append(li[2])
        return pcm

    def get(self):
        conn = sql.connect(host=credentials.HOST,
                           user=credentials.USER,
                           passwd=credentials.PASSWD,
                           database="quantum")
        cursor = conn.cursor()
        stmt = "SELECT * FROM quantum.pods_clients_map;"
        cursor.execute(stmt)
        result = cursor.fetchall()
        conn.close()
        return self.format(result)
