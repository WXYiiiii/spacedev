import csv

# 读取CSV文件并将每一行存储为列表
with open('data.csv', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    data_list = [row for row in csv_reader]

print(data_list)