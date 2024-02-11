import psycopg2
from .tasks import TasksModel

try:
    conn = psycopg2.connect(
        host="db", database="postgres", user="admin", password="secret"
    )
    cur = conn.cursor()

    tasks = TasksModel(conn, cur)
except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)
