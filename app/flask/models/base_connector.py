import psycopg2
from psycopg2.extras import RealDictCursor
import os

try:
    conn = psycopg2.connect(
        host="db", database=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD')
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)
except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)


class BaseConnector:

    def __init__(self):
        self.conn = conn
        self.cursor = cursor

    def db_execute(self, sql_request: str, variables: tuple = None) -> None:
        self.cursor.execute(sql_request, variables)
        self.conn.commit()

    def db_fetch(
        self, sql_request: str, variables: tuple = None, quantity: int | None = None
    ):
        self.cursor.execute(sql_request, variables)
        if quantity:
            return self.cursor.fetchmany(quantity)
        else:
            return self.cursor.fetchall()
