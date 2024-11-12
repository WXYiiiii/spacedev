import pandas as pd
import logging
import mysql.connector

class ExcelCodeReplacer:
    def __init__(self, connection, excel_file_path, output_file_path, subject_id, logger=None):
        self.connection = connection
        self.excel_file_path = excel_file_path
        self.output_file_path = output_file_path
        self.subject_id = subject_id
        self.config_data = []  # 使用列表来存储配置数据
        self.excel_df = None
        self.logger = logger or logging.getLogger(__name__)

    def read_config_table(self):
        """读取MySQL配置表，仅选择指定的 subject_id"""
        query = """
            SELECT column_name, code_value, column_comment AS code_name 
            FROM config_table 
            WHERE column_type = 'dict' AND subject_id = %s
        """
        self.logger.info(f"正在读取配置表，subject_id: {self.subject_id}")

        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.subject_id,))
            # 获取所有结果
            self.config_data = cursor.fetchall()

        self.logger.info(f"配置表读取成功，共有 {len(self.config_data)} 条记录.")

    def read_excel(self):
        """读取Excel文件，指定字段名称在第二行"""
        self.logger.info(f"正在从路径读取Excel文件: {self.excel_file_path}")
        self.excel_df = pd.read_excel(self.excel_file_path, header=0)
        self.logger.info(f"Excel文件读取成功，共有 {len(self.excel_df)} 行.")

    def replace_codes(self):
        """替换Excel中的码值"""
        dictionaries = {}

        for row in self.config_data:
            column_name, code_value, code_name = row  # 解包元组

            if column_name not in dictionaries:
                dictionaries[column_name] = {}

            dictionaries[column_name][code_value] = code_name

        for column in dictionaries.keys():
            if column in self.excel_df.columns:
                self.logger.info(f"正在替换列中的码值: {column}")
                # 使用 replace 方法进行替换
                self.excel_df[column] = self.excel_df[column].replace(dictionaries[column])
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
            self.read_config_table()
            self.read_excel()
            self.replace_codes()
            self.save_to_excel()
            self.logger.info("码值替换过程完成.")
        except Exception as e:
            self.logger.error(f"处理过程中发生错误: {e}")

# 使用示例
if __name__ == "__main__":
    # 创建数据库连接
    connection = mysql.connector.connect(
        host='localhost',
        user='your_user',
        password='your_password',
        database='test_db'
    )

    # 配置文件路径和输出文件路径
    excel_file_path = 'test_excel_file.xlsx'
    output_file_path = 'output_excel_file.xlsx'

    # 指定要处理的 subject_id
    subject_id = 'ads_bam_new_product'

    # 设置日志记录器
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # 创建类实例并处理
    replacer = ExcelCodeReplacer(connection, excel_file_path, output_file_path, subject_id, logger)

    try:
        replacer.process()
    finally:
        connection.close()  # 确保在处理完成后关闭连接