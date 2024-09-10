import pandas as pd

# 读取包含表名称的Excel文件的Sheet1
df = pd.read_excel('excel1.xlsx', sheet_name='qqq')

# 假设表名称在第一列
table_names = df.iloc[:, 0].tolist()  # 获取第一列的所有数据并转换为列表

# 读取分词表
translation_df = pd.read_excel('excel2.xlsx')
# 假设分词表有两列：'abbreviation'和'translation'
abbreviations = translation_df.set_index('abbreviation')['translation'].to_dict()

# 拼接英文名称
final_names = []
for table in table_names:
    # 假设表名称中包含分词,使用分词表进行拼接
    name_parts = table.split('_')  # 根据下划线分割表名称
    translated_parts = [abbreviations.get(part, part) for part in name_parts]  # 翻译缩写
    final_name = ' '.join(translated_parts)  # 拼接成最终名称
    final_names.append(final_name)

# 创建一个新的DataFrame保存结果
result_df = pd.DataFrame(final_names, columns=['Final English Name'])

# 保存到新的Excel文件
result_df.to_excel('excel3.xlsx', index=False)