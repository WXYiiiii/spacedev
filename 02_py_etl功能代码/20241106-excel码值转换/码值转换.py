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