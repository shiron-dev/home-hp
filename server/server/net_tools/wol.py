import wakeonlan


def send_wal(mac_address, ip_address="255.255.255.255", port=9):
    wakeonlan.send_magic_packet(mac_address, ip_address=ip_address, port=port)
