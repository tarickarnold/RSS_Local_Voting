import datetime
import os
import sqlite3
from config import Config
import time
from time_keeper import Timer


class Database(object):

    def __init__(self, db_file_path) -> None:
        self.db_file_path = db_file_path
        self.connection = sqlite3.connect(db_file_path)
        self.cur = self.connection.cursor()

    def commit(self) -> None:
        self.connection.commit()

    def create_table(self, table_name, columns) -> None:
        column_definitions = ", ".join([f"{col[0]} {col[1]}" for col in columns])
        create_table_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"
        self.cur.execute(create_table_stmt)
        self.commit()

    def __del__(self) -> None:
        self.connection.close()

    def __enter__(self):
        return self.connection.cursor()

    def execute_insert(self, table_name, data) -> None:
        placeholders = ", ".join(["?" for _ in data])
        insert_stmt = f"INSERT INTO {table_name} VALUES ({placeholders});"
        self.cur.execute(insert_stmt, data)
        self.commit()

    def executemany_insert(self, table_name, data) -> None:
        placeholders = ", ".join(["?" for _ in data])
        insert_stmt = f"INSERT INTO {table_name} VALUES ({placeholders});"
        self.cur.executemany(insert_stmt, data)
        self.commit()

    def __exit__(self, ext_type, exc_value, traceback) -> None:
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    def select_all(self, table_name) -> list[any]:
        select_stmt: str = f"SELECT * FROM {table_name}"
        self.cur.execute(select_stmt)
        all_rows = self.cur.fetchall()
        return all_rows

    def select_many(self, table_name, number_of_rows) -> list[any]:
        self.number_of_rows: int = number_of_rows
        select_stmt: str = f"SELECT * FROM {table_name}"
        self.cur.execute(select_stmt)
        rows = self.cur.fetchmany(number_of_rows)
        return rows


# def main():
    # dir_name: str = os.path.dirname(__file__)
    # config = Config()
    # bot_name = config.settings.bot_name
    # stage = config.settings.current_env
    # machine_name = config.settings.machine_name
    # bot_user_name = config.settings.bot_user_name
    # business_unit = config.settings.business_unit
    # human_time = config.settings.human_time
    # from_email = config.settings.notifications.from_email
    # to_email = config.settings.notifications.to_email
    # table_name = config.settings.sqlite_db.table_name
    # db_file_path = config.settings.sqlite_db.db_file_path
    # id = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    # run_date = int(datetime.date.today().strftime("%Y%m%d"))
    # time = int(datetime.datetime.now().strftime("%H%M%S"))
    # timer = Timer()
    # start_time = timer.start()
    # elapsed_time = timer.stop()


    # total_transactions = 122
    # success = 100
    # business_exception = 20
    # system_exception = 2
    # error = "This is a error test"

    # columns: list[tuple[str, str]] = [
    #     ("id", "INTEGER PRIMARY KEY"),
    #     ("bot_name", "TEXT"),
    #     ("machine_name", "TEXT"),
    #     ("environment", "TEXT"),
    #     ("bot_user_name", "TEXT"),
    #     ("business_unit", "TEXT"),
    #     ("run_date", "INTEGER"),
    #     ("time", "INTEGER"),
    #     ("elapsed_time", "FLOAT"),
    #     ("human_time", "FLOAT"),
    #     ("total_transactions", "INTEGER"),
    #     ("success", "INTEGER"),
    #     ("business_exception", "INTEGER"),
    #     ("system_exception", "INTEGER"),
    #     ("error", "TEXT")
    # ]

    # test = "test"
    # new_column = [("test", "TEXT")]
    # new_data = [test]

    # db_name: str = bot_name + ".db"
    # db_file_path: str = os.path.join(dir_name, db_name)
    # db = Database(db_file_path)
    # data = [
    #     id,
    #     bot_name,
    #     machine_name,
    #     stage,
    #     bot_user_name,
    #     business_unit,
    #     run_date,
    #     time,
    #     elapsed_time,
    #     human_time,
    #     total_transactions,
    #     success,
    #     business_exception,
    #     system_exception,
    #     error
    #     ]
    
    # db.create_table(table_name = table_name, columns = columns)
    # db.execute_insert(table_name = table_name, data = data)

# if __name__ == "__main__":
#     main()
