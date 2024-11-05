# 示例输入：包含多个列表，每个列表的第一个元素是 zip_name
input_list = [
    ["org1-period1-10-flagA", "additional_info1"],
    ["org1-period1-15-flagB", "additional_info2"],
    ["org1-period2-20-flagA", "additional_info3"],
    ["org2-period1-10-flagC", "additional_info4"],
    ["org2-period1-10-flagD", "additional_info5"],
    ["org1-period1-10-flagA", "additional_info6"],  # 重复项
    ["org2-period2-15-flagC", "additional_info7"],
]

# 使用字典进行去重，键为 (org, period)，值为完整的 zip_name 和其他信息
unique_dict = {}

for item in input_list:
    zip_name = item[0]  # 原始 zip_name
    parts = zip_name.split('-')  # 分割字符串
    org, period, time, flag = parts  # 获取各个部分

    key = (org, period)  # 使用 (org, period) 作为字典的键

    # 如果键不存在或当前的 flag/time 更优，则更新字典
    if key not in unique_dict:
        unique_dict[key] = [zip_name, item[1]]  # 存储原始 zip_name 和其他信息
    else:
        existing_zip_name, existing_info = unique_dict[key]

        # 根据 flag 和 time 的优先级进行比较
        existing_parts = existing_zip_name.split('-')
        existing_time, existing_flag = existing_parts[2], existing_parts[3]

        if (flag > existing_flag) or (flag == existing_flag and time > existing_time):
            unique_dict[key] = [zip_name, item[1]]  # 更新为更优的值

# 将去重后的结果转换为列表
unique_list = [value for value in unique_dict.values()]

# 输出结果
for r in unique_list:
    print(r)