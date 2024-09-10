import psutil
import os

# 獲取當前進程ID
# 获取ID -> 进程 -> 内存信息
pid = os.getpid()
print(pid)
process = psutil.Process(pid)


# 獲取程序當前的內存使用量（以MB為單位）
memory_info = process.memory_info()
print(f"RSS: {memory_info.rss / (1024 ** 2):.2f} MB")  # 常驻集大小
print(f"VMS: {memory_info.vms / (1024 ** 2):.2f} MB")  # 虚拟内存大小
