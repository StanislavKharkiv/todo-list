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
                COMPLETE BOOLEAN DEFAULT false
            )
            """
        )

        self.cursor.execute(
            """
            DO $$
            BEGIN
                IF (SELECT COUNT(*) FROM Tasks) = 0 THEN
                    INSERT INTO Tasks (NAME, COMMENT)
                    VALUES ('Example', 'do something for example...');
                END IF;
            END $$;
            """
        )

        self.cursor.execute(
            "ALTER TABLE Tasks ADD COLUMN IF NOT EXISTS deleted BOOLEAN DEFAULT false;"
        )

        self.cursor.execute(
            "ALTER TABLE Tasks ADD COLUMN IF NOT EXISTS delete_date TIMESTAMP ;"
        )

        self.conn.commit()

    def get_tasks(self):
        return self.db_fetch("SELECT * FROM Tasks WHERE deleted=false")

    def get_deleted_tasks(self):
        return self.db_fetch("SELECT * FROM Tasks WHERE deleted=true")

    def add_task(self, task):
        self.db_execute(
            "INSERT INTO Tasks (NAME, COMMENT) VALUES (%s, %s);",
            (task["name"], task["comment"]),
        )
        self.conn.commit()

    def delete_task(self, id):
        self.db_execute(
            "UPDATE Tasks SET deleted = True, delete_date = CURRENT_TIMESTAMP WHERE id=%s",
            (id,),
        )

    def delete_task_permanently(self, id):
        self.db_execute("DELETE FROM Tasks WHERE id=%s", (id,))

    def interval_deletion(self):
        print('CRON task ---')
        self.db_execute(
            "DELETE FROM Tasks WHERE delete_date <= CURRENT_TIMESTAMP - INTERVAL '1 day'"
        )

    def complete_task(self, id):
        self.db_execute("UPDATE Tasks SET COMPLETE = (True) WHERE id=%s", (id,))
