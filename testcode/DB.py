import MySQLdb

__author__ = 'leo'


class DB:
    conn = None
    cursor = None

    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db


    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pwd, db=self.db, port=3306,
                                    charset='utf8')

    def execute(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
        return cursor

    def close(self):
        if (self.cursor):
            self.cursor.close()
        self.conn.commit()
        self.conn.close()