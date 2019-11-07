import logging
import MySQLdb

class Database:
    def __init__(self, host="localhost", user="root", password=None, db=None):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.conn = MySQLdb.connect(self.host, self.user, self.password, self.db)
        try:
            if (self.conn):
                status = "DB init success"
            else:
                status = "DB init failed"
            self.conn.autocommit(True)
            self.cursor = self.conn.cursor()
            logging.info("%s" % status)
        except Exception as e:
            status = "DB init fail %s " % str(e)
            logging.info("%s" % status)

    def reconnect(self):
        self.conn = MySQLdb.connect(self.host, self.user, self.password, self.db)
        try:
            if (self.conn):
                status = "DB reconnect success"
            else:
                status = "DB reconnect failed"
            self.conn.autocommit(True)
            self.cursor = self.conn.cursor()
            logging.info("%s" % status)
        except Exception as e:
            status = "DB reconnect fail %s " % str(e)
            logging.info("%s" % status)


    def insert(self, query):
        try:
            if self.conn is None:
                self.__init__()
            else:
                self.conn.ping(True)
                logging.info("%s" % query)
                self.cursor.execute(query)
        except MySQLdb.OperationalError:
            self.reconnect()
            logging.info("%s" % query)
            self.cursor.execute(query)
        except Exception as e:
            logging.exception("Insert Failed: %s" % e)
            self.conn.rollback()


    def query(self, query):
        try:
            if self.conn is None:
                self.__init__()
            else:
                self.conn.ping(True)
                self.cursor.execute(query)
        except MySQLdb.OperationalError:
            self.reconnect()
            logging.info("%s" % query)
            self.cursor.execute(query)
        except Exception as e:
            logging.exception("Query Failed: %s" % e)
            self.conn.rollback()
            return False

        return self.cursor.fetchall()


    def __del__(self):
        self.conn.close()

