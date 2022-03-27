import sqlite3
from sqlite3 import Error


class DataBase:
    def __init__(self):
        self.conn = None
        self.cur = None

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
        except Error as ex:
            print(ex)

    def execute(self, sql):
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql)
            self.conn.commit()
        except Error as ex:
            print(ex)

    def execute_with_parameters(self, sql, parameters):
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, parameters)
            self.conn.commit()
        except Error as ex:
            print(ex)

    def get(self, sql, first=False):
        try:
            self.execute(sql)
            rv = self.cur.fetchall()
            self.cur.close()
            return (rv[0] if rv else None) if first else rv
        except Error as ex:
            print(ex)

    def get_with_parameters(self, sql, parameters, first=False):
        try:
            self.execute_with_parameters(sql, parameters)
            rv = self.cur.fetchall()
            self.cur.close()
            return (rv[0] if rv else None) if first else rv
        except Error as ex:
            print(ex)

    def drop_table(self, table):
        sql = 'DROP TABLE IF EXISTS %s;' % table
        self.execute(sql)

    def create_table(self, table, parameters):
        sql = 'CREATE TABLE IF NOT EXISTS %s (%s);' % (table, parameters)
        self.execute(sql)

    def select_count(self, table):
        sql = 'SELECT COUNT(*) FROM %s;' % table
        self.execute(sql)
        return self.cur.fetchone()[0]

    def select_distinct(self, column, table):
        sql = 'SELECT DISTINCT %s FROM %s;' % (column, table)
        return self.get(sql, False)

    def reset_int_column(self, table, column, value):
        sql = 'UPDATE %s SET %s = %s;' % (table, column, str(value))
        self.execute(sql)

    def close_connection(self):
        try:
            if self.conn:
                self.conn.close()
        except Error as ex:
            print(ex)
