import yaml
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import sqlite3

# 读取配置文件
def load_config(config_path='config.yaml'):
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# 连接SQLite，执行查询并获取结果
def query_sqlite_data(conn, project_id, sqlite_indicators, config):
    cursor = conn.cursor()
    query = f"""
    SELECT {', '.join(sqlite_indicators)}
    FROM project_data
    WHERE {config['mapping']['project_id_column']} = ?
    """
    cursor.execute(query, (project_id,))
    return cursor.fetchone()

# 设置单元格样式的函数
def set_cell_style(cell, config):
    cell.font = Font(
        name=config['excel_style']['font']['name'],
        size=config['excel_style']['font']['size'],
        bold=config['excel_style']['font']['bold'],
        italic=config['excel_style']['font']['italic'],
        color=config['excel_style']['font']['color']
    )
    cell.fill = PatternFill(start_color=config['excel_style']['fill']['start_color'])
    cell.alignment = Alignment(
        horizontal=config['excel_style']['alignment']['horizontal'],
        vertical=config['excel_style']['alignment']['vertical']
    )

# 读取Excel模板，获取项目名称、指标名称的映射关系
def read_excel_template(template_path, config):
    workbook = openpyxl.load_workbook(template_path)
    sheet = workbook.active

    # 获取Excel中的指标字段，从指定列开始
    excel_indicators = [cell.value for cell in sheet[config['mapping']['indicator_row']][config['mapping']['column_num']:]]

    # 获取项目名称和对应的Excel行号
    project_map = {
        sheet[f"{config['mapping']['project_column']}{row}"].value: row
        for row in range(config['mapping']['start_row'], sheet.max_row + 1)
        if sheet[f"{config['mapping']['project_column']}{row}"].value
    }

    return workbook, sheet, excel_indicators, project_map

# 将查询结果写入Excel
def write_to_excel(sheet, project_row, query_result, excel_to_sqlite_indicator_map, config):
    excel_indicators = [cell.value for cell in sheet[config['mapping']['indicator_row']][config['mapping']['column_num']:]]
    indicator_column_map = {indicator: idx + config['mapping']['column_num'] for idx, indicator in enumerate(excel_indicators)}

    for excel_indicator, column_idx in indicator_column_map.items():
        sqlite_field = excel_to_sqlite_indicator_map.get(excel_indicator)
        if sqlite_field and query_result:
            result_index = list(excel_to_sqlite_indicator_map.values()).index(sqlite_field)
            cell_value = query_result[result_index]
            cell = sheet.cell(row=project_row, column=column_idx)
            cell.value = cell_value
            set_cell_style(cell, config)

# 主函数
def main():
    # 加载配置文件
    config = load_config()

    # 读取Excel模板
    template_path = './data/input_file1.xlsx'
    workbook, sheet, excel_indicators, project_map = read_excel_template(template_path, config)

    # 从配置文件中获取Excel指标名称到SQLite字段的映射
    excel_to_sqlite_indicator_map = config['indicator_mapping']
    sqlite_indicators = list(excel_to_sqlite_indicator_map.values())

    # 连接数据库，只执行一次
    conn = sqlite3.connect(config['sqlite']['db_path'])

    # 遍历Excel中的项目名称
    for project_name, excel_row in project_map.items():
        project_id = config['project_mapping'].get(project_name)
        if project_id:
            # 查询SQLite数据库中的数据
            query_result = query_sqlite_data(conn, project_id, sqlite_indicators, config)
            if query_result:
                # 将查询结果写入Excel
                write_to_excel(sheet, excel_row, query_result, excel_to_sqlite_indicator_map, config)

    # 关闭数据库连接
    conn.close()

    # 保存Excel文件
    output_path = 'output.xlsx'
    workbook.save(output_path)
    print(f"数据已成功写入 {output_path}")

if __name__ == "__main__":
    main()
