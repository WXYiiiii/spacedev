import os
import time

import zipfile
from memory_profiler import profile


@profile
def unzip_large_file(zip_file_path, extract_to):
    # 确保目标解压目录存在
    os.makedirs(extract_to, exist_ok=True)

    # 记录开始时间
    start_time = time.time()

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 提取所有文件到指定目录
        zip_ref.extractall(extract_to)

    # 计算解压时间
    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time


zip_file_path = './data/large8.zip'  # 替换为你的 ZIP 文件路径
extract_to = './data/'  # 替换为解压目标路径

elapsed_time = unzip_large_file(zip_file_path, extract_to)
print(f"解压耗时: {elapsed_time:.2f} 秒")


