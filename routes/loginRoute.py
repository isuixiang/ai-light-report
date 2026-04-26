# route login
from flask import Blueprint, session, request, json, jsonify, redirect, make_response, render_template
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from models.user import User
from utils.jwttoken import verify_token
from utils.captcha import generate_image
from utils.error import Error
from utils.crypt import StringCrypto
from io import BytesIO
from dotenv import load_dotenv
import os, base64

loginRoute = Blueprint('login', __name__)

# 读取配置参数
load_dotenv(override=True)

# 获取验证码
@loginRoute.route('/get_captcha', methods=['GET'])
def get_captcha():
    # 创建验证码对象
    im, code = generate_image(4)
    # 把验证码放入session
    session['code'] = code
    # 把验证码转换为二进制
    buffer = BytesIO()
    # 把验证码保存在创建的二进制容器里面
    im.save(buffer, "JPEG")
    # 获取图片
    buf_bytes = buffer.getvalue()
    # 转base64编码
    buf_bytes64 = base64.b64encode(buf_bytes)
    response = make_response(buf_bytes64)
    # 读取图片需要指定Content-Type
    response.headers['Content-Type'] = 'image/jpeg'
    return response

# 登录页
@loginRoute.route('/', methods=['GET', 'POST'])
@loginRoute.route('/login', methods=['GET', 'POST'])
def index():
    # 已登录重定向到首页
    if session.get('userid') != None:
        return redirect('/index')
    
    # GET请求
    if request.method == 'GET':
        return render_template('login.html')

    # 验证token
    token = request.headers['Authorization']
    if verify_token(token, os.getenv('SECRET_KEY')) == None:
        return jsonify({'code':Error.INVALID_TOKEN, 'message':Error.msg[Error.INVALID_TOKEN]})

    # 参数
    data = json.loads(request.data)
    no = data['no']
    password = data['password']
    verificationCode = data['verificationCode']

    # 校验验证码(首次登录不校验)
    if len(verificationCode) > 0:
        code = session.get('code')
        if code == None or verificationCode.lower() != code.lower():
            return jsonify({'code':Error.INVALID_CAPTCHA, 'message':Error.msg[Error.INVALID_CAPTCHA]})
    
    # 验证手机和密码
    user = User.getByNo(no)
    if (not user or user == None):
        return jsonify({'code':Error.INVALID_ACCOUNT_PWD, 'message':Error.msg[Error.INVALID_ACCOUNT_PWD]})

    # 解密登录密码
    secret_key = os.getenv('SECRET_KEY')
    salt_key = os.getenv('SALT_KEY')
    crypto = StringCrypto(secret_key, salt_key)
    success, msg = crypto.decrypt(user.pwd)
    if not success:
        return jsonify({'code':Error.SYS_ERROR, 'message':msg})
    pwd_decrypt = msg
    
    if (pwd_decrypt != password):
        return jsonify({'code':Error.INVALID_ACCOUNT_PWD, 'message':Error.msg[Error.INVALID_ACCOUNT_PWD]})
    
    # 验证账号状态
    if (user.state == 0):
        return jsonify({'code':Error.ACCOUNT_DISABLED, 'message':Error.msg[Error.ACCOUNT_DISABLED]})
    
    # 验证成功
    session['userid'] = user.id
    return jsonify({'code':Error.SUCCESS, 'message':Error.msg[Error.SUCCESS]})

# 退出登录
@loginRoute.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/login')