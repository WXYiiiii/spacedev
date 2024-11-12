import csv
import time
import polars as pl
import requests
import xml.etree.ElementTree as ET

class PolarsUtil:
    def __init__(self):
        self.local_interface_url = 'http://localhost:8081/public/interface/urlManage'
        self.file_path = '/data/tmp/xtcpjbxx_12_68_2000.csv'
        self.output_file_path = '/data/tmp/xtcpjbxx_12_68_2000_output.csv'
        self.classpath = '/home/dspetl/tmp/lilm/CtrcSpringBoot.jar'
        self.v_etl_dt = None
        self.df_gl_fmdb = None  # DataFrame 日历信息，来源于数据库查询
        self.df_task = None  # DataFrame 任务配置信息
        self.temp_task_code = None  # 作业编号
        self.temp_task_name = None  # 作业名称
        self.temp_freq = None  # 频次
        self.temp_execute_range = ''  # 报告数据区间，curr_range：etl_dt所在区间。next_range：etl_dt的上个区间
        self.temp_offset_type = None  # 偏移日期的类型 workday：工作日。calendar day：自然日
        self.temp_offset_days = None  # 偏移量
        self.temp_execute_date_type = None  # 执行日期的类型 workday：工作日。calendar_day：自然日

        self.column_names = [
            'col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7', 'col_8',
            'col_9', 'col_10', 'col_11', 'col_12', 'col_13', 'col_14', 'col_15',
            'col_16', 'col_17', 'col_18', 'col_19', 'col_20', 'col_21', 'col_22',
            'col_23', 'col_24', 'col_25', 'col_26', 'col_27', 'col_28', 'col_29',
            'col_30', 'col_31', 'col_32', 'col_33', 'col_34', 'col_35', 'col_36',
            'col_37', 'col_38', 'col_39', 'col_40', 'col_41', 'col_42', 'col_43',
            'col_44', 'col_45', 'col_46', 'col_47', 'col_48', 'col_49', 'col_50',
            'col_51', 'col_52', 'col_53', 'col_54', 'col_55', 'col_56',
            'col_57', 'col_58', 'col_59', 'col_60',
            'col_61', 'col_62', 'col_63'
        ]

        self.MainClass = None
        self.byte_array_output_stream = None
        self.java_system = None

    def process_large_file_in_batches(self):
        with open(self.output_file_path, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            with_header = True

            schema = pl.Schema(dict(zip(self.column_names, [pl.Utf8] * len(self.column_names))))
            seen_groups = set()
            v_batch_size = 1000  # 每个线程读取的行数

            reader = pl.read_csv_batched(
                source=self.file_path,
                batch_size=v_batch_size,
                separator=chr(1),
                schema_overrides=schema
            )

            batches = reader.next_batches(4)  # 线程数

            while batches:
                print('---------------------------------------------------')
                df_current_batches = pl.concat(batches)
                print(f'df_current_batches 行数 {df_current_batches.shape[0]}')

                df_batch_sm = df_current_batches.filter(pl.col('col_17') == '私募')
                print(f'df_batch_sm 行数 {df_batch_sm.shape[0]}')

                df_batch_not_sm = df_current_batches.filter(pl.col('col_17') != '私募')
                print(f'df_batch_not_sm 行数 {df_batch_not_sm.shape[0]}')

                df_batch_sm = self.sm4(df_batch_sm)
                print('df合并')

                df_batch_result = pl.concat([df_batch_sm, df_batch_not_sm], rechunk=True)
                print(f'df_batch_result 行数 {df_batch_result.shape[0]}')

                print('输出到csv')
                self.write_df_to_csv(writer, df_batch_result, with_header)
                with_header = False

                batches = reader.next_batches(4)  # 线程数
                print('---------------------------------------------------')

    def sm4(self, df_batch_sm):
        strs = df_batch_sm['col_6'].to_list()
        xtcpdm_data = ", ".join(strs)
        print(f'明文 len {len(xtcpdm_data)}')

        sm4_data_str = self.encrypt_by_post(xtcpdm_data)

        if len(xtcpdm_data) > len(sm4_data_str):
            print(f'【error】 {sm4_data_str}')

        df_batch_sm = df_batch_sm.with_columns(pl.Series('col6', sm4_data_str.split(', '))
                                               )
        return df_batch_sm

    def encrypt_by_post(self, xtcpdm_data):
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

        headers = {'Content-Type': 'text/plain'}
        response = requests.post(self.local_interface_url, data=request_message, headers=headers)

        response_str = response.text
        root = ET.fromstring(response_str)

        sm4_data_str = root.find('.//result').text
        return sm4_data_str

    def write_df_to_csv(self, writer, df_batch_sm, with_header):
        data = df_batch_sm.rows()

        if with_header:
            writer.writerow(df_batch_sm.columns)

        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    v_etl_dt = None  # sys.argv[1]
    obj = PolarsUtil()
    obj.v_etl_dt = v_etl_dt

    start_time = time.time()
    obj.process_large_file_in_batches()
    end_time = time.time()

    print(f'耗时 {end_time - start_time} 秒')