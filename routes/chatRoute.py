# route chat
from flask import Blueprint, request, json, jsonify, render_template
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from models.datasource import DataSource
from models.llm import Llm
from models.exceltemplate import ExcelTemplate
from models.chatmessage import ChatMessage
from models.skills import Skills
from utils.jwttoken import verify_token
from utils.error import Error
from utils.llmapi import llm_call, llm_chat_call
from utils.dbexec import sql_exec
from utils.sqlcheck import SQLSecurityChecker
from utils.logger import setup_logger
from utils.crypt import StringCrypto
from json import JSONDecodeError
from dotenv import load_dotenv
import re, os

chatRoute = Blueprint('chat', __name__)

# 读取配置参数
load_dotenv(override=True)

# 启动日志信息
logger = setup_logger()

# 解析json字符串
def parse_json(str):
    # 使用正则表达式提取 ```json 和 ``` 之间的内容
    if str.strip().startswith("```json"):
        match = re.search(r'```json\s*({.*?})\s*```', str, re.DOTALL)
        json_str = match.group(1)
    else:
        json_str = str

    # 解析成json对象
    try:
        return True, json.loads(json_str)
    except JSONDecodeError as e:
        return False, f"JSON解析错误: {e}"

# 替换SQL语句中的limit字符串
def ensure_limit_one(sql):
    """
    如果 SQL 语句中没有 LIMIT 子句，则在末尾添加 " LIMIT 1"；
    如果已有 LIMIT 子句，则将其替换为 " LIMIT 1"。
    忽略大小写，并处理可能存在的注释或换行。
    """
    # 使用正则表达式匹配 LIMIT 子句（不区分大小写）
    # (?i) 表示忽略大小写
    # \s* 匹配任意空白字符（包括换行）
    # (?:\d+)? 可选的数字（如 LIMIT 10）
    # (?:\s*,\s*\d+)? 可选的 OFFSET 部分（如 LIMIT 5,10 或 LIMIT 10 OFFSET 5）
    pattern = r'(?i)\s+LIMIT\s+(?:\d+\s*(?:,\s*\d+)?|OFFSET\s+\d+)(?:\s+|$)'
    
    # 查找是否已存在 LIMIT
    if re.search(pattern, sql):
        # 替换已有的 LIMIT 子句为 LIMIT 1
        # 注意：只替换最后一个 LIMIT（通常 SQL 中只应有一个）
        # 使用 sub 替换第一个匹配（从右往左更安全，但一般 LIMIT 在末尾）
        new_sql = re.sub(pattern, ' LIMIT 1', sql, count=1)
        return new_sql
    else:
        # 没有 LIMIT，直接在末尾添加
        return sql.rstrip().rstrip(';') + ' LIMIT 1'

