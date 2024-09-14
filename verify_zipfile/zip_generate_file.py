import csv
import os
import uuid
import numpy as np

def generate_large_csv(file_name, target_size_gb):
    target_size_bytes = target_size_gb * (1024 ** 3)  # 转换为字节
    chunk_size = 1024 * 1024  # 每次写入 1MB 数据
    rows_per_chunk = chunk_size // 100  # 假设每行平均 100 字节

    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # 生成数据直到文件大小达到目标大小
        while os.path.getsize(file_name) < target_size_bytes:
            for _ in range(rows_per_chunk):
                # 生成随机数据
                row = [str(uuid.uuid4()), np.random.random(), np.random.random(), np.random.randint(1000)]
                writer.writerow(row)
            csvfile.flush()  # 刷新写入缓存

# 使用示例
generate_large_csv('./data/large1.csv', 1)  # 生成 4GB 的 CSV 文件