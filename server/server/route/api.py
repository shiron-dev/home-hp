from flask import Blueprint, jsonify
import net_tools
from domain import IPDevice

api = Blueprint("api", __name__, url_prefix="/api")
ip = Blueprint("ip", __name__, url_prefix="/ip")

@api.route("device/list", methods=["GET"])
def get_devices():
    return jsonify(IPDevice.get_all())

@api.route("device/register", methods=["POST"])
def register_device(request):
    ip = request.form["ip"]
    mac = request.form["mac"]
    hostname = request.form["hostname"]
    device_name = request.form["device_name"]
    device = IPDevice(ip=ip, mac=mac, hostname=hostname, device_name=device_name)
    device.save()
    return jsonify({"result": "success"})
    

@ip.route("/list", methods=["GET"])
def list_devices():
    return jsonify(net_tools.get_lan_devices())

api.register_blueprint(ip)

