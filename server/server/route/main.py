from flask import Flask, render_template, Blueprint
from domain import IPDevice
import net_tools

main = Blueprint("main", __name__)

@main.route("/")
def index():
  devices = IPDevice.get_all()
  scanned = net_tools.get_lan_devices()
  return render_template(
    'index.html',
    registered_devices=devices,
    scanned_devices=scanned
    )