# 一键生成报表定义
@chatRoute.route('/chat/fullsetting', methods=['POST'])
def chat_fullsetting():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    ds_id = data['ds_id']               # 数据源ID
    template_id = data['template_id']   # 模板ID
    llmname = data['llmname']           # 大模型名称

    # 取数据源记录
    datasource = DataSource.get(ds_id)
    db_type = datasource.db_type

    # 取模板记录
    exceltemplate = ExcelTemplate.get(template_id)
    pattern = exceltemplate.pattern

    # 判断是否配置了主技能
    mainskill = Skills.getMainSkill(ds_id)
    content = mainskill.content
    if not mainskill or not content:
        return jsonify({'code':Error.NO_MATCH_SKILLS, 'message':Error.msg[Error.NO_MATCH_SKILLS]})

    # 取大模型记录
    llm = Llm.getByName(llmname)
    apikey = llm.apikey
    if not llm or not apikey:
        return jsonify({'code':Error.SYS_ERROR, 'message':Error.msg[Error.SYS_ERROR]})

    # 提示词
    prompt_full_skills = os.getenv('PROMPT_FULL_SKILLS')
    prompt = prompt_full_skills.replace('{pattern}', pattern)

    # 第1步：加载主技能，调用大模型输出所需子技能
    result, response = llm_call(llmname, apikey, prompt, content)
    #print(result, response)
    logger.info(f"llm response step1: {response}")
    if result == False:
        return jsonify({'code':Error.LLM_ERROR, 'message':response})
    
    # 解析json数据
    result, json_data = parse_json(response)
    if not result:
        return jsonify({'code':Error.SYS_ERROR, 'message':json_data})
    
    # 第2步：加载所需技能，调用大模型输出SQL语句
    required_skills =  json_data['required_skills']
    #print(required_skills)
    file_content = f"{content}"
    for item in required_skills:
        name, _ = os.path.splitext(item)
        subskill = Skills.getSubSkill(ds_id, type=2, name=name)
        file_content = f"{file_content}\n\n{subskill.content}"
    
    # 通用技能
    commonskills = Skills.getCommonSkills(ds_id)
    for item in commonskills:
        file_content = f"{file_content}\n\n{item.content}"
    #print(file_content)

    # 提示词
    prompt_full_sqls = os.getenv('PROMPT_FULL_SQLS')
    prompt = prompt_full_sqls.replace('{pattern}', pattern).replace('{dbtype}', db_type)

    result, response = llm_call(llmname, apikey, prompt, file_content)
    #print(result, response)
    logger.info(f"llm response step2: {response}")
    if result == False:
        return jsonify({'code':Error.LLM_ERROR, 'message':response})
    
    # 解析json数据
    result, json_data = parse_json(response)
    if not result:
        return jsonify({'code':Error.SYS_ERROR, 'message':json_data})
    
    #print(json_data)
    
    # 生成SQL失败
    if (not json_data or len(json_data) == 0):
        return jsonify({'code':Error.SQL_FAILED, 'message':Error.msg[Error.SQL_FAILED]})
    
    try:
        # JSON转字符串
        content_string = json.dumps(json_data, ensure_ascii=False, indent=4)

        # 更新模板定义
        ExcelTemplate.updateContent(template_id, content_string)

        # 取报表定义
        exceltemplate = ExcelTemplate.get(template_id)
        
        # JSON序列化
        data_dict = exceltemplate.to_dict()
        
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'data':data_dict})
    except SQLAlchemyError as e:
        #print(f"chat_fullsetting error: {e}")
        logger.error(f"chat_fullsetting error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 发送聊天
@chatRoute.route('/chat/sendmessage', methods=['POST'])
def chat_sendmessage():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    ds_id = data['ds_id']               # 数据源ID
    llmname = data['llmname']           # 大模型名称
    message = data['message']

    # 取数据源记录
    datasource = DataSource.get(ds_id)
    db_type = datasource.db_type
    db_host = datasource.db_host
    db_port = datasource.db_port
    db_name = datasource.db_name
    db_user = datasource.db_user
    db_password = datasource.db_password

    # 解密数据库用户密码
    secret_key = os.getenv('SECRET_KEY')
    salt_key = os.getenv('SALT_KEY')
    crypto = StringCrypto(secret_key, salt_key)
    success, msg = crypto.decrypt(db_password)
    if not success:
        return jsonify({'code':Error.SYS_ERROR, 'message':msg})
    dbpassword_decrypt = msg

    # 判断是否配置了主技能
    mainskill = Skills.getMainSkill(ds_id)
    content = mainskill.content
    if not mainskill or not content:
        return jsonify({'code':Error.NO_MATCH_SKILLS, 'message':Error.msg[Error.NO_MATCH_SKILLS]})

    # 取大模型记录
    llm = Llm.getByName(llmname)
    apikey = llm.apikey
    if not llm or not apikey:
        return jsonify({'code':Error.SYS_ERROR, 'message':Error.msg[Error.SYS_ERROR]})

    # 提示词
    prompt_skills = os.getenv('PROMPT_SKILLS')
    prompt = prompt_skills.replace('{message}', message)

    # 第1步：加载主技能，调用大模型输出所需子技能
    result, response = llm_call(llmname, apikey, prompt, content)
    #print(result, response)
    logger.info(f"step1 [get subskills]: {response}")
    if result == False:
        return jsonify({'code':Error.LLM_ERROR, 'message':response})
    
    # 解析json数据
    result, json_data = parse_json(response)
    if not result:
        return jsonify({'code':Error.SYS_ERROR, 'message':json_data})
    
    # 第2步：加载所需技能，调用大模型输出SQL语句
    required_skills =  json_data['required_skills']
    #print(required_skills)
    file_content = f"{content}"
    for item in required_skills:
        name, _ = os.path.splitext(item)
        subskill = Skills.getSubSkill(ds_id, type=2, name=name)
        file_content = f"{file_content}\n\n{subskill.content}"
    
    # 通用技能
    commonskills = Skills.getCommonSkills(ds_id)
    for item in commonskills:
        file_content = f"{file_content}\n\n{item.content}"
    #print(file_content)

    # 提示词
    prompt_sql = os.getenv('PROMPT_SQL')
    prompt = prompt_sql.replace('{message}', message).replace('{dbtype}', db_type)

    result, response = llm_call(llmname, apikey, prompt, file_content)
    #print(result, response)
    logger.info(f"step2 [get sql]: {response}")
    if result == False:
        return jsonify({'code':Error.LLM_ERROR, 'message':response})
    
    # 解析json数据
    result, json_data = parse_json(response)
    if not result:
        return jsonify({'code':Error.SYS_ERROR, 'message':json_data})
    
    # SQL语句和标题
    sql_statement = json_data['sql_statement']
    
    # 生成SQL失败
    if (sql_statement == None or sql_statement == ''):
        return jsonify({'code':Error.SQL_FAILED, 'message':Error.msg[Error.SQL_FAILED]})
    
    try:
        # 验证SQL执行是否报错，报错则修复（循环3次直到没有报错）
        for i in range(3):
            new_sql_statement = ensure_limit_one(sql_statement)
            success, results = sql_exec(db_type, db_host, db_port, db_name, db_user, dbpassword_decrypt, new_sql_statement)
            if not success:
                # 再次调用大模型生成SQL
                prompt = f"{prompt}\n\nSQL语句执行时报错，错误信息`{results}`，请修复该错误并重新生成正确的SQL语句。"
                result, response = llm_call(llmname, apikey, prompt, file_content)
                logger.info(f"step3 [repair sql {i+1}]: {response}")
                if not result:
                    return jsonify({'code':Error.LLM_ERROR, 'message':response})
                
                # 解析json数据
                result, json_data = parse_json(response)
                if not result:
                    return jsonify({'code':Error.SYS_ERROR, 'message':json_data})

                # SQL语句和标题
                sql_statement = json_data['sql_statement']
                
                # 生成SQL失败
                if (sql_statement == None or sql_statement == ''):
                    return jsonify({'code':Error.SQL_FAILED, 'message':Error.msg[Error.SQL_FAILED]})
            else:   # SQL正确时跳出循环
                break
        # 以上代码用于验证SQL语句的执行 End ###############################

        # 用户提问
        role = 'user'
        type = 'text'
        json_content = {
            'type': 'text',
            'value': message
        }
        content = json.dumps(json_content, ensure_ascii=False, indent=4)
        ChatMessage.insert(ds_id, role, type, content)

        # ai返回
        role = 'ai'
        type = 'sql'
        json_content = {
            'type': 'sql',
            'text': message,
            'value': sql_statement
        }
        content = json.dumps(json_content, ensure_ascii=False, indent=4)
        chat_id = ChatMessage.insert(ds_id, role, type, content)

        #chat_id = 1
        #sql_statement = "SELECT employee.no AS 工号, employee.name AS 姓名, CASE employee.gender WHEN 1 THEN '男性' WHEN 2 THEN '女性' ELSE '未知' END AS 性别, CASE employee.married WHEN 0 THEN '未婚' WHEN 1 THEN '已婚' ELSE '未知' END AS 婚姻状况, CASE employee.state WHEN 0 THEN '离职' WHEN 1 THEN '在职' ELSE '未知' END AS 在职状态, DATE_FORMAT(employee.hiredate, '%Y-%m-%d') AS 入职日期, DATE_FORMAT(employee.firedate, '%Y-%m-%d') AS 离职日期 FROM employee WHERE 1=1 LIMIT 100"
        
        data = {'id': chat_id, 'sql': sql_statement}
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'data':data})
    except SQLAlchemyError as e:
        #print(f"chat_sendmessage error: {e}")
        logger.error(f"chat_sendmessage error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 执行SQL语句生成表格数据
@chatRoute.route('/chat/executesql', methods=['POST'])
def chat_executesql():
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    ds_id = data['ds_id']
    sql_id = data['sql_id']

    # 取datasource
    datasource = DataSource.get(ds_id)
    db_port = datasource.db_port
    db_type = datasource.db_type
    db_host = datasource.db_host
    db_name = datasource.db_name
    db_user = datasource.db_user
    db_password = datasource.db_password

    # 加密数据库用户密码
    secret_key = os.getenv('SECRET_KEY')
    salt_key = os.getenv('SALT_KEY')
    crypto = StringCrypto(secret_key, salt_key)
    success, msg = crypto.decrypt(db_password)
    if not success:
        return jsonify({'code':Error.SYS_ERROR, 'message':msg})
    dbpassword_decrypt = msg

    # 取SQL语句
    chatmessage = ChatMessage.get(sql_id)
    content = chatmessage.content
    json_content = json.loads(content)
    sql_statement = json_content['value']
    
    # 检查SQL安全性
    checker = SQLSecurityChecker()
    success, msg = checker.check_sql_security(sql_statement)
    if not success:
        return jsonify({'code':Error.UNSAFE_SQL, 'message':msg})

    try:
        # 执行SQL
        success, results = sql_exec(db_type, db_host, db_port, db_name, db_user, dbpassword_decrypt, sql_statement)
        if not success:
            return jsonify({'code':Error.DB_ERROR, 'message':results})
        
        # 没有符合条件的记录
        if results['row_count'] == 0:
            return jsonify({'code':Error.NO_MATCH_ROWS, 'message':Error.msg[Error.NO_MATCH_ROWS]})
        
        # 超过记录数限制
        if results['row_count'] > int(os.getenv('MAX_ROWS')):
            return jsonify({'code':Error.OVER_MAX_ROWS, 'message':Error.msg[Error.OVER_MAX_ROWS]})
        
        # 执行成功
        role = 'ai'
        type = 'table'
        json_content = {
            'type': 'table',
            'columns': results['columns'],
            'records': results['records'],
            'row_count': results['row_count'],
            'sql_id': sql_id
        }

        content = json.dumps(json_content, ensure_ascii=False, indent=4)
        chat_id = ChatMessage.insert(ds_id, role, type, content)

        data = {'id': chat_id, 'content': json_content}
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'data':data})
    except SQLAlchemyError as e:
        #print(f"chat_executesql error: {e}")
        logger.error(f"chat_executesql error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})
