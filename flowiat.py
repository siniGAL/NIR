# -*- coding: utf-8 -*-
from scapy.all import *

# rdpcap comes from scapy and loads in our pcap file
scapy_cap = rdpcap('AUDIO_tor_spotify2.pcap')

src_ip = '10.0.2.15'
src_port = '59717'
dst_ip = '37.97.149.8'
dst_port = '443'

pivot_table = {}
start_time = 0
times = []
frames_lenght = []

for idx, packet in enumerate(scapy_cap):
    if 'IP' and 'TCP' in packet:
        if src_ip == packet['IP'].src and src_port == packet['TCP'].sport and dst_ip == packet['IP'].dst and dst_port == packet['TCP'].dport or src_ip == packet['IP'].dst and src_port == packet['TCP'].dport and dst_ip == packet['IP'].src and dst_port == packet['TCP'].sport:
            if start_time == 0:
                start_time = packet.time
                time = packet.time
                times.append(0)
                frames_lenght.append(packet.wirelen)
            elif packet.time - start_time > 10:
                flow_bytes = sum(frames_lenght) / (scapy_cap[idx - 1].time - start_time)
                flow_packets = idx / (scapy_cap[idx - 1].time - start_time)
                flow_iat_min = min(times)
                flow_iat_max = max(times)
                flow_iat_mean = sum(times) / idx
                Xi = []
                for i in range(len(times)):
                    Xi.append((times[i] - flow_iat_mean) ** 2)
                flow_iat_std = (sum(Xi) / (idx - 2)) ** 0.5
            else:
                times.append(packet.time - time)
                time = packet.time
                frames_lenght.append(packet.wirelen)


