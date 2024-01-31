from flask import Flask
from route import main, api
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)



IS_DEBUG = os.environ.get("IS_DEBUG") == "True"
PORT = os.environ.get("PORT") or 8080

app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=IS_DEBUG, port=PORT)
