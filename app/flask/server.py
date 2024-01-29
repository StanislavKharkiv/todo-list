import psycopg2
from flask import Flask
from routes import routes

conn = psycopg2.connect(host="db", database="postgres", user="admin", password="secret")

cur = conn.cursor()
 
cur.execute("""
CREATE TABLE IF NOT EXISTS Tasks
(
    ID SERIAL PRIMARY KEY,
    NAME TEXT NOT NULL,
    COMMENT TEXT NOT NULL,
    COMPLETE BOOLEAN DEFAULT false
)
""")

cur.execute("""
DO $$
  BEGIN
    IF (SELECT COUNT(*) FROM Tasks) = 0 THEN
        INSERT INTO Tasks (NAME, COMMENT)
        VALUES ('Example', 'do something for example...');
    END IF;
  END $$;
""")

conn.commit()

print('DB created!!!!!!!!!!!!!!!!!')

app = Flask(__name__)

routes(app)

if __name__ == "__main__":
    app.run(debug=True, port="9000", host="0.0.0.0")

