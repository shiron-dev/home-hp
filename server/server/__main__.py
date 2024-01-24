from flask import Flask, request, Response, Blueprint, jsonify
import wakeonlan
import net_tools

app = Flask(__name__)

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/list", methods=["GET"])
def list_devices():
    return jsonify(net_tools.get_lan_devices())

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
