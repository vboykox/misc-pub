# -*- coding: utf-8 -*-

import signal
from sys import argv
from time import sleep, time
from scapy.all import *

_, role, iface, dst_mac, src_ip, dst_ip, *_ = argv + [None] * 10

iface_mac = get_if_hwaddr(iface)

p = Ether(src=iface_mac, dst=dst_mac)/IP(src=src_ip, dst=dst_ip)

processed = 0

def pps_print():
    end_time = time.monotonic()
    with open(f"pps-{role}.txt", "w+") as f:
        print("pss", role, processed / (end_time - start_time), file=f)

def signal_handler(sig, frame):
    pps_print()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

start_time = time.monotonic()
if role == "send":
    def pkts():
        global processed
        while True:
            yield p/f"{processed}\n"
            processed += 1
    sendp(pkts(), iface=iface, verbose=False, inter=1)
elif role == "recv":
    def process_pkt(pkt):
        global processed
        if not IP in pkt:
            return
        if pkt[IP].src != src_ip:
            return
        try:
            idx = int(pkt[IP].payload.load.decode('utf-8'))
        except: pass
        else:
            print(f"{time.time()}:{idx}")
            processed += 1

    sniff(iface=iface,
        prn=process_pkt,
        lfilter=lambda pkt: Ether in pkt and pkt[Ether].src != iface_mac)
