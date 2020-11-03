from scapy.all import *
import pandas as pd
import os
from multiprocessing import Pool


def get_pcap_paths(path):
    return (os.path.join(path, f)
            for f in os.listdir(path)
            if 'pcap' in f)


def create_csv(files):
    scapy_cap = rdpcap(files)
    packets_data = {}
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
        packets_data = {idx: string}
    data_frame = pd.DataFrame(packets_data)
    data_frame.to_csv(path_or_buf='/mnt/data/csv/' + files.replace(path, '') + '.csv')
    print(files)


if __name__ == '__main__':
    path = '/mnt/data/test/'

    files = get_pcap_paths(path)

    pool = Pool(10)
    pool.map(create_csv, files)
    pool.close()
    pool.join()
