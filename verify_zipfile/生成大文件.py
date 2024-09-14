import os
import random
import csv

# 设置文件名和目标大小(以字节为单位)
file_name = 'large_file6.csv'
target_size = 2 * 1024 * 1024 * 1024  # 200GB

# 定义生成数据的函数
def generate_data(num_rows):
    data = []
    for _ in range(num_rows):
        # 生成随机数据,您可以根据需要自定义数据格式
        row = [random.randint(1, 100), random.random(), 'Sample Text']
        data.append(row)
    return data

# 写入CSV文件
def write_large_csv(file_name, target_size):
    with open(file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)

        # 写入CSV头部
        csv_writer.writerow(['Integer', 'Float', 'Text'])

        current_size = os.path.getsize(file_name)
        num_rows = 0

        while current_size < target_size:
            # 每次生成并写入10000行
            rows_to_write = generate_data(10000)
            csv_writer.writerows(rows_to_write)
            num_rows += 10000

            # 更新当前文件大小
            current_size = os.path.getsize(file_name)

    print("CSV文件生成完成,文件名: {}, 总行数: {}".format(file_name, num_rows))

# 执行函数
if __name__ == '__main__':
    write_large_csv(file_name, target_size)