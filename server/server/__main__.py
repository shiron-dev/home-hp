from flask import Flask
from route import main, api

app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
