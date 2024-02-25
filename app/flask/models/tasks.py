class TasksModel:
    def __init__(self, conn, cursor) -> None:
        self.conn = conn
        self.cursor = cursor

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
            "ALTER TABLE Tasks ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT false;"
        )

        self.conn.commit()

    def get_tasks(self):
        self.cursor.execute("SELECT * FROM Tasks WHERE is_deleted=false")
        return self.cursor.fetchall()

    def get_deleted_tasks(self):
        self.cursor.execute("SELECT * FROM Tasks WHERE is_deleted=true")
        return self.cursor.fetchall()

    def add_task(self, task):
        self.cursor.execute(
            "INSERT INTO Tasks (NAME, COMMENT, IS_DELETED) VALUES (%s, %s, %s);",
            (task["name"], task["comment"], False),
        )
        self.conn.commit()

    def delete_task(self, id):
        self.cursor.execute(
            "UPDATE Tasks SET is_deleted = (%s) WHERE id=%s",
            (
                True,
                id,
            ),
        )
        self.conn.commit()

    def delete_task_permanently(self, id):
        self.cursor.execute("DELETE FROM Tasks WHERE id=%s", (id,))
        self.conn.commit()

    def complete_task(self, id):
        self.cursor.execute(
            "UPDATE Tasks SET COMPLETE = (%s) WHERE id=%s",
            (
                True,
                id,
            ),
        )
        self.conn.commit()
