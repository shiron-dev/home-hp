from scapy.all import ARP, Ether, srp
import socket
from util import memoize
from ping3 import ping
import concurrent.futures
from apscheduler.schedulers.blocking import BlockingScheduler

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


def ping_to_device(ip_address, port=80):
    try:
        result = ping(ip_address, timeout=2, unit="s")
        return result is not None
    except Exception as e:
        print(f"Error during ping: {e}")
        return False


def ping_all_devices(ip_addresses):
    ret = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(ping_to_device, ip_addresses))
        ret.extend(results)
    return ret


def get_lan_devices(target_ip=None, iface=None):
    if target_ip is None:
        my_ip = get_local_ip()
        gateway = ".".join(my_ip.split(".")[0:-1])
        target_ip = f"{gateway}.1/24"

    devices = scan(target_ip, iface=iface)
    return devices

class ScanManager:

    def __init__(self, interval=20):
        self.status = {}
        self.interval = interval
        self.scan_ips = []
        self.scheduler = BlockingScheduler()

    # @memoize
    def get_lan_devices(self):
        return get_lan_devices()

    # @memoize
    def ping_all_devices(self, ip_addresses):
        return ping_all_devices(ip_addresses)
    
    def start(self, ip_addresses):
        self.scan_ips = ip_addresses
        self.scheduler.add_job(self._update_status, "interval", seconds=self.interval)
        self.scheduler.start()
    
    def set_scan_ips(self, ip_addresses):
        self.scan_ips = ip_addresses

    def stop_scan(self):
        self.scan_ips = []
        self.scheduler.shutdown()

    def _update_status(self):
        for i, st in enumerate(self.ping_all_devices(self.scan_ips)):
            self.status[self.scan_ips[i]] = st

    def get_status(self, ip_addresses):
        return [self.status[key] if key in self.status else False for key in ip_addresses]
