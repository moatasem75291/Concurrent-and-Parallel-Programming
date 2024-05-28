import os
import threading
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.sql import text


class PostgresMasterScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super(PostgresMasterScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self):
        while True:
            val = self._input_queue.get()
            if val == "DONE":
                break

            symbol, price, extracted_time = val
            postgress_worker = PostgresWorkwer(symbol, price, extracted_time)
            postgress_worker.insert_into_db()


class PostgresWorkwer:
    def __init__(self, symbol, price, extracted_time):
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time

        load_dotenv()
        self._PG_USER = os.getenv("PG_USER") or ""
        self._PG_PW = os.getenv("PG_PW") or ""
        self._PG_HOST = os.getenv("PG_HOST") or "localhost"
        self._PG_DB = os.getenv("PG_DB") or "postgres"

        self._engine = create_engine(
            f"postgresql://{self._PG_USER}:{self._PG_PW}@{self._PG_HOST}/{self._PG_DB}"
        )

    def _create_insert_query(self):
        query = """INSERT INTO prices (symbol, price, extracted_time) VALUES (:symbol, :price, :extracted_time)"""
        return query

    def insert_into_db(self):

        query = self._create_insert_query()

        with self._engine.connect() as conn:
            if conn.execute(
                text(query),
                {
                    "symbol": self._symbol,
                    "price": self._price,
                    "extracted_time": str(self._extracted_time),
                },
            ):
                conn.commit()
                print(f"Date for {self._symbol} Saved to the database.")
