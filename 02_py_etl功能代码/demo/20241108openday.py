import csv
from datetime import datetime

# 读取原始CSV文件，添加日期列并写入新的CSV文件
input_file = 'your_file.csv'  # 输入文件名
output_file = 'updated_file.csv'  # 输出文件名

# 获取当前日期
current_date = datetime.now().strftime('%Y%m%d')

# 读取整个CSV文件
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    # 使用csv.reader读取数据，确保所有字段都用双引号包裹
    reader = csv.reader(infile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)

    # 将数据存储在列表中
    data = [row for row in reader]

# 在每一行末尾添加当前日期
for row in data:
    row.append(current_date)

# 写入新的CSV文件
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerows(data)  # 一次性写入所有行

print(f"已将日期添加到 {output_file} 中，所有字段均用双引号包裹。")