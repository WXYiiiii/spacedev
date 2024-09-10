import zipfile
import os
import time
from memory_profiler import profile

@profile
def stream_unzip(source_file, target_file):
    CHUNK_SIZE = 1024 * 1024  # 每次读取1MB

    try:
        start_time = time.time()  # 记录开始时间

        with zipfile.ZipFile(source_file, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            if not file_list:
                print("ZIP 文件中没有文件。")
                return

            # 可以选择解压第一个文件，或者遍历所有文件
            for file_name in file_list:
                with zip_ref.open(file_name) as source_ref:
                    with open(target_file, 'wb') as target_ref:
                        for chunk in iter(lambda: source_ref.read(CHUNK_SIZE), b''):
                            target_ref.write(chunk)
                print(f"已解压缩 {file_name} 到 {target_file}")

        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算解压时间
        print(f"解压完成，耗时 {elapsed_time:.2f} 秒。")

    except zipfile.BadZipFile:
        print("错误：无法打开 ZIP 文件，文件可能已损坏。")
    except Exception as e:
        print(f"发生错误：{e}")

# 解压
stream_unzip('./data/large8.zip', './data/temp.csv')



# import zipfile
#
# from Crypto.SelfTest.Cipher.test_CFB import file_name
#
#
# def stream_unzip(source_file, target_file):
#     CHUNK_SIZE = 1024 * 1024  # 每次读取1MB
#
#     with zipfile.ZipFile(source_file, 'r') as zip_ref:
#         file_name = zip_ref.namelist()[0]
#         with zip_ref.open(file_name) as source_ref:  # 使用 open() 方法打开文件
#             with open(target_file, 'wb') as target_ref:
#                 for chunk in iter(lambda: source_ref.read(CHUNK_SIZE), b''):
#                     target_ref.write(chunk)
#
# # 使用示例
# stream_unzip('data/large_file.zip', 'utput.csv')
