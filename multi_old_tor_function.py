from functions import iat_statistics
from functions import walk_path
import time as timer
import shutil
import os
import pandas as pd
from multiprocessing import Pool
import itertools


def multi_function(file, timeout):
    if 'nontor' in file.lower():
        label = 'nonTOR'
    else:
        label = 'TOR'

    iat_statistics(file, timeout, label)

if __name__  == '__main__':
    timeout = 10

    source_path = '/Users/macbookpro/Documents/all_numpy/csv_of_pcap'
    files = walk_path(source_path)
    shutil.rmtree('tmp', ignore_errors=True, onerror=None)
    os.mkdir('tmp', dir_fd=None)

    start_timer = timer.time()
    pool = Pool(8)
    pool.starmap(multi_function, zip(files, list(itertools.repeat(timeout, len(files)))))
    pool.close()
    pool.join()
    files = walk_path('tmp')
    data = pd.DataFrame()

    for file in files:
        data_tmp = pd.read_csv(file, sep=",")
        data = pd.concat([data, data_tmp])
    data.to_csv('statistics_' + str(timeout) + 's' + '.csv', index=False)

    shutil.rmtree('tmp', ignore_errors=False, onerror=None)
    print('Time to complete: %s' % ((timer.time() - start_timer) / 60))
