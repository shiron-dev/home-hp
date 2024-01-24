from scapy.all import ARP, Ether, srp
import socket


def scan(ip):
    # ARPパケットを作成して送信
    arp_request = ARP(pdst=ip)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")  # ブロードキャストアドレスに送信
    packet = ether_frame / arp_request

    result = srp(packet, timeout=3, verbose=0)[0]

    # 取得したデバイスの情報を格納
    devices = []
    for sent, received in result:
        try:
            # ホスト名の取得
            hostname = received.hostname
        except:
            hostname = "N/A"
        devices.append({"ip": received.psrc, "mac": received.hwsrc, "hostname": hostname})

    return devices


def get_lan_devices(target_ip=None):
    if target_ip is None:
        my_ip = socket.gethostbyname(socket.gethostname())
        gateway = ".".join(my_ip.split(".")[0:-1])
        target_ip = f"{gateway}/24"

    devices = scan(target_ip)

    return devices
