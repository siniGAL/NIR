# -*- coding: utf-8 -*-
from scapy.all import *
import numpy as np
import matplotlib.pyplot as plt

# rdpcap comes from scapy and loads in our pcap file
scapy_cap = rdpcap('AUDIO_tor_spotify2.pcap')

src_ip = '10.0.2.15'
src_port = '59717'
dst_ip = '37.97.149.8'
dst_port = '443'

start_time = 0
times = []
frames_lenght = []


for idx, packet in enumerate(scapy_cap):
    if 'IP' and 'TCP' in packet:
        if src_ip == packet['IP'].src and src_port == str(packet['TCP'].sport) and dst_ip == packet['IP'].dst and dst_port == str(packet['TCP'].dport):
            if start_time == 0:
                start_time = packet.time
                time = packet.time
                frames_lenght.append(packet.wirelen)
            elif packet.time - start_time > 10:
                if len(times) > 1:
                    flow_bytes = sum(frames_lenght) / sum(times)
                    flow_packets = len(frames_lenght) / sum(times)
                    flow_iat_min = min(times)
                    flow_iat_max = max(times)
                    #flow_iat_mean = sum(times) / len(times)
                    flow_iat_mean = np.mean(times)
                    '''
                    Xi = []
                    for i in range(len(times)):
                        Xi.append((times[i] - flow_iat_mean) ** 2)
                    flow_iat_std = (sum(Xi) / (len(times) - 1)) ** 0.5
                    '''
                    flow_iat_std = np.std(times)
                    print('flow iat min =', flow_iat_min, 'flow iat max =', flow_iat_max, 'flow iat mean =', flow_iat_mean, 'flow iat std =', flow_iat_std)
                    p1 = np.mean(times)
                    pp = np.array(times) - p1
                    yup = np.array(pp[pp > 0.0])
                    ydn = np.array(pp[pp < 0.0])
                    p2 = yup.max() - ydn.min()
                    p5 = (max(times) - np.mean(times)) / (np.mean(times) - min(times))
                    print(p5)
                    start_time = packet.time
                    time = packet.time
                    times = []
                    frames_lenght = []
                    frames_lenght.append(packet.wirelen)
            else:
                times.append(packet.time - time)
                time = packet.time
                frames_lenght.append(packet.wirelen)


