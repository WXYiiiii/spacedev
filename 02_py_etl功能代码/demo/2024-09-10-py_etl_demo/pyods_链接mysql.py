# 通过odbc连接mysql
import pyodbc

def connect_mysql_odbc(server, database, username, password, driver='{MySQL ODBC 8.0 Unicode Driver}'):
    """
    通过ODBC连接MySQL数据库
    
    参数:
    server (str): MySQL服务器地址
    database (str): 数据库名称
    username (str): 用户名
    password (str): 密码
    driver (str): ODBC驱动名称，默认为MySQL ODBC 8.0 Unicode Driver
    
    返回:
    pyodbc.Connection: 数据库连接对象
    """
    connection_string = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )
    
    try:
        conn = pyodbc.connect(connection_string)
        print("成功连接到MySQL数据库")
        return conn
    except pyodbc.Error as e:
        print(f"连接MySQL数据库失败: {str(e)}")
        return None

# 使用示例
if __name__ == "__main__":
    conn = connect_mysql_odbc(
        server="localhost",
        database="your_database",
        username="your_username",
        password="your_password"
    )
    
    if conn:
        # 在这里执行数据库操作
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM your_table")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        
        # 关闭连接
        conn.close()
