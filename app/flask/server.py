import secrets

from flask import Flask
from routes import routes
import models.main

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


routes(app)

if __name__ == "__main__":
    app.run(debug=True, port="9000", host="0.0.0.0")
