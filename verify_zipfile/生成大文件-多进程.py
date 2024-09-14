import csv
import numpy as np
import os
import multiprocessing as mp
# 多进程
def generate_chunk(start_row, chunk_size, num_columns):
    data = np.random.rand(chunk_size, num_columns)
    return data.tolist()

def write_chunk_to_csv(start_row, chunk_size, num_columns, filename, lock):
    data = generate_chunk(start_row, chunk_size, num_columns)

    lock.acquire()
    try:
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            if start_row == 0:
                writer.writerow(['col{}'.format(i) for i in range(num_columns)])
            writer.writerows(data)
    finally:
        lock.release()

def worker(args):
    start_row, chunk_size, num_columns, filename, lock = args
    write_chunk_to_csv(start_row, chunk_size, num_columns, filename, lock)

def parallel_generate_large_csv(filename, num_rows, num_columns, chunk_size=1000000, num_processes=None):
    if num_processes is None:
        num_processes = mp.cpu_count()

    manager = mp.Manager()
    lock = manager.Lock()

    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['col{}'.format(i) for i in range(num_columns)])

    pool = mp.Pool(processes=num_processes)

    tasks = [(start_row, chunk_size, num_columns, filename, lock)
             for start_row in range(0, num_rows, chunk_size)]

    pool.map(worker, tasks)

    pool.close()
    pool.join()

if __name__ == '__main__':
    filename = 'large_file.csv'
    total_rows = 10000000
    num_columns = 10
    chunk_size = 1000000

    parallel_generate_large_csv(filename, total_rows, num_columns, chunk_size)
