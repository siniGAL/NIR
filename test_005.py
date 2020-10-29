from scapy.all import *
import pandas as pd
import os
from multiprocessing import Pool


def get_image_paths(path):
    return (os.path.join(path, f)
            for f in os.listdir(path)
            if 'pcap' in f)


def create_csv(files):
    packets_data = {}
    scapy_cap = rdpcap(files)

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
    table[files] = packets_data
    data_frame = pd.DataFrame(table)
    data_frame.to_csv('%s.csv' % (files))
    print(files)

if __name__ == '__main__':
    path = '/Users/macbookpro/Documents/Dataset/Pcaps/tor/'

    files = get_image_paths(path)

    pool = Pool(4)
    pool.map(create_csv, files)
    pool.close()
    pool.join()
