# app.py
from datetime import timedelta
from urllib.parse import quote_plus
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, Blueprint, send_from_directory, redirect, render_template
from flask_cors import CORS
from models.db import db
from routes.loginRoute import loginRoute
from routes.indexRoute import indexRoute
from routes.uploadRoute import uploadRoute
from routes.chatRoute import chatRoute
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)       # 支持全局跨域

# 设置静态目录
static_bp = Blueprint('static', __name__)
upload_bp = Blueprint('upload', __name__)

# 静态目录路由
@static_bp.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@upload_bp.route('/<path:filename>')
def upload_files(filename):
    return send_from_directory('upload', filename)

# 注册静态目录
app.register_blueprint(static_bp, url_prefix='/static')
app.register_blueprint(upload_bp, url_prefix='/upload')

# 设置最大可上传文件
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 1MB

# 设置SESSION有效期为30天
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SESSION_COOKIE_SECURE'] = True

# 读取配置参数
load_dotenv(override=True)

# SECRET_KEY
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# 显式设置 session cookie 路径
app.config.update(
    SESSION_COOKIE_PATH='/',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # 如果用 HTTP；HTTPS 设为 True
)

# DB PARAMS
db_host = os.getenv('DB_HOST')          # 主机地址
db_port = os.getenv('DB_PORT')         # 主机端口
db_name = os.getenv('DB_NAME')      # 数据库名称
db_user = os.getenv('DB_USER')     # 用户名
db_password = os.getenv('DB_PASSWORD')  # 密码

# 对密码进行 URL 编码
encoded_password = quote_plus(db_password)

# 设置数据库连接地址
# mysql+pymysql://root:123456@localhost:3306/db?charset=utf8mb4
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4' %(db_user, encoded_password, db_host, db_port, db_name)
# 是否追踪数据库修改(开启后会触发一些钩子函数)  一般不开启, 会影响性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 是否打印底层执行的SQL语句
app.config['SQLALCHEMY_ECHO'] = False

# 数据库初始化，关联 Flask 应用
db.init_app(app)

# 配置信任真实的客户端IP，而非代理IP
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# 注册路由
app.register_blueprint(loginRoute)
app.register_blueprint(indexRoute)
app.register_blueprint(uploadRoute)
app.register_blueprint(chatRoute)

# 主路由
@app.route('/')
def home():
    return redirect('/login')

# 404
@app.errorhandler(404)
def page_not_found(error):
     return render_template('404.html'), 404

# 生产环境不需要 app.run()
if __name__ == '__main__':
    app.run(debug=True)
