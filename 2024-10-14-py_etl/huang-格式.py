import pandas as pd
import logging

class ExcelCodeReplacer:
    def __init__(self, connection, excel_file_path, output_file_path, subject_id, logger=None):
        self.connection = connection
        self.excel_file_path = excel_file_path
        self.output_file_path = output_file_path
        self.subject_id = subject_id  # 新增的 subject_id 参数
        self.config_df = None
        self.excel_df = None
        self.logger = logger or logging.getLogger(__name__)  # 使用传入的 logger，或创建一个默认 logger

    def read_config_table(self):
        """读取MySQL配置表，仅选择指定的 subject_id"""
        query = f"""
            SELECT column_name, code_value, code_name 
            FROM config_table 
            WHERE column_type = 'dict' AND subject_id = '{self.subject_id}'
        """
        self.logger.info("正在读取配置表，subject_id: %s", self.subject_id)
        self.config_df = pd.read_sql(query, self.connection)
        self.logger.info("配置表读取成功，共有 %d 条记录.", len(self.config_df))

    def read_excel(self):
        """读取Excel文件，指定字段名称在第二行"""
        self.logger.info("正在从路径读取Excel文件: %s", self.excel_file_path)
        self.excel_df = pd.read_excel(self.excel_file_path, header=1)  # header=1表示第二行作为列名
        self.logger.info("Excel文件读取成功，共有 %d 行.", len(self.excel_df))

    def replace_codes(self):
        """替换Excel中的码值"""
        # 为每个column_name创建独立的字典
        dictionaries = {}

        for _, row in self.config_df.iterrows():
            column_name = row['column_name']
            code_value = row['code_value']
            code_name = row['code_name']

            # 如果该column_name还没有字典，则初始化一个新的字典
            if column_name not in dictionaries:
                dictionaries[column_name] = {}

            # 将码值和名称添加到对应字段的字典中
            dictionaries[column_name][code_value] = code_name

        # 替换Excel中的码值
        for column in dictionaries.keys():
            if column in self.excel_df.columns:
                self.logger.info("正在替换列中的码值: %s", column)
                self.excel_df[column] = self.excel_df[column].apply(
                    lambda x: ','.join(dictionaries[column].get(code.strip(), code.strip()) for code in x.split(',')) if pd.notnull(x) else x
                )
                self.logger.info("列 %s 的替换完成.", column)

    def save_to_excel(self):
        """保存替换后的Excel文件"""
        if self.output_file_path == self.excel_file_path:
            raise ValueError("输出文件路径不能与输入文件路径相同.")

        self.logger.info("正在保存更新后的Excel文件到路径: %s", self.output_file_path)
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
            self.logger.error("处理过程中发生错误: %s", e)


# 使用示例
if __name__ == "__main__":
    import mysql.connector

    # 创建数据库连接
    connection = mysql.connector.connect(
        host='your_host',
        user='your_user',
        password='your_password',
        database='your_database'
    )

    # 配置文件路径和输出文件路径
    excel_file_path = 'path_to_your_excel_file.xlsx'
    output_file_path = 'path_to_output_excel_file.xlsx'

    # 指定要处理的 subject_id
    subject_id = 'ads_bam_new_product'  # 替换为实际的 subject_id

    # 设置日志记录器
it

    # 创建类实例并处理
    replacer = ExcelCodeReplacer(connection, excel_file_path, output_file_path, subject_id, logger)

    try:
        replacer.process()
    finally:
        connection.close()  # 确保在处理完成后关闭连接