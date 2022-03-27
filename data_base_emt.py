from data_base import DataBase
from sqlite3 import Error


class DataBaseEMT(DataBase):
    emt_db_filename = '../emt.db'

    def __init__(self, init=False):
        super().__init__()
        # create a database connection
        self.create_connection(self.emt_db_filename)
        if init:
            # if os.path.exists(self.emt_db_filename):
            #     os.remove(self.emt_db_filename)
            self.arrives_cont = 0
            self.init_data()
        else:
            self.arrives_cont = self.select_count('arrives')
            print(self.arrives_cont)

    def insert_into_arrives(self, values):
        sql = """
            INSERT INTO arrives(id, stop_id, line, position, estimateArrive) VALUES(?,?,?,?,?)
            """
        try:
            cur = self.conn.cursor()
            cur.execute(sql, values)
            self.conn.commit()

            return cur.lastrowid
        except Error as ex:
            print(ex)

    def update_arrive(self, arrive):
        sql = """
            UPDATE arrives SET estimateArrive = ? WHERE stop_id = ? AND line = ? AND position = ?
            """
        try:
            cur = self.conn.cursor()
            cur.execute(sql, arrive)
            self.conn.commit()
        except Error as ex:
            print(ex)

    def get_arrive(self, args):
        sql = """
            SELECT estimateArrive FROM arrives WHERE stop_id = ? AND line = ?
            """
        try:
            return self.get_with_args(sql, args, True)
        except Error as ex:
            print(ex)

    def get_arrives(self, args):
        sql = """
            SELECT estimateArrive FROM arrives WHERE stop_id = ? AND line = ?
            """
        try:
            return self.get_with_args(sql, args, True)
        except Error as ex:
            print(ex)

    def init_data(self):
        # create tables
        if self.conn is None:
            return

        table_specs = """
            id integer PRIMARY KEY,
            stop_id integer,
            line text,
            position integer,
            estimateArrive integer
            """
        # create arrives table
        self.drop_table('arrives')
        self.create_table('arrives', table_specs)

    def init_bus_data(self, stop_id: int, line):
        if self.conn is None:
            return

        # arrives
        arrive_1 = (self.arrives_cont, stop_id, line, 1, 0)
        self.arrives_cont += 1
        arrive_2 = (self.arrives_cont, stop_id, line, 2, 0)
        self.arrives_cont += 1
        print(self.arrives_cont)

        # create arrives
        self.insert_into_arrives(arrive_1)
        self.insert_into_arrives(arrive_2)
