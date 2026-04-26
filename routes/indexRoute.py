# route index
from flask import Blueprint, request, session, json, jsonify, redirect, render_template
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from models.dbtype import DbType
from models.llmtype import LlmType
from models.datasource import DataSource
from models.llm import Llm
from models.exceltemplate import ExcelTemplate
from models.exceloutput import ExcelOutput
from models.skills import Skills
from models.user import User
from utils.jwttoken import verify_token
from utils.dbtest import db_test
from utils.error import Error
from utils.sqlcheck import SQLSecurityChecker
from utils.logger import setup_logger
from utils.crypt import StringCrypto
from utils.dbexec import sql_exec
from utils.mdread import read_md_content
from openpyxl import load_workbook
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import re, os, shutil, random

indexRoute = Blueprint('index', __name__)

# 读取配置参数
load_dotenv(override=True)

# 启动日志信息
logger = setup_logger()

# 移动文件目录
def move_file(source ,destination):
    try:
        # 确保目标目录存在
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        # 移动文件
        shutil.move(source, destination)
        print(f"文件已成功从 {source} 移动到 {destination}")
        return True
    except FileNotFoundError:
        print("源文件不存在")
        return False
    except PermissionError:
        print("没有足够的权限执行此操作")
        return False
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False

# 字符串脱敏函数
def mask_apikey(s: str, start: int = 5, end: int = 5, mask_char: str = '*'):
        if not s or not isinstance(s, str):
            return s
            
        s = s.strip()
        total_length = len(s)
        
        # 如果字符串长度不足以脱敏，直接返回
        if total_length <= start + end:
            return s
            
        # 计算需要脱敏的中间部分长度
        mask_length = total_length - start - end
        
        start_part = s[:start]
        end_part = s[-end:] if end > 0 else ''
        
        return f"{start_part}{mask_char * mask_length}{end_part}"

# 生成单行的SQL语句
def one_line_sql(sql):
    # 去除两端空格
    new_sql = sql.strip()
    # 合并多行为空格（保留必要空格）
    sql_oneline = re.sub(r'\s+', ' ', new_sql)
    # 或仅移除 \n 但保留空格
    sql_oneline = new_sql.replace('\n', ' ').replace('\r', ' ')
    return sql_oneline

# 读取excel文件内容
def read_excel_content(file_path):
    # 加载工作簿，data_only=False → 保留公式
    wb = load_workbook(filename=file_path, data_only=False)
    ws = wb.active  # 默认读取第一个工作表

    # 获取最大行列范围（避免全表扫描性能问题）
    max_row = ws.max_row
    max_col = ws.max_column

    # 构建二维数据表
    data = []
    for row in range(1, max_row + 1):
        row_data = []
        for col in range(1, max_col + 1):
            cell = ws.cell(row=row, column=col)
            value = cell.value

            # 处理 None（空单元格）
            if value is None:
                row_data.append('')
            else:
                # 公式在 openpyxl 中就是字符串，以 '=' 开头
                # 直接转为字符串确保前端安全显示
                row_data.append(str(value))
        data.append(row_data)
    
    return data

# 生成输出文件名
def generate_outputfile(title):
    # 生成14位日期时间 + 4位随机数
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(1000, 9999)
    return f"{title}_{timestamp}_{random_num}.xlsx"

# 预处理，未登录重定向到login
@indexRoute.before_request
def pre_redirect():
    if session.get('userid') == None:
        return redirect('/')

# 首页
@indexRoute.route('/index')
def index():
    # 登录用户id
    userid = session.get('userid')

    # 取登录用户
    user = User.get(userid)

    # 取数据库类型
    dbtype = DbType.getList()
    # 取大模型类型
    llmtype = LlmType.getList()

    # 取已配置数据源
    datasource = DataSource.getList()
    # 取已配置大模型
    llm = Llm.getList()

    llm_dict = []
    for item in llm:
        item_dict = item.to_dict()
        item_dict['mask_apikey'] = mask_apikey(item_dict['apikey'])
        llm_dict.append(item_dict)

    data = {
        'dbtype': dbtype,
        'llmtype': llmtype,
        'datasource': datasource,
        'llm': llm_dict
    }

    return render_template('index.html', data=data, user=user)

