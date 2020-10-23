# -*- coding: utf-8 -*-
from scapy.all import *

# rdpcap comes from scapy and loads in our pcap file
scapy_cap = rdpcap('AIM_Chat.pcap')

table = []

package_range = {}
source_ips = []
source_ports = []
destination_ips = []
destination_ports = []
protocols = []
frames_lenght = []
time_packets = []

start_time = scapy_cap[0].time

pivot_table = {}

for idx, packet in enumerate(scapy_cap):
    total_time = packet.time - start_time
    if total_time > 10:
        flow_bytes = sum(frames_lenght) / (scapy_cap[idx - 1].time - start_time)
        flow_packets = idx / (scapy_cap[idx - 1].time - start_time)
        flow_iat_min = min(time_packets)
        flow_iat_max = max(time_packets)
        flow_iat_mean = sum(time_packets)/idx
        Xi = []
        for i in range(len(time_packets)):
            Xi.append((time_packets[i] - flow_iat_mean)**2)
        flow_iat_std = (sum(Xi) / (idx-2))**0.5
    elif 'IP' in packet:
        source_ips.append(packet['IP'].src)
        source_ports.append(packet['TCP'].sport)
        destination_ips.append(packet['IP'].dst)
        destination_ports.append(packet['TCP'].dport)
        protocols.append(packet['IP'].proto)
        frames_lenght.append(packet.wirelen)
        if idx != 0:
            time_packets.append(packet.time - scapy_cap[idx - 1].time)
    else:
        frames_lenght.append(packet.wirelen)
        if idx != 0:
            time_packets.append(packet.time - scapy_cap[idx - 1].time)
    pass
