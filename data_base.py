import sqlite3
from sqlite3 import Error


class DataBase:
    def __init__(self):
        self.conn = None
        self.cur = None

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as ex:
            print(ex)

    def execute(self, sql):
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql)
            self.conn.commit()
        except Error as ex:
            print(ex)

    def execute_with_args(self, sql, args):
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, args)
            self.conn.commit()
        except Error as ex:
            print(ex)

    def get_with_args(self, sql, args, first=False):
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, args)
            self.conn.commit()
            rv = self.cur.fetchall()
            self.cur.close()
            return (rv[0] if rv else None) if first else rv
        except Error as ex:
            print(ex)

    def drop_table(self, table):
        sql = 'DROP TABLE IF EXISTS ' + table + ';'
        self.execute(sql)

    def create_table(self, table, table_spec):
        sql = 'CREATE TABLE IF NOT EXISTS ' + table + '(' + table_spec + ');'
        self.execute(sql)

    def select_count(self, table):
        sql = 'SELECT COUNT(*) FROM ' + table + ';'
        self.execute(sql)
        return self.cur.fetchone()[0]

    def close_connection(self):
        try:
            if self.conn:
                self.conn.close()
        except Error as ex:
            print(ex)
