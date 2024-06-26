from datetime import datetime
from .base_connector import BaseConnector

class TasksModel(BaseConnector):
    def __init__(self):
        super().__init__()

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Tasks
            (
                ID SERIAL PRIMARY KEY,
                NAME TEXT NOT NULL,
                COMMENT TEXT NOT NULL,
                COMPLETE BOOLEAN DEFAULT false,
                USER_ID INT NOT NULL,
                CREATE_DATE TIMESTAMP NOT NULL
            )
            """
        )

        self.cursor.execute(
            "ALTER TABLE Tasks ADD COLUMN IF NOT EXISTS deleted BOOLEAN DEFAULT false;"
        )

        self.cursor.execute(
            "ALTER TABLE Tasks ADD COLUMN IF NOT EXISTS delete_date TIMESTAMP ;"
        )

        self.cursor.execute(
            "ALTER TABLE Tasks ADD COLUMN IF NOT EXISTS create_date TIMESTAMP NOT NULL;"
        )

        self.conn.commit()

    def get_tasks(self, user_id):
        return self.db_fetch(
            f"SELECT * FROM Tasks WHERE deleted=false AND user_id={user_id}"
        )

    def get_deleted_tasks(self, user_id):
        return self.db_fetch(
            f"SELECT * FROM Tasks WHERE deleted=true AND user_id={user_id}"
        )

    def add_task(self, task, user_id):
        self.db_execute(
            "INSERT INTO Tasks (NAME, COMMENT, USER_ID, CREATE_DATE) VALUES (%s, %s, %s, %s);",
            (task["name"], task["comment"], user_id, datetime.now()),
        )
        self.conn.commit()

    def delete_task(self, id):
        self.db_execute(
            "UPDATE Tasks SET deleted = True, delete_date = CURRENT_TIMESTAMP WHERE id=%s",
            (id,),
        )

    def recover_task(self, id):
        self.db_execute(
            "UPDATE Tasks SET deleted=false WHERE id=%s",
            (id,),
        )

    def delete_task_permanently(self, id):
        self.db_execute("DELETE FROM Tasks WHERE id=%s", (id,))

    def interval_deletion(self):
        self.db_execute(
            "DELETE FROM Tasks WHERE delete_date <= CURRENT_TIMESTAMP - INTERVAL '1 day'"
        )

    def complete_task(self, id):
        self.db_execute("UPDATE Tasks SET COMPLETE = (True) WHERE id=%s", (id,))

    def not_complete_task(self, id):
        self.db_execute("UPDATE Tasks SET COMPLETE = (False) WHERE id=%s", (id,))
