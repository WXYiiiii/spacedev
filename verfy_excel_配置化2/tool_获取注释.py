# 定义包含表结构的字符串
table_structure = """
year_week_id TEXT (32), -- 周ID
start_date NUMERIC, --开始日期
end_date NUMERIC, --结束日期
order_idx INTEGER, --排序ID
item_id TEXT(32), --项目 ID
prod_qty INTEGER, --个数 （个）
prod_pct REAL(24,6), --个数占比 （%）
prod_wow_change INTEGER, --个数环比增量 （个）
prod_wow_ratio REAL (24,6), --个数环比 （%）
prod_yoy_change INTEGER, --个数同比增量 （个）
prod_yoy_ratio REAL (24, 6), --个数同比 （%）
prod_1st_quartile INTEGER, --个数第一四分位数 （个）
prod_2nd_quartile INTEGER, --个数第二四分位数 （个）
prod_3rd_quartile INTEGER,--个数第三四分位数 （个）
prod_top5_tot INTEGER ,--个数前五名机构合计数量 （个）
prod_top5_pct REAL (24 ,6), --个数前五名机构合计占比 （%）
payin_trust_scale_100m REAL (24,6), --实收信托规模 （亿元）
trust_scale_pct REAL(24,6), --规模占比 （%）
scale_wow_change REAL (24, 6), --规模环比增量 （亿元)
scale_wow_ratio REAL (24,6), --规模环比 （%）
scale_yoy_change REAL (24, 6), --规模同比增量 （亿元）
scale_yoy_ratio REAL (24,6) ,--规模同比 （%）
scale_1st_quartile REAL (24 ,6), --规模第一四分位数 （亿元）
scale_2nd_quartile REAL (24 , 6), --规模第二 四分位数 （亿元）
scale_3rd_quartile REAL (24, 6),-- 规模第三四分位数 （亿元）
scale_top5_tot INTEGER, --规模前五名机构合计数量 （个）
scale_top5_pct REAL (24, 6), --规模前五名机构合计占比 （%）
issuing_org_qty INTEGER, --参与发行机构 （家）
issuing_org_wow_change INTEGER, --机构环比增量 （家）
issuing_org_wow_ratio REAL (24,6), --机构环比 （%）
"""

# 提取注释内容的函数
def extract_comments(table_structure):
    comments = []
    for line in table_structure.strip().split('\n'):
        # 查找注释部分
        if '--' in line:
            # 提取并去除前后空格
            comment = line.split('--')[1].strip()
            comments.append(comment)
    return comments

# 获取注释并打印
comments = extract_comments(table_structure)
for comment in comments:
    print(comment)


'''
周ID
开始日期
结束日期

排序ID
项目 ID
个数 （个）
个数占比 （%）
个数环比增量 （个）
个数环比 （%）
个数同比增量 （个）
个数同比 （%）
个数第一四分位数 （个）
个数第二四分位数 （个）
个数第三四分位数 （个）
个数前五名机构合计数量 （个）
个数前五名机构合计占比 （%）
实收信托规模 （亿元）
规模占比 （%）
规模环比增量 （亿元)
规模环比 （%）
规模同比增量 （亿元）
规模同比 （%）
规模第一四分位数 （亿元）
规模第二 四分位数 （亿元）
规模第三四分位数 （亿元）
规模前五名机构合计数量 （个）
规模前五名机构合计占比 （%）
参与发行机构 （家）
机构环比增量 （家）
机构环比 （%）
'''