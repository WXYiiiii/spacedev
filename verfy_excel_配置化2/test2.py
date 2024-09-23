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



def write_to_excel(data, input_path, output_path, start_row, start_column):
    # 打开模板文件
    workbook = openpyxl.load_workbook(input_path)
    worksheet = workbook.active

    # 插入空行以避免覆盖现有数据
    worksheet.insert_rows(start_row, amount=len(data))

    # 写入数据
    for row_index, row_data in enumerate(data):
        for col_index, value in enumerate(row_data):
            worksheet.cell(row=start_row + row_index, column=start_column + col_index, value=value)

    # 保存输出文件
    workbook.save(output_path)

# 主函数
def main():
    # 加载yaml配置
    config = load_yaml_config('config.yaml')

    # 从SQLite执行查询
    data = query_db(config['sqlite']['db_path'], config['query'])

    # 将数据写入Excel
    # write_to_excel(
    #     config['input_path'],
    #     config['output_path'],
    #     config['start_row'],
    #     config['start_column'],
    #     data
    # )

    write_to_excel(
        data,
        config['input_path'],
        config['output_path'],
        config['start_row'],
        config['start_column']

    )

if __name__ == '__main__':
    main()
