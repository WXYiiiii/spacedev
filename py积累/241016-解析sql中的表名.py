from sqlglot import parse_one, exp

def extract_table_name(sql):
    # 解析 SQL 语句
    parsed = parse_one(sql)

    # 找到解析结果中的所有表名
    tables = [table.name for table in parsed.find_all(exp.Table)]

    return tables[0]

# 示例 SQL 查询
sql_query = "SELECT * FROM my_table;"

# 提取并打印表名
table_names = extract_table_name(sql_query)
print("找到的表名:", table_names)