from flask import Flask
from routes import routes
import models.main

app = Flask(__name__)

routes(app)

if __name__ == "__main__":
    app.run(debug=True, port="9000", host="0.0.0.0")
