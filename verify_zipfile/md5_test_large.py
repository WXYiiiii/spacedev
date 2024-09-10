import hashlib
import os
import time
from memory_profiler import profile

@profile
def calculate_md5(file_path):
    """计算文件的 MD5 值"""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        # 逐块读取文件内容并更新 MD5 哈希
        for byte_block in iter(lambda: f.read(1024 * 1024 * 10), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()


def write_transfer_flag(file_path, md5_value):
    """将 MD5 值写入传输标志文件"""
    flag_file_path = file_path + ".ok"
    with open(flag_file_path, "w") as f:
        f.write(md5_value)
    # print(f"MD5 value written to {flag_file_path}")


start_time = time.time()

file_path = "./data/temp.csv"
md5_value = calculate_md5(file_path)
# print(f"MD5 value: {md5_value}")
write_transfer_flag(file_path, md5_value)

end_time = time.time()  # 记录结束时间
elapsed_time = end_time - start_time  # 计算解压时间
print(f"标志文件生成完成，耗时 {elapsed_time:.2f} 秒。")


# 4kb  15.74s
# 2mb  12.40s
