from scapy.all import ARP, Ether, srp
import socket


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


def get_lan_devices(target_ip=None, iface=None):
    if target_ip is None:
        my_ip = socket.gethostbyname(socket.gethostname())
        gateway = ".".join(my_ip.split(".")[0:-1])
        target_ip = f"{gateway}/24"

    devices = scan(target_ip, iface=iface)

    return devices
