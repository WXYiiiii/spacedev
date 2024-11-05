import csv

# 要写入CSV的数据
data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "Los Angeles"],
    ["Charlie", 35, "Chicago"]
]

# 创建并写入CSV文件
with open('output.csv', mode='w', newline='') as file:
    csv_writer = csv.writer(file)

    # 写入标题行
    csv_writer.writerow(data[0])

    # 写入数据行
    csv_writer.writerows(data[1:])

print("CSV文件已创建并写入数据。")