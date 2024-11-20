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

        self.column_names = [
            'col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7', 'col_8',
            'col_9', 'col_10', 'col_11', 'col_12', 'col_13', 'col_14', 'col_15',
            'col_16', 'col_17', 'col_18', 'col_19', 'col_20', 'col_21', 'col_22',
            'col_23', 'col_24', 'col_25', 'col_26', 'col_27', 'col_28', 'col_29',
            'col_30', 'col_31', 'col_32', 'col_33', 'col_34', 'col_35', 'col_36',
            'col_37', 'col_38', 'col_39', 'col_40', 'col_41', 'col_42', 'col_43',
            'col_44', 'col_45', 'col_46', 'col_47', 'col_48', 'col_49', 'col_50',
            # Add more columns as necessary
        ]

    def process_large_file_in_batches(self):
        with open(self.output_file_path, mode='w+', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            with_header = True

            schema = pl.Schema(dict(zip(self.column_names, [pl.Utf8] * len(self.column_names))))
            v_batch_size = 1000

            reader = pl.read_csv_batched(
                source=self.file_path,
                batch_size=v_batch_size,
                separator=chr(1),
                schema_overrides=schema
            )

            batches = reader.next_batches(4)

            while batches:
                print('---------------------------------------------------')

                df_current_batches = pl.concat(batches)
                print(f'df_current_batches 行数 {df_current_batches.shape[0]}')

                # 添加索引列以保持原始顺序
                df_current_batches = df_current_batches.with_row_index(name='index')

                # 根据条件过滤出“私募”数据
                df_batch_sm = df_current_batches.filter(pl.col('col_17') == '私募')
                print(f'df_batch_sm 行数 {df_batch_sm.shape[0]}')

                # 过滤出非“私募”数据
                df_batch_not_sm = df_current_batches.filter(pl.col('col_17') != '私募')
                print(f'df_batch_not_sm 行数 {df_batch_not_sm.shape[0]}')

                # 对“私募”数据进行 SM4 加密处理
                df_batch_sm = self.sm4(df_batch_sm)

                print('df合并')

                # 合并加密后的数据和未加密的数据，并保持原始顺序
                df_batch_result = pl.concat([df_batch_sm, df_batch_not_sm], rechunk=True)

                # 根据索引重新排序，以保持原始顺序
                df_batch_result = df_batch_result.sort('index')
                df_batch_result = df_batch_result.drop('index')

                print(f'df_batch_result 行数 {df_batch_result.shape[0]}')

                print('输出到csv')
                self.write_df_to_csv(writer, df_batch_result, with_header)
                with_header = False

                batches = reader.next_batches(4)
                print('---------------------------------------------------')

    def sm4(self, df_batch_sm, en_col_name):
        strs = df_batch_sm[en_col_name].to_list()
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
    v_etl_dt = None
    obj = PolarsUtil()

    start_time = time.time()
    obj.process_large_file_in_batches()
    end_time = time.time()

    print(f'耗时 {end_time - start_time} 秒')