from data_base import DataBase
from sqlite3 import Error


class DataBaseEMT(DataBase):
    emt_db_filename = '../emt.db'

    def __init__(self, init=False):
        super().__init__()
        # create a database connection
        self.open()
        if init:
            # if os.path.exists(self.emt_db_filename):
            #     os.remove(self.emt_db_filename)
            self.arrives_cont = 0
            self.init_schema()

    def open(self):
        self.create_connection(self.emt_db_filename)

    def insert_into_arrives(self, values):
        sql = """
            INSERT INTO arrives(id, stop_id, line, position, estimateArrive) VALUES(?,?,?,?,?)
            """
        try:
            self.execute_with_parameters(sql, values)
            return self.cur.lastrowid
        except Error as ex:
            print(ex)

    def update_arrive(self, arrive):
        sql = """
            UPDATE arrives SET estimateArrive = ? WHERE stop_id = ? AND line = ? AND position = ?
            """
        self.execute_with_parameters(sql, arrive)

    def get_arrive(self, stop_id, line):
        sql = """
            SELECT estimateArrive FROM arrives WHERE stop_id = ? AND line = ? AND position = 1
            """
        return self.get_with_parameters(sql, (stop_id, line), first=True)

    def get_arrives(self, args):
        sql = """
            SELECT estimateArrive FROM arrives WHERE stop_id = ? AND line = ?
            """
        return self.get_with_parameters(sql, args, first=False)

    def init_schema(self):
        # create tables
        if self.conn is None:
            return

        parameters = """
            id integer PRIMARY KEY,
            stop_id integer,
            line text,
            position integer,
            estimateArrive integer
            """
        # create arrives table
        self.drop_table('arrives')
        self.create_table('arrives', parameters)

    def init_bus_data(self, stop_id: int, line):
        if self.conn is None:
            return

        # arrives
        arrive_1 = (self.arrives_cont, stop_id, line, 1, 0)
        self.arrives_cont += 1
        arrive_2 = (self.arrives_cont, stop_id, line, 2, 0)
        self.arrives_cont += 1
        # print(self.arrives_cont)

        # create arrives
        self.insert_into_arrives(arrive_1)
        self.insert_into_arrives(arrive_2)
