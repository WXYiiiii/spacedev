import sqlite3

# 创建SQLite数据库并连接
def create_database(db_name='project_data.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 创建表格：项目ID，个数，规模，个数占比
    cursor.execute('''
    drop table if exists project_data
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS project_data (
        project_id INTEGER PRIMARY KEY,
        count INTEGER,
        scale REAL,
        count_ratio REAL
    )
    ''')

    # 插入模拟数据
    data = [
        (1, 100, 5000.0, 0.2),
        (2, 200, 10000.0, 0.4),
        (3, 150, 7500.0, 0.3),
        (4, 50, 2500.0, 0.1)
    ]

    cursor.executemany('''
    INSERT INTO project_data (project_id, count, scale, count_ratio)
    VALUES (?, ?, ?, ?)
    ''', data)

    conn.commit()
    conn.close()

# 查询数据并打印
def query_database(db_name='project_data.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM project_data')
    rows = cursor.fetchall()

    for row in rows:
        # print(f"Project ID: {row[0]}, Count: {row[1]}, Scale: {row[2]}, Count Ratio: {row[3]}")
        print(f" {row[0]}, {row[1]}, {row[2]}, {row[3]}")

    conn.close()

# 主函数
if __name__ == "__main__":
    create_database()  # 创建新的数据库
    query_database()    # 查询并打印数据