import os
import random

# 定义文件路径
file_path = 'output.txt'  # 输出文件名

# 定义第六列的可选内容
options = ["自然人", "境外自然人", "个体工商户", "猪猪", "猫猫"]

# 每次写入的行数
batch_size = 100000 # 每次写入 100 万行
total_rows = 100000000  # 总共生成 1 亿行

# 打开文件进行写入
with open(file_path, 'w', encoding='utf-8') as f:
    for i in range(total_rows):
        # 随机选择第六列的内容
        sixth_column_value = random.choice(options)

        # 创建一行数据，包含九列
        row = [
            f"Column1_{i}",   # 第一列
            f"Column2_{i}",   # 第二列
            f"Column3_{i}",   # 第三列
            f"Column4_{i}",   # 第四列
            f"Column5_{i}",   # 第五列
            sixth_column_value,  # 第六列（随机选择）
            f"Column7_{i}",   # 第七列
            f"Column8_{i}",   # 第八列
            f"Column9_{i}"    # 第九列
        ]

        # 使用 SOH 字符作为分隔符写入文件
        f.write('\x01'.join(row) + '\n')

        # 每写入一定数量的行，打印进度信息
        if (i + 1) % batch_size == 0:
            print(f"{i + 1} 行数据已写入...")

print(f"文件 '{file_path}' 已生成，包含 {total_rows} 行数据。 大小是{os.path.getsize(file_path) / (1024 * 1024)}M")