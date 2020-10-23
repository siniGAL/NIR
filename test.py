from scapy.all import *
import pandas as pd
import os

path = '/Users/macbookpro/Documents/Dataset/Pcaps/nonTor/'

for index in range(len((os.listdir(path)))):

    packets_data = {}
    scapy_cap = rdpcap('%s' % (path + os.listdir(path)[index]))

    for idx, packet in enumerate(scapy_cap):
        string = []
        if 'IP' in packet:
            string.extend([packet['IP'].src, packet['IP'].dst])
        else:
            string.append('xx.xx.xx.xx')
            string.append('xx.xx.xx.xx')
        if 'TCP' in packet:
            string.insert(1, packet['TCP'].sport)
            string.insert(3, packet['TCP'].dport)
        else:
            string.insert(1, 'xxxx')
            string.insert(3, 'xxxx')
        packets_data[idx] = string
    table = {}
    table[os.listdir(path)[index]] = packets_data
    data_frame = pd.DataFrame(table)
    data_frame.to_csv('%s.csv' % (os.listdir(path)[index]))
    print(os.listdir(path)[index])
