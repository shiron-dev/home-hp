from scapy.all import ARP, Ether, srp
import socket
from util import memoize


def scan(ip, iface=None):
    arp_request = ARP(pdst=ip)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether_frame / arp_request

    result = srp(packet, iface=iface, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        try:
            hostname = received.hostname
        except:
            hostname = "N/A"
        devices.append({"ip": received.psrc, "mac": received.hwsrc, "hostname": hostname})

    return devices


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return None


@memoize()
def get_lan_devices(target_ip=None, iface=None):
    if target_ip is None:
        my_ip = get_local_ip()
        gateway = ".".join(my_ip.split(".")[0:-1])
        target_ip = f"{gateway}.1/24"

    devices = scan(target_ip, iface=iface)
    return devices
