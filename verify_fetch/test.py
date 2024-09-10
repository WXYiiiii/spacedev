import sqlite3
import random
import string
from memory_profiler import profile

# 创建一个模拟数据库并插入大量数据
def create_database():
    conn = sqlite3.connect('example.db')
#     cursor = conn.cursor()
#     cursor.execute('CREATE TABLE IF NOT EXISTS your_table (id INTEGER PRIMARY KEY, name TEXT)')
#
#     # 插入大量数据（模拟4GB的数据）
#     for _ in range(1000000):  # 插入100万条记录
#         name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # 随机生成名字
#         cursor.execute('INSERT INTO your_table (name) VALUES (?)', (name,))
#
#     conn.commit()
#     conn.close()

@profile
def fetch_data():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table")

    while True:
        rows = cursor.fetchmany(5)  # 每次提取5行
        if not rows:  # 如果没有更多行，退出循环
            break
        # 处理每一行（这里只是打印行数，不打印具体内容）
        print(f"Fetched {len(rows)} rows")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database()  # 创建数据库并插入数据
    fetch_data()       # 提取数据并监控内存使用