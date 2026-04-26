# SQL语句安全性检查
import re
import sqlparse
from typing import Tuple

class SQLSecurityChecker:
    def __init__(self):
        '''
        self.dangerous_keywords = [
            'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE',
            'TRUNCATE', 'EXEC', 'EXECUTE', 'MERGE', 'REPLACE', 'GRANT',
            'REVOKE', 'COMMIT', 'ROLLBACK', 'SAVEPOINT', 'LOCK', 'UNLOCK'
        ]
        '''
        self.dangerous_keywords = [
            'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE',
            'TRUNCATE', 'EXEC', 'EXECUTE', 'MERGE', 'GRANT',
            'REVOKE', 'COMMIT', 'ROLLBACK', 'SAVEPOINT', 'LOCK', 'UNLOCK'
        ]
        
        self.dangerous_functions = [
            'SLEEP', 'BENCHMARK', 'LOAD_FILE', 'UPDATEXML', 'EXTRACTVALUE',
            'PG_SLEEP', 'WAITFOR', 'GET_LOCK'
        ]
    
    def check_sql_security(self, sql: str):
        """
        综合检查SQL语句安全性
        """
        # 基础检查
        safe, message = self._basic_checks(sql)
        if not safe:
            return False, message
        
        # 语法检查
        safe, message = self._syntax_checks(sql)
        if not safe:
            return False, message
        
        # 模式检查
        safe, message = self._pattern_checks(sql)
        if not safe:
            return False, message
        
        return True, "SQL语句安全"
    
    def _basic_checks(self, sql: str) -> Tuple[bool, str]:
        """基础检查"""
        sql_upper = sql.strip().upper()
        
        # 检查是否以SELECT开头
        if not sql_upper.startswith('SELECT'):
            return False, "只允许SELECT查询语句"
        
        # 检查危险关键字
        for keyword in self.dangerous_keywords:
            if re.search(r'\b' + keyword + r'\b', sql_upper):
                return False, f"检测到危险关键字: {keyword}"
        
        return True, "基础检查通过"
    
    def _syntax_checks(self, sql: str):
        """语法检查"""
        try:
            parsed = sqlparse.parse(sql)
            if not parsed:
                return False, "无法解析SQL语句"
            
            # 检查语句数量
            if len(parsed) > 1:
                return False, "不允许多个SQL语句"
            
            statement = parsed[0]
            
            # 检查语句类型
            if not statement.get_type() == 'SELECT':
                return False, "只允许SELECT语句"
            
            return True, "语法检查通过"
            
        except Exception as e:
            return False, f"SQL语法错误: {str(e)}"
    
    def _pattern_checks(self, sql: str):
        """模式检查"""
        sql_upper = sql.upper()
        
        # 检查危险函数
        for func in self.dangerous_functions:
            if re.search(r'\b' + func + r'\s*\(', sql_upper):
                return False, f"检测到危险函数: {func}"
        
        # 检查注释（可能用于注释绕过）
        if '--' in sql or '/*' in sql or '#' in sql:
            return False, "检测到SQL注释"
        
        # 检查分号（可能用于多语句执行）
        if sql.count(';') > 1:
            return False, "检测到多个分号"
        
        return True, "模式检查通过"

'''
# 使用示例
checker = SQLSecurityChecker()

# 测试安全SQL
safe_sql = "SELECT username, email FROM users WHERE status = 'active'"
result, message = checker.check_sql_security(safe_sql)
print(f"安全SQL: {result}, {message}")

# 测试危险SQL
dangerous_sql = "SELECT * FROM users; DROP TABLE users"
result, message = checker.check_sql_security(dangerous_sql)
print(f"危险SQL: {result}, {message}")
'''
