import sqlite3
import random
from datetime import datetime, timedelta

# 创建SQLite数据库并连接
def create_database(db_name='new_project_data.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 创建表格：项目ID，个数，规模，个数占比
    cursor.execute('''
    CREATE TABLE reg_init_indus_sum_wk(
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
    PRIMARY KEY (year_week_id , item_id )
    ); 
    ''')

    # 生成模拟数据
    data = []

    # 创建一些模拟数据
    for i in range(10):  # 假设我们生成10条数据
        year_week_id = f"2024-W{i+1}"
        start_date = (datetime.now() - timedelta(weeks=i)).date()
        end_date = start_date + timedelta(days=6)
        order_idx = i + 1
        item_id = f"item_{i+1}"
        prod_qty = random.randint(1000, 5000)  # 随机生成数量
        prod_pct = round(random.uniform(0.1, 1.0) * 100, 2)  # 随机生成占比
        prod_wow_change = random.randint(-100, 100)  # 环比增量
        prod_wow_ratio = round(random.uniform(-10.0, 10.0), 2)  # 环比百分比变化
        prod_yoy_change = random.randint(-200, 200)  # 同比增量
        prod_yoy_ratio = round(random.uniform(-20.0, 20.0), 2)  # 同比百分比变化

        # 四分位数和前五名统计数据
        quartiles = [random.randint(500, 3000) for _ in range(3)]
        prod_top5_tot = sum(sorted(quartiles)[-5:]) if len(quartiles) >= 5 else sum(quartiles)
        prod_top5_pct = round(prod_top5_tot / float(prod_qty) * 100 if prod_qty > 0 else 0.0, 2)

        payin_trust_scale_100m = round(random.uniform(10.0, 100.0), 2)
        trust_scale_pct = round(random.uniform(0.1, 1.0) * 100, 2)

        scale_wow_change = round(random.uniform(-50.0, 50.0), 2)
        scale_wow_ratio = round(random.uniform(-10.0, 10.0), 2)

        scale_yoy_change = round(random.uniform(-100.0, 100.0), 2)
        scale_yoy_ratio = round(random.uniform(-20.0, 20.0), 2)

        scale_quartiles = [round(random.uniform(5.0, 50.0), 2) for _ in range(3)]
        scale_top5_tot = sum(sorted(scale_quartiles)[-5:]) if len(scale_quartiles) >= 5 else sum(scale_quartiles)
        scale_top5_pct = round(scale_top5_tot / float(payin_trust_scale_100m) * 100 if payin_trust_scale_100m > 0 else 0.0, 2)

        issuing_org_qty = random.randint(1, 10)
        issuing_org_wow_change = random.randint(-2, 2)
        issuing_org_wow_ratio = round(random.uniform(-20.0, 20.0), 2)

        data.append((year_week_id,
                     start_date.isoformat(),
                     end_date.isoformat(),
                     order_idx,
                     item_id,
                     prod_qty,
                     prod_pct,
                     prod_wow_change,
                     prod_wow_ratio,
                     prod_yoy_change,
                     prod_yoy_ratio,
                     quartiles[0],
                     quartiles[1],
                     quartiles[2],
                     prod_top5_tot,
                     prod_top5_pct,
                     payin_trust_scale_100m,
                     trust_scale_pct,
                     scale_wow_change,
                     scale_wow_ratio,
                     scale_yoy_change,
                     scale_yoy_ratio,
                     scale_quartiles[0],
                     scale_quartiles[1],
                     scale_quartiles[2],
                     scale_top5_tot,
                     scale_top5_pct,
                     issuing_org_qty,
                     issuing_org_wow_change,
                     issuing_org_wow_ratio))

    cursor.executemany('''
    INSERT INTO reg_init_indus_sum_wk (
      year_week_id,
      start_date,
      end_date,
      order_idx,
      item_id,
      prod_qty,
      prod_pct,
      prod_wow_change,
      prod_wow_ratio,
      prod_yoy_change,
      prod_yoy_ratio,
      prod_1st_quartile,
      prod_2nd_quartile,
      prod_3rd_quartile,
      prod_top5_tot,
      prod_top5_pct,
      payin_trust_scale_100m,
      trust_scale_pct,
      scale_wow_change,
      scale_wow_ratio,
      scale_yoy_change,
      scale_yoy_ratio,
      scale_1st_quartile,
      scale_2nd_quartile,
      scale_3rd_quartile,
      scale_top5_tot,
      scale_top5_pct,
      issuing_org_qty,
      issuing_org_wow_change,
      issuing_org_wow_ratio
     )
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
     ''', data)

    conn.commit()
    conn.close()

# 查询数据并打印
def query_database(db_name='new_project_data.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM reg_init_indus_sum_wk')
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

# 主函数
if __name__ == "__main__":
    create_database()   # 创建新的数据库并插入数据
    query_database()     # 查询并打印数据