# 取全部模板记录
@indexRoute.route('/exceltemplate/list', methods=['POST'])
def exceltemplate_list():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})

    # 参数
    data = json.loads(request.data)
    ds_id = data['ds_id']
    page = data['page']
    
    # 分页查询
    pagination = ExcelTemplate.getPage(page, ds_id)
    results = [item.to_dict() for item in pagination.items]

    data = {
        'results': results,
        'current_page': pagination.page,
        'total_pages': pagination.pages,
        'total_items': pagination.total,
        'has_prev': pagination.has_prev,
        'has_next': pagination.has_next
    }

    return jsonify({'code':Error.SUCCESS, 'data':data})

# 取单条模板记录
@indexRoute.route('/exceltemplate/detail', methods=['POST'])
def exceltemplate_detail():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})

    # 参数
    data = json.loads(request.data)
    template_id = data['id']

    # 取模板记录
    exceltemplate = ExcelTemplate.get(template_id)

    # 读取模板内容
    #fname = exceltemplate.filename[1:]     # 去掉文件名中第一个斜杠符号
    #excel_data = read_excel_content(fname)
    '''
    data = {
        'id': template_id,
        'rows': len(excel_data),
        'cols': len(excel_data[0]) if data else 0,
        'excel_data': excel_data,
        'pattern': exceltemplate.pattern,
        'content': exceltemplate.content
    }
    '''
    # JSON序列化
    data_dict = exceltemplate.to_dict()

    return jsonify({'code':Error.SUCCESS, 'data':data_dict})

# 数据源链接测试
@indexRoute.route('/datasource/test', methods=['POST'])
def datasource_test():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    #name = data['name']
    dbtype = data['dbtype']
    dbport = data['dbport']
    dbhost = data['dbhost']
    dbname = data['dbname']
    dbuser = data['dbuser']
    dbpassword = data['dbpassword']

    # 数据库连接测试
    success, message = db_test(dbtype, dbhost, dbport, dbname, dbuser, dbpassword)
    if success:
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    else:
        return jsonify({'code':Error.DB_ERROR, 'message':message})

