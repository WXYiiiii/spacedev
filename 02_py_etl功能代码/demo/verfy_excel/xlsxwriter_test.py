import xlsxwriter

# 创建一个新的Excel文件
workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()

# 设置列宽
worksheet.set_column('A:A', 20)

# 添加加粗格式
bold = workbook.add_format({'bold': True})

# 写入数据
worksheet.write('A1', 'Hello')
worksheet.write('A2', 'World', bold)
worksheet.write(2, 0, 123)
worksheet.write(3, 0, 123.456)

# 插入图像
worksheet.insert_image('B5', 'logo.png')

# 创建图表
chart = workbook.add_chart({'type': 'column'})
chart.add_series({
    'name': 'Series1',
    'categories': '=Sheet1!$A$1:$A$5',
    'values': '=Sheet1!$B$1:$B$5',
})
worksheet.insert_chart('D2', chart)

# 添加自动筛选
worksheet.autofilter('A1:D1')

# 关闭工作簿
workbook.close()

