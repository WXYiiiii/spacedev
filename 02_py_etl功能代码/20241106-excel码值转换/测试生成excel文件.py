import pandas as pd

# 创建测试数据，包含新码值
data = {
    '姓名': ['张三', '李四', '王五'],
    '年龄': [28, 30, 25],
    '职业': ['a', 'b', 'c'],  # 新职业码值
    '地址': ['北京市朝阳区', '上海市浦东区', '广州市天河区'],
    '电话号码': ['a', 'b', 'c'],  # 新电话号码码值
    '邮箱': ['zhangsan@example.com', 'lisi@example.com', 'wangwu@example.com'],
    '性别': ['0', '1', '0'],  # 性别码值，0: 男，1: 女
    '状态': ['0', '1', '0']   # 状态码值，0: 在职，1: 离职
}

# 创建DataFrame
df = pd.DataFrame(data)

# 保存为Excel文件
excel_file_path = 'test_excel_file.xlsx'
df.to_excel(excel_file_path, index=False)

print(f"测试Excel文件已生成: {excel_file_path}")