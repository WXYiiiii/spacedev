import pandas as pd
import logging

class ExcelCodeReplacer:
    def __init__(self, excel_file_path, output_file_path, logger=None):
        self.excel_file_path = excel_file_path
        self.output_file_path = output_file_path
        self.excel_df = None
        self.logger = logger or logging.getLogger(__name__)

        # 模拟配置表数据（新码值与实际值的映射）
        self.config_data = [
            ('职业', 'a', '软件工程师'),
            ('职业', 'b', '产品经理'),
            ('职业', 'c', '数据分析师'),
            ('电话号码', 'a', '13800000000'),
            ('电话号码', 'b', '13900000001'),
            ('电话号码', 'c', '13700000002'),
            ('性别', '0', '男'),
            ('性别', '1', '女'),
            ('状态', '0', '在职'),
            ('状态', '1', '离职')
        ]

    def read_excel(self):
        """读取Excel文件"""
        self.logger.info(f"正在从路径读取Excel文件: {self.excel_file_path}")
        self.excel_df = pd.read_excel(self.excel_file_path)
        self.logger.info(f"Excel文件读取成功，共有 {len(self.excel_df)} 行.")

        # 输出读取到的数据和数据类型
        self.logger.info(f"Excel文件内容:\n{self.excel_df}")
        self.logger.info(f"各列的数据类型:\n{self.excel_df.dtypes}")

        # 将所有数据转换为字符串类型
        self.excel_df = self.excel_df.astype(str)
        self.logger.info("所有数据已转换为字符串类型.")
        self.logger.info(f"转换后的数据类型:\n{self.excel_df.dtypes}")

    def replace_codes(self):
        """替换Excel中的码值"""
        dictionaries = {}

        # 构建字典用于替换
        for row in self.config_data:
            column_name, code_value, code_name = row  # 解包元组

            if column_name not in dictionaries:
                dictionaries[column_name] = {}

            dictionaries[column_name][code_value] = code_name

        self.logger.info(f"替换字典: {dictionaries}")

        # 替换操作
        for column in dictionaries.keys():
            if column in self.excel_df.columns:
                self.logger.info(f"正在替换列中的码值: {column}")
                # 打印当前列的数据
                original_data = self.excel_df[column].unique()
                self.logger.info(f"原始数据: {original_data}")

                # 处理多个码值的情况
                def replace_multiple_codes(cell):
                    if ',' in cell:
                        codes = cell.split(',')
                        names = [dictionaries[column].get(code.strip(), code.strip()) for code in codes]
                        return ';'.join(names)
                    else:
                        return dictionaries[column].get(cell.strip(), cell.strip())

                # 使用 apply 方法进行替换
                self.excel_df[column] = self.excel_df[column].apply(replace_multiple_codes)

                # 打印替换后的数据
                replaced_data = self.excel_df[column].unique()
                self.logger.info(f"替换后的数据: {replaced_data}")
                self.logger.info(f"列 {column} 的替换完成.")

    def save_to_excel(self):
        """保存替换后的Excel文件"""
        if self.output_file_path == self.excel_file_path:
            raise ValueError("输出文件路径不能与输入文件路径相同.")

        self.logger.info(f"正在保存更新后的Excel文件到路径: {self.output_file_path}")
        self.excel_df.to_excel(self.output_file_path, index=False)
        self.logger.info("Excel文件保存成功.")

    def process(self):
        """执行整个处理流程"""
        try:
            self.read_excel()
            self.replace_codes()
            self.save_to_excel()
            self.logger.info("码值替换过程完成.")
        except Exception as e:
            self.logger.error(f"处理过程中发生错误: {e}")

# 使用示例
if __name__ == "__main__":
    # 配置文件路径和输出文件路径
    excel_file_path = 'test_excel_file.xlsx'
    output_file_path = 'output_excel_file.xlsx'

    # 设置日志记录器
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # 创建类实例并处理
    replacer = ExcelCodeReplacer(excel_file_path, output_file_path, logger)

    replacer.process()


# ===========================
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



# ==================================================
#!/bin/bash

# 定义源目录和目标目录
src_dir="/data/script/python"
dest_dir="/data/script/python/bak"

# 获取今天的日期，格式为YYYYMMDD
today=$(date +%Y%m%d)

# 进入源目录
cd $src_dir

# 移动今天之前的所有日志文件
find . -type f -name "etl_*.log" -mtime +0 -exec mv {} $dest_dir \;

echo "所有今天之前的日志文件已移动到 $dest_dir"

