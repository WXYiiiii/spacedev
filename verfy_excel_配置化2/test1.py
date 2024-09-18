import sqlite3
import openpyxl
import yaml

# 加载配置文件
def load_config(config_file='config.yaml'):
    with open(config_file, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

# 从SQLite数据库中获取数据
def fetch_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
    SELECT
        prod_qty,
        prod_pct,
        prod_wow_change,
        prod_wow_ratio,
        prod_yoy_change,
        prod_yoy_ratio,
        prod_1st_quartile,
        prod_2nd_quartile,
        prod_3rd_quartile,
        prod_top5_tot,
        prod_top5_pct,
        payin_trust_scale_100m,
        trust_scale_pct,
        scale_wow_change,
        scale_wow_ratio,
        scale_yoy_change,
        scale_yoy_ratio,
        scale_1st_quartile,
        scale_2nd_quartile,
        scale_3rd_quartile,
        scale_top5_tot,
        scale_top5_pct,
        issuing_org_qty,
        issuing_org_wow_change,
        issuing_org_wow_ratio
    FROM reg_init_indus_sum_wk 
    ORDER BY order_idx;
    '''

    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data

# 将数据写入Excel文件
def write_to_excel(data, input_path, output_path, start_row, start_column):
    # 加载输入的Excel模板文件
    wb = openpyxl.load_workbook(input_path)
    ws = wb.active  # 获取当前活动工作表

    # 写入数据到指定位置
    for row_index, row_data in enumerate(data, start=start_row):
        for col_index, value in enumerate(row_data, start=start_column):
            ws.cell(row=row_index, column=col_index, value=value)

    # 保存输出的Excel文件
    wb.save(output_path)

# 主函数
if __name__ == "__main__":
    config = load_config()  # 加载配置文件

    db_path = config['sqlite']['db_path']
    input_path = config['input_path']
    output_path = config['output_path']
    start_column = config['start_column']
    start_row = config['start_row']

    data = fetch_data(db_path)  # 从数据库中获取数据
    write_to_excel(data, input_path, output_path, start_row, start_column)  # 写入Excel