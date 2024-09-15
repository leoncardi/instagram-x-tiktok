import os

import aiosqlite
from entrymaven import l

class AsyncSQLiteCommiter:
    def __init__(self, db_dir, db_file_name):
        self.db_dir = db_dir
        self.db_file_name = db_file_name
        self.db_path = f'{self.db_dir}/{self.db_file_name}.db'
        self.conn = None
        self.cursor = None
               
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
                l.info(f'(Database: {self.db_file_name}.db) Database has been erased to store new data')
            except aiosqlite.Error as e:
                l.error(f'(Database: {self.db_file_name}.db | AsyncSQLiteCommiter.__init__) {e}')
                raise e

    async def __aenter__(self) -> 'AsyncSQLiteCommiter':
        try:
            if not os.path.exists(self.db_path):
                l.info(f'(Database: {self.db_file_name}.db) Database will be created from scratch to connect')
            self.conn = await aiosqlite.connect(self.db_path)
            self.cursor = await self.conn.cursor()
            l.info(f'(Database: {self.db_file_name}.db) Connection established ')
            return self
        except aiosqlite.Error as e:
            l.error(f'(Database: {self.db_file_name}.db | AsyncSQLiteCommiter.__enter__) {e}')
            raise e
    
    async def __aexit__(self, exc_type, exc_val, exec_tb):
        await self.close()

    async def close(self):
        try:
            await self.conn.close()
            l.info(f'(Database: {self.db_file_name}.db) Connection closed')
        except aiosqlite.Error as e:
            l.error(f'(Database: {self.db_file_name}.db | AsyncSQLiteCommiter.__exit__) {e}')
            raise e

    async def create_table(self, table_name: str):
        try:
            await self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY)')
        except aiosqlite.Error as e:
            l.warning(f'(Database: {self.db_file_name}.db | AsyncSQLiteCommiter.create_table) {e}')

    async def insert_extracted_raw_data(self, raw_datasets: list, table_name: str):
        try:
            await self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY)')

            for i, dataset in enumerate(raw_datasets, start=1):
                await self.cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN "{table_name}_{i}" TEXT')
                
            for i, dataset in enumerate(raw_datasets, start=1):
                for datapoint in dataset:
                    await self.cursor.execute(f'INSERT INTO {table_name} ({table_name}_{i}) VALUES(?)', (datapoint,))
                    l.info(f"(Database: {self.db_file_name}.db) Committed datapoint: {datapoint}")
                    await self.conn.commit()
            l.info(f'(Database: {self.db_file_name}.db) All datapoints have been committed')
        except aiosqlite.Error as e:
            l.warning(f'(Database: {self.db_file_name}.db | AsyncSQLiteCommiter.insert_extracted_raw_data) {e}')
            