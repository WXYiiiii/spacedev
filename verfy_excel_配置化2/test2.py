import sqlite3
import openpyxl
import yaml

# 读取yaml配置文件
def load_yaml_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

# 从SQLite数据库执行查询
def query_db(db_path, query):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# 将数据批量写入Excel
def write_to_excel(input_path, output_path, start_row, start_column, data):
    # 打开输入Excel模板文件
    wb = openpyxl.load_workbook(input_path)
    ws = wb.active

    # 在指定起始行之前插入空行（如果需要的话）
    for _ in range(start_row - 1):
        ws.append([])  # 添加空行以确保从 start_row 开始

    # 批量写入数据，逐行插入
    for row_data in data:
        # 在指定的列位置插入数据
        ws.append([None] * (start_column - 1) + list(row_data))

    # 保存输出Excel文件
    wb.save(output_path)

# 主函数
def main():
    # 加载yaml配置
    config = load_yaml_config('config.yaml')

    # 从SQLite执行查询
    data = query_db(config['sqlite']['db_path'], config['query'])

    # 将数据写入Excel
    write_to_excel(
        config['input_path'],
        config['output_path'],
        config['start_row'],
        config['start_column'],
        data
    )

if __name__ == '__main__':
    main()
