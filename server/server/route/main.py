from flask import Flask, render_template, Blueprint, redirect, request
from domain import IPDevice
import net_tools

main = Blueprint("main", __name__)


scan_manager = net_tools.ScanManager()
scan_manager.start([device.ip for device in IPDevice.get_all()])

@main.route("/")
def index():
    devices = IPDevice.get_all()
    scan_manager.set_scan_ips([device.ip for device in devices])
    status = scan_manager.get_status([device.ip for device in devices])
    for i in range(len(devices)):
        devices[i].status = status[i]
    scanned = scan_manager.get_lan_devices()
    return render_template("index.html", registered_devices=devices, scanned_devices=scanned)


@main.route("/register", methods=["POST"])
def register():
    ip = request.form["ip"]
    mac = request.form["mac"]
    hostname = request.form["hostname"]
    name = request.form["name"]
    device = IPDevice(ip=ip, mac=mac, hostname=hostname, name=name)
    device.save()
    return redirect("/")


@main.route("/delete", methods=["POST"])
def delete():
    id = request.form["id"]
    device = IPDevice.get_by_id(id)
    device.delete()
    return redirect("/")


@main.route("/wol", methods=["POST"])
def wol():
    device = IPDevice.get_by_id(request.form["id"])
    net_tools.send_wal(device.mac)
    return redirect("/")


@main.route("/update")
def update():
    return render_template("update.html", device=IPDevice.get_by_id(request.args.get("id")))


@main.route("/update", methods=["POST"])
def update_post():
    device = IPDevice.get_by_id(request.form["id"])
    device.name = request.form["name"]
    device.save()
    return redirect("/")