# 数据源参数保存
@indexRoute.route('/datasource/save', methods=['POST'])
def datasource_save():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    name = data['name']
    dbtype = data['dbtype']
    dbport = data['dbport']
    dbhost = data['dbhost']
    dbname = data['dbname']
    dbuser = data['dbuser']
    dbpassword = data['dbpassword']

    # 加密数据库用户密码
    secret_key = os.getenv('SECRET_KEY')
    salt_key = os.getenv('SALT_KEY')
    crypto = StringCrypto(secret_key, salt_key)
    success, msg = crypto.encrypt(dbpassword)
    if not success:
        return jsonify({'code':Error.SYS_ERROR, 'message':msg})
    dbpassword_encrypt = msg

    try:
        # 添加数据源
        DataSource.insert(name, dbtype, dbhost, dbport, dbname, dbuser, dbpassword_encrypt)
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"datasource_save error: {e}")
        logger.error(f"datasource_save error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 数据源更新名称
@indexRoute.route('/datasource/edit', methods=['POST'])
def datasource_edit():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
	# 参数
    data = json.loads(request.data)
    ds_id = data['ds_id']
    name = data['name']

    try:
        # 取数据源记录
        datasource = DataSource.get(ds_id)

        # 更新数据源名称
        if datasource.name != name:
            DataSource.updateName(ds_id, name)

        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"datasource_edit error: {e}")
        logger.error(f"datasource_edit error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 删除数据源
@indexRoute.route('/datasource/delete', methods=['POST'])
def datasource_delete():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    id = data['id']
   
    try:
        # 删除关联数据
        ExcelTemplate.deleteByDsId(id)
        DataSource.delete(id)

        # 删除数据源关联的Skills文档
        Skills.deleteByDsID(id)
        
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"datasource_delete error: {e}")
        logger.error(f"datasource_delete error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 添加大模型配置
@indexRoute.route('/llm/save', methods=['POST'])
def llm_save():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    name = data['name']
    apikey = data['apikey']
   
    try:
        # 判断是否重复添加
        llm = Llm.getByName(name)
        if llm:
            return jsonify({'code':Error.HAS_EXISTED, 'message':Error.msg[Error.HAS_EXISTED]})
        
        Llm.insert(name, apikey)
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"llm_save error: {e}")
        logger.error(f"llm_save error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 删除大模型配置
@indexRoute.route('/llm/delete', methods=['POST'])
def llm_delete():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    id = data['id']
   
    try:
        Llm.delete(id)
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"llm_delete error: {e}")
        logger.error(f"llm_delete error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 设置默认模型
@indexRoute.route('/llm/setting', methods=['POST'])
def llm_setting():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    id = data['id']
   
    try:
        Llm.update(id)
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"llm_setting error: {e}")
        logger.error(f"llm_setting error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 保存模板信息
@indexRoute.route('/exceltemplate/save', methods=['POST'])
def exceltemplate_save():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    ds_id = data['ds_id']
    title = data['title']
    desc = data['desc']
    excelfile = data['filename']

    # 将文件从临时目录移动到正式目录
    file_src = os.path.join(os.getenv('TEMP_PATH'), excelfile)
    file_dst = os.path.join(os.getenv('EXCELS_PATH'), excelfile)
    full_file_src = os.getcwd() + file_src
    full_file_dst = os.getcwd() + file_dst
    if not move_file(full_file_src, full_file_dst):
        return jsonify({'code':Error.SYS_ERROR, 'message':Error.msg[Error.SYS_ERROR]})
    
    try:
        # 读取模板内容
        fname = file_dst[1:]     # 去掉文件名中第一个斜杠符号
        excel_data = read_excel_content(fname)

        # JSON转字符串
        pattern = json.dumps(excel_data, ensure_ascii=False)
        ExcelTemplate.insert(ds_id, title, desc, file_dst, pattern)
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"exceltemplate_save error: {e}")
        logger.error(f"exceltemplate_save error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 更新模板信息与文件
@indexRoute.route('/exceltemplate/edit', methods=['POST'])
def exceltemplate_edit():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
	# 参数
    data = json.loads(request.data)
    template_id = data['id']
    title = data['title']
    desc = data['desc']
    excelfile = data['filename']

    # 将文件从临时目录移动到正式目录
    if excelfile:
        file_src = os.path.join(os.getenv('TEMP_PATH'), excelfile)
        file_dst = os.path.join(os.getenv('EXCELS_PATH'), excelfile)
        full_file_src = os.getcwd() + file_src
        full_file_dst = os.getcwd() + file_dst
        if not move_file(full_file_src, full_file_dst):
            return jsonify({'code':Error.SYS_ERROR, 'message':Error.msg[Error.SYS_ERROR]})
    
    try:
        # 取模板记录
        exceltemplate = ExcelTemplate.get(template_id)

        # 更新模板标题和描述
        if (exceltemplate.title != title or exceltemplate.desc != desc):
            ExcelTemplate.updateInfo(template_id, title, desc)

        # 更新模板文件
        if excelfile:
            fname = file_dst[1:]     # 去掉文件名中第一个斜杠符号
            excel_data = read_excel_content(fname)

            # JSON转字符串
            pattern = json.dumps(excel_data, ensure_ascii=False)
            ExcelTemplate.updateFile(template_id, file_dst, pattern)
        
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"exceltemplate_edit error: {e}")
        logger.error(f"exceltemplate_edit error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 删除模板记录
@indexRoute.route('/exceltemplate/delete', methods=['POST'])
def exceltemplate_delete():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    id = data['template_id']
   
    try:
        # 删除模板和关联数据
        ExcelTemplate.delete(id)
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"exceltemplate_delete error: {e}")
        logger.error(f"exceltemplate_delete error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 更新报表定义
@indexRoute.route('/exceltemplate/setting', methods=['POST'])
def exceltemplate_setting():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    template_id = data['id']
    content = data['content']   # 模板定义（数组）

    try:
        # JSON转字符串
        content_string = json.dumps(content, ensure_ascii=False, indent=4)

        # 取原报表定义
        exceltemplate = ExcelTemplate.get(template_id)

        # 有变更时更新报表定义
        #if content_string != exceltemplate.content:
        # 更新模板定义
        ExcelTemplate.updateContent(template_id, content_string)

        # 取报表定义
        exceltemplate = ExcelTemplate.get(template_id)
        
        # JSON序列化
        data_dict = exceltemplate.to_dict()
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'data':data_dict})
    except SQLAlchemyError as e:
        #print(f"exceltemplate_setting error: {e}")
        logger.error(f"exceltemplate_setting error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 执行报表定义
@indexRoute.route('/exceltemplate/execute', methods=['POST'])
def exceltemplate_execute():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    template_id = data['id']

    # 取报表定义
    exceltemplate = ExcelTemplate.get(template_id)

    # 取datasource
    datasource = DataSource.get(exceltemplate.ds_id)
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

    try:
        # 字符串转JSON
        json_content = json.loads(exceltemplate.content)

        # 生成报表数据
        report_data = []
        for item in json_content:
            row = item['row']
            col = item['col']
            type = item['type']
            value = item['value']

            if type == "text":  # 文本
                item_data = {"row": row, "col": col, "value": value}
                report_data.append(item_data)
            else:       # SQL语句
                # 检查SQL安全性
                checker = SQLSecurityChecker()
                success, msg = checker.check_sql_security(value)
                if not success:
                    return jsonify({'code':Error.UNSAFE_SQL, 'message':msg})
                
                # 执行SQL
                success, results = sql_exec(db_type, db_host, db_port, db_name, db_user, dbpassword_decrypt, value)
                if not success:
                    return jsonify({'code':Error.DB_ERROR, 'message':results})
                
                # 没有符合条件的记录
                if results["row_count"] <= 0:
                    continue

                # 循环生成报表数据
                rowIndex = row
                for record in results["records"]:
                    colIndex = col
                    for element in record:
                        #element_value = str(element) if element else ""
                        element_value = element if element else ""
                        item_data = {"row": rowIndex, "col": colIndex, "value": element_value}
                        report_data.append(item_data)
                        colIndex += 1       # 列递增
                    rowIndex += 1   # 行递增
        
        #print(report_data)
        # 获取源模板文件
        file_src = exceltemplate.filename
        fname = file_src[1:]     # 去掉文件名中第一个斜杠符号

        # 加载工作簿，data_only=False → 保留公式
        wb = load_workbook(filename=fname, data_only=False)
        ws = wb.active  # 默认读取第一个工作表

        # 通过索引写入文件
        for item in report_data:
            ws.cell(row=int(item["row"]), column=int(item["col"]), value=item["value"])

        # 创建输出文件
        filename = generate_outputfile(exceltemplate.title)
        file_dst = os.path.join(os.getenv('FILES_PATH'), filename)
        full_file_dst = os.getcwd() + file_dst

        # 保存文件
        wb.save(full_file_dst)

        # 保存输出结果
        content_string = json.dumps(report_data, ensure_ascii=False, indent=4)
        ExcelOutput.insert(template_id, exceltemplate.title, content_string, file_dst)

        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"exceltemplate_execute error: {e}")
        logger.error(f"exceltemplate_execute error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 取输出报表列表
@indexRoute.route('/exceloutput/list', methods=['POST'])
def exceloutput_list():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})

    # 参数
    data = json.loads(request.data)
    template_id = data['template_id']

    # 取输出报表记录
    exceloutput = ExcelOutput.getListByTemplateId(template_id)

    # JSON序列化
    exceloutput_dict = []
    for item in exceloutput:
        item_dict = item.to_dict()
        exceloutput_dict.append(item_dict)

    return jsonify({'code':Error.SUCCESS, 'data':exceloutput_dict})

