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
            "ALTER TABLE Tasks ADD COLUMN IF NOT EXISTS deleted BOOLEAN DEFAULT false;"
        )

        self.cursor.execute(
            "ALTER TABLE Tasks ADD COLUMN IF NOT EXISTS delete_date TIMESTAMP ;"
        )

        self.conn.commit()

    def db_request(self, sql_request):
        self.cursor.execute(sql_request)
        self.conn.commit()

    def db_fetch(self, sql_request):
        self.cursor.execute(sql_request)
        return self.cursor.fetchall()
    
    def get_tasks(self):
        return self.db_fetch("SELECT * FROM Tasks WHERE deleted=false")

    def get_deleted_tasks(self):
        return self.db_fetch("SELECT * FROM Tasks WHERE deleted=true")

    def add_task(self, task):
        self.db_request(f"INSERT INTO Tasks (NAME, COMMENT) VALUES ('{task["name"]}', '{task["comment"]}');")

    def delete_task(self, id):
        self.db_request(f"UPDATE Tasks SET deleted = {True}, delete_date = CURRENT_TIMESTAMP WHERE id={id}")

    def delete_task_permanently(self, id):
        self.db_request(f"DELETE FROM Tasks WHERE id={id}")
    
    def interval_deletion(self):
        self.db_request("DELETE FROM Tasks WHERE delete_date <= CURRENT_TIMESTAMP - INTERVAL '1 day'") 

    def complete_task(self, id):
        self.db_request(f"UPDATE Tasks SET COMPLETE = ({True}) WHERE id={id}")
