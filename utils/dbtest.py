# 连接数据源测试
import mysql.connector
import pymssql
from mysql.connector import Error

# 数据库连接测试
def db_test(dbtype, host, port, database, username, password):
    if dbtype == 'MySQL':
        return mysql_connection(host, port, database, username, password)
    elif dbtype == 'SQLServer':
        return sqlserver_connection(host, port, database, username, password)

# 连接MySQL
def mysql_connection(host, port, database, username, password):
    """
    测试MySQL数据库连接
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        
        if connection.is_connected():
            # 获取数据库信息
            '''
            db_info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            
            print(f"连接成功！MySQL服务器版本: {db_info}")
            print(f"当前数据库: {db_name[0]}")
            
            cursor.close()
            '''
            connection.close()
            return True, "连接成功"
        else:
            return False, "连接失败"
    except Error as e:
        return False, f"连接错误: {str(e)}"

# 连接SQLServer
def sqlserver_connection(host, port, database, username, password):
    """
    测试SQLServer数据库连接
    """
    try:
        connection = pymssql.connect(
            server=host,
            port=port,
            user=username,
            password=password,
            database=database,
            charset='UTF-8'
        )
        if connection:
            '''
            cursor = connection.cursor()
            cursor.execute("SELECT DB_NAME()")
            result = cursor.fetchone()
            print("当前数据库:", result[0])
            '''
            connection.close()
            return True, "连接成功"
        else:
            return False, "连接失败"
    except pymssql.Error as e:
        return False, f"连接错误: {e}"

