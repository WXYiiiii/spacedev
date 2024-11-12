import openpyxl

# 对特定单元格进行替换 其他内容格式不变

# 1. 读取Excel文件
input_file = './data/input.xlsx'
output_file = './data/pyxlout.xlsx'

# 加载工作簿
workbook = openpyxl.load_workbook(input_file)

# 选择活动工作表（可以根据需要选择特定的工作表）
sheet = workbook.active

# 2. 修改特定单元格的内容
# 假设我们要修改A1和B2单元格的内容
sheet['A1'] = '新的内容1'  # 修改A1单元格
sheet['B2'] = '新的内容2'  # 修改B2单元格

# 3. 保存修改后的Excel文件
workbook.save(output_file)

print(f"文件已保存为 {output_file}")