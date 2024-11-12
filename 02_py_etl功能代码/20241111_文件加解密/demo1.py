import csv
import time
import polars as pl
import requests
import xml.etree.ElementTree as ET

class PolarsUtil:
    def __init__(self):
        # 初始化属性，包括接口 URL、输入输出文件路径和列名等
        self.local_interface_url = 'http://localhost:8081/public/interface/urlManage'
        self.file_path = '/data/tmp/xtcpjbxx_12_68_2000.csv'
        self.output_file_path = '/data/tmp/xtcpjbxx_12_68_2000_output.csv'

        # 列名定义
        self.column_names = [
            'col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7', 'col_8',
            'col_9', 'col_10', 'col_11', 'col_12', 'col_13', 'col_14', 'col_15',
            'col_16', 'col_17', 'col_18', 'col_19', 'col_20', 'col_21', 'col_22',
            'col_23', 'col_24', 'col_25', 'col_26', 'col_27', 'col_28', 'col_29',
            'col_30', 'col_31', 'col_32', 'col_33', 'col_34', 'col_35', 'col_36',
            'col_37', 'col_38', 'col_39', 'col_40', 'col_41', 'col_42', 'col_43',
            'col_44', 'col_45', 'col_46', 'col_47', 'col_48', 'col_49', 'col_50',
            'col_51', 'col_52', 'col_53', 'col_54', 'col_55', 'col_56',
            'col_57', 'col_58', 'col_59',
            'col_60',' col61',' col62',' col63'
        ]

    def process_large_file_in_batches(self):
        # 打开输出文件以写入处理结果
        with open(self.output_file_path, mode='w+', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)  # 创建 CSV 写入器
            with_header = True  # 标记是否写入表头

            # 定义数据模式以便于读取 CSV 文件
            schema = pl.Schema(dict(zip(self.column_names, [pl.Utf8] * len(self.column_names))))

            # 设置批处理大小
            v_batch_size = 1000  # 每个线程读取的行数

            # 按批次读取 CSV 文件
            reader = pl.read_csv_batched(
                source=self.file_path,
                batch_size=v_batch_size,
                separator=chr(1),  # 使用特定字符作为分隔符
                schema_overrides=schema  # 应用模式覆盖
            )

            batches = reader.next_batches(4)  # 获取初始批次（线程数为4）

            while batches:  # 当还有批次可处理时
                print('---------------------------------------------------')

                # 合并当前批次的数据为一个 DataFrame
                df_current_batches = pl.concat(batches)
                print(f'df_current_batches 行数 {df_current_batches.shape[0]}')

                # 对“证件”列进行加密，仅在“类型”列为“个人”的情况下
                df_current_batches = self.encrypt_certificates(df_current_batches)

                print('输出到csv')
                self.write_df_to_csv(writer, df_current_batches, with_header)  # 写入 CSV 文件
                with_header = False  # 后续批次不再写入表头

                batches = reader.next_batches(4)  # 获取下一个批次（线程数为4）
                print('---------------------------------------------------')

    def encrypt_certificates(self, df):
        # 对传入的 DataFrame 中的“证件”列进行加密处理，仅在“类型”为“个人”时加密
        certificate_column = df['col6']  # 假设“证件”在第6列（即' col6'）
        type_column = df['类型']  # 假设“类型”列名为'类型'

        encrypted_certificates = []

        for cert, type_value in zip(certificate_column, type_column):
            if type_value == "个人":
                encrypted_cert = self.encrypt_by_post(cert)  # 加密证件信息
                encrypted_certificates.append(encrypted_cert)
            else:
                encrypted_certificates.append(cert)  # 保持原值

        df = df.with_columns(pl.Series('证件加密后列名' , encrypted_certificates))  # 更新 DataFrame 中的证件列
        return df

    def encrypt_by_post(self, xtcpdm_data):
        # 构造 XML 请求消息并发送到接口进行加密处理
        request_message = f"""<service>
            <Head>
                <SvcCd>PDGP001</SvcCd>
                <PlaintextMaxLength>10000</PlaintextMaxLength>
                <ResultByteMaxLength>40000</ResultByteMaxLength>
            </Head>
            <Body>
                <Data>{xtcpdm_data}</Data>
            </Body>
        </service>"""

        headers = {'Content-Type': 'text/plain'}  # 设置请求头信息

        response = requests.post(self.local_interface_url, data=request_message, headers=headers)  # 发送 POST 请求

        response_str = response.text  # 获取响应文本

        root = ET.fromstring(response_str)  # 将响应解析为 XML 格式

        sm4_data_str = root.find('.//result').text  # 提取加密结果
        return sm4_data_str

    def write_df_to_csv(self, writer, df, with_header):
        # 将 DataFrame 写入 CSV 文件中
        data = df.rows()  # 获取 DataFrame 中的所有行

        if with_header:
            writer.writerow(df.columns)  # 如果需要，写入表头

        for row in data:
            writer.writerow(row)  # 写入每一行数据


if __name__ == "__main__":
    v_etl_dt = None  # sys.argv[1]  # 从命令行获取 ETL 日期（目前未使用）
    obj = PolarsUtil()  # 创建 PolarsUtil 实例

    start_time = time.time()  # 开始计时
    obj.process_large_file_in_batches()  # 调用处理方法
    end_time = time.time()  # 结束计时

    print(f'耗时 {end_time - start_time} 秒')  # 打印程序运行时间