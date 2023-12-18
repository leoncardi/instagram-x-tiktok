import os
import sqlite3

from entrymaven import l

class SQLiteHandler:
    def __init__(self, db_dir, db_file_name):   
        self.db_dir = db_dir
        self.db_file_name = db_file_name

    def verify_to_create_database_if_it_does_not_exist(self):
        if not os.path.exists(self.db_file_name):
            l.info(f'Database "{self.db_file_name}" does not exist. Creating it.')
            try:
                with sqlite3.connect(self.db_file_name):
                    pass
            except sqlite3.Error as e:
                l.error(f'(SQLiteHandler.verify_to_create_database_if_it_does_not_exist) {e}')
        else:
            l.info(f'Database "{self.db_file_name}" already exists.')

    def connect(self):
        self.verify_to_create_database_if_it_does_not_exist()
        try:
            conn = sqlite3.connect(self.db_file_name)
            cursor = conn.cursor()
            l.info('Connected to database')
            return conn, cursor
        except sqlite3.Error as e:
            l.error(f'(SQLiteHandler.connect) {e}')
            return None, None

    def commit_and_disconnect(self, conn):
        try:
            conn.commit()
            l.info('Changes committed to database')
            conn = conn.close()
            l.info('Disconnected from database')
        except sqlite3.Error as e:
            l.error(f'(SQLiteHandler.commit_and_disconnect) {e}')

    def create_dataset_for_chart_data(self, extracted_data: list, table_name: str):
        try:
            conn, cursor = self.connect()
            
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            existing_table = cursor.fetchone()
            
            if existing_table:
                cursor.execute(f"DROP TABLE {table_name}")
                l.info(f"Table '{table_name}' already exists. Overwriting it.")        
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (chart_raw TEXT, table_raw TEXT)')

            for data in extracted_data:
                cursor.execute(f'INSERT INTO {table_name} (chart_raw) VALUES (?)', (data,))
            l.info(f'Inserted {len(extracted_data)} datapoints into table {table_name}')
            
            self.commit_and_disconnect(conn)
        except sqlite3.Error as e:
            l.error(f'(SQLiteHandler.create_table) {e}')
            raise e
        
    def create_dataset_for_table_data(self, extracted_data: list, table_name: str):
        pass