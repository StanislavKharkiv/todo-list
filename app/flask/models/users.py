from .base_connector import BaseConnector


class UsersModel(BaseConnector):
    def __init__(self):
        super().__init__()

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Users
            (
                ID SERIAL PRIMARY KEY,
                EMAIL VARCHAR(255) NOT NULL,
                PASSWORD VARCHAR(120) NOT NULL
            )
            """
        )

    def signup(self, data):
        self.db_execute(
            "INSERT INTO Users (EMAIL, PASSWORD) VALUES(%s, %s);",
            (data["email"], data["password"]),
        )

    def find_by_email(self, email):
        return self.db_fetch("SELECT * FROM Users WHERE email=%s", (email,), 1)
    
    def delete_user(self, id):
        self.db_execute("DELETE FROM Users WHERE id=%s", (id,))
