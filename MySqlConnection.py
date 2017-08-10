import MySQLdb


class MysqlConnections:
    def __init__(self):
        self.db = MySQLdb.Connection('localhost', 'root', '123456.qaz', 'NetEasyMusicCommit', charset='utf8')
        self.cursor = self.db.cursor()

    def insert_info(self, music_id, comments):
        # encode_comments = comments.decode('utf-8').encode('gb2312')
        sql_sta = "insert INTO commit VALUES ('%s', '%s')" % (music_id, comments)
        self.execute_statement(sql_sta)

    def execute_statement(self, sql):
        print sql
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print e
            self.db.rollback()