# 删除技能文档
@indexRoute.route('/exceloutput/delete', methods=['POST'])
def exceloutput_delete():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    id = data['id']
   
    try:
        # 删除报表输出文件
        ExcelOutput.delete(id)
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"exceloutput_delete error: {e}")
        logger.error(f"exceloutput_delete error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 修改密码
@indexRoute.route('/user/settingpassword', methods=['POST'])
def user_settingpassword():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    old_password = data['old_password']
    new_password = data['new_password']

    # 登录用户id
    userid = session.get('userid')
    user = User.get(userid)

    # 解密原密码
    secret_key = os.getenv('SECRET_KEY')
    salt_key = os.getenv('SALT_KEY')
    crypto = StringCrypto(secret_key, salt_key)
    success, msg = crypto.decrypt(user.pwd)
    if not success:
        return jsonify({'code':Error.SYS_ERROR, 'message':msg})
    pwd_decrypt = msg

    # 原密码不符
    if pwd_decrypt != old_password:
        return jsonify({'code':Error.INVALID_PASSWORD, 'message':Error.msg[Error.INVALID_PASSWORD]})
    
    try:
        # 加密新密码
        success, msg = crypto.encrypt(new_password)
        if not success:
            return jsonify({'code':Error.SYS_ERROR, 'message':msg})
        pwd_encrypt = msg

        # 修改密码
        User.updatePwd(userid, pwd_encrypt)
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"user_settingpassword error: {e}")
        logger.error(f"user_settingpassword error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 查询Skills文档
@indexRoute.route('/skills/list', methods=['POST'])
def skills_list():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    ds_id = data['ds_id']

    # 取数据源的Skills文档
    skills = Skills.getListByDsId(ds_id)

    # 序列化
    skills_dict = []
    for item in skills:
        item_dict = item.to_dict()
        skills_dict.append(item_dict)

    return jsonify({'code':Error.SUCCESS, 'data':skills_dict})

# Skill文档保存
@indexRoute.route('/skills/save', methods=['POST'])
def skills_save():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    ds_id = data['ds_id']
    type = data['type']
    name = data['name']
    desc = data['desc']
    filename = data['filename']

    # 避免重复添加主技能和通用技能
    skill1 = None
    if (int(type) == 1):
        skill1 = Skills.getSkillByDsIdType(ds_id, type)
    
    # 避免重复添加同一个技能名称
    skill2 = Skills.getSkillByDsIdName(ds_id, name)
    
    # 重复添加则直接返回提示
    if (skill1 or skill2):
        return jsonify({'code':Error.HAS_EXISTED, 'message':Error.msg[Error.HAS_EXISTED]})
    
    # 将文件从临时目录移动到正式目录
    file_src = os.path.join(os.getenv('TEMP_PATH'), filename)
    file_dst = os.path.join(os.getenv('SKILLS_PATH'), filename)
    full_file_src = os.getcwd() + file_src
    full_file_dst = os.getcwd() + file_dst
    if not move_file(full_file_src, full_file_dst):
        return jsonify({'code':Error.SYS_ERROR, 'message':Error.msg[Error.SYS_ERROR]})
    
    try:
        # 读文档内容
        fname = file_dst[1:]     # 去掉文件名中第一个斜杠符号
        file_content = read_md_content(Path(fname))
        if (file_content == None or file_content == ''):
            return jsonify({'code':Error.FILE_ERROR, 'message':Error.msg[Error.FILE_ERROR]})

        # 添加Skill文档
        Skills.insert(ds_id, type, name, desc, file_dst, file_content)
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"skills_save error: {e}")
        logger.error(f"skills_save error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})

# 删除技能文档
@indexRoute.route('/skills/delete', methods=['POST'])
def skills_delete():
    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})
    
    # 参数
    data = json.loads(request.data)
    id = data['id']
   
    try:
        # 删除技能文档
        Skills.delete(id)
        db.session.commit()
        return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})
    except SQLAlchemyError as e:
        #print(f"skills_delete error: {e}")
        logger.error(f"skills_delete error: {e}")
        db.session.rollback()
        return jsonify({'code':Error.DB_ERROR, 'message':e._message})
