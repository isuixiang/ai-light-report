# 自定义错误码
class Error:
    SUCCESS = 200
    INVALID_TOKEN = 1001
    HAS_EXISTED = 1002
    SQL_FAILED = 1003
    UNSAFE_SQL = 1004
    NO_MATCH_ROWS = 1005
    OVER_MAX_ROWS = 1006
    NO_MATCH_CHART = 1007
    NO_MATCH_SKILLS = 1008
    INVALID_ACCOUNT_PWD = 2001
    INVALID_CAPTCHA = 2002
    ACCOUNT_DISABLED = 2003
    ACCOUNT_HAS_EXIST = 2004
    INVALID_PASSWORD = 2005
    DB_ERROR = 9991
    FILE_ERROR = 9992
    LLM_ERROR = 9993
    SQL_ERROR = 9994
    SYS_ERROR = 9999

    msg = {
        SUCCESS: 'success',
        INVALID_TOKEN: '无效令牌',
        HAS_EXISTED: '请不要重复添加',
        SQL_FAILED: '生成SQL失败',
        UNSAFE_SQL: '不安全的SQL语句',
        NO_MATCH_ROWS: '没有符合条件的记录',
        OVER_MAX_ROWS: '超过记录数限制',
        NO_MATCH_CHART: '没有可展示的图表',
        NO_MATCH_SKILLS: '未正确配置技能文档',
        INVALID_ACCOUNT_PWD: '账号或密码错误',
        INVALID_CAPTCHA: '验证码错误',
        ACCOUNT_DISABLED: '账号已禁用',
        ACCOUNT_HAS_EXIST: '账号已存在',
        INVALID_PASSWORD: '原密码错误',
        DB_ERROR: '数据库错误',
        FILE_ERROR: '读文件错误',
        LLM_ERROR: '接口调用错误',
        SQL_ERROR: 'SQL执行错误',
        SYS_ERROR: '系统异常'
    }