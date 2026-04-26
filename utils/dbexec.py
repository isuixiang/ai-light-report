# 连接数据库执行SQL语句
import mysql.connector
import pymssql
from mysql.connector import Error

# 数据库连接
def sql_exec(dbtype, host, port, database, username, password, sql):
    if dbtype == 'MySQL':
        return mysql_sql_exec(host, port, database, username, password, sql)
    elif dbtype == 'SQLServer':
        return sqlserver_sql_exec(host, port, database, username, password, sql)

# MySQL执行SQL语句
def mysql_sql_exec(host, port, database, username, password, sql):
    """
    MySQL执行SQL语句
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            results = cursor.fetchall()
            
            # 列名
            columns = [desc[0] for desc in cursor.description]
            
            # 数据列表
            records = [list(row.values()) for row in results]
            
            data = {
                'columns': columns,
                'records': records,
                'row_count': len(results)
            }
            
            cursor.close()
            connection.close()
            return True, data
        else:
            return False, "连接失败"
    except Error as e:
        return False, f"连接错误: {str(e)}"

# SQLServer执行SQL语句
def sqlserver_sql_exec(host, port, database, username, password, sql):
    """
    SQLServer执行SQL语句
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
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            results = cursor.fetchall()
            
            # 列名
            columns = [desc[0] for desc in cursor.description]
            
            # 数据列表
            records = [list(row.values()) for row in results]
            
            data = {
                'columns': columns,
                'records': records,
                'row_count': len(results)
            }
            
            cursor.close()
            connection.close()
            return True, data
        else:
            return False, "连接失败"
    except pymssql.Error as e:
        return False, f"连接错误: {e}"
