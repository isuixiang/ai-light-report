# model user 用户表
from sqlalchemy_serializer import SerializerMixin
from models.db import db
from datetime import datetime

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)        # ID,主键
    no = db.Column(db.String(20), unique=True)     		# 账号
    pwd = db.Column(db.String(256))                     # 密码
    name = db.Column(db.String(20))                     # 姓名
    create_time = db.Column(db.DateTime, index=True)    # 创建时间
    state = db.Column(db.Integer)                       # 状态(0-禁用,1-正常)

    # 创建用户
    def insert(no, pwd, name):
        data = User(
            no = no,
            pwd = pwd,
            name = name,
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            state = 1
        )
        db.session.add(data)
        db.session.flush()
        return data.id

    # 用户登录
    def login(no, pwd):
        return User.query.filter(User.no==no, User.pwd==pwd).first()
    
    # 修改用户
    def update(id, name, state):
        data = User.query.get(id)
        data.name = name
        data.state = state

    # 修改密码
    def updatePwd(id, newpwd):
        data = User.query.get(id)
        data.pwd = newpwd
    
    # 删除用户
    def delete(id):
        data = User.query.get(id)
        db.session.delete(data)

    # 根据no取用户
    def getByNo(no):
        return User.query.filter(User.no==no).first()

    # 根据ID取用户
    def get(id):
        return User.query.get(id)
