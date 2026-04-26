# model llm 大模型接口配置
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import update
from models.db import db
from datetime import datetime

class Llm(db.Model, SerializerMixin):
    __tablename__ = 'llm'
    id = db.Column(db.Integer, primary_key=True)        # ID,主键
    name = db.Column(db.String(20), unique=True)        # 大模型名称
    url = db.Column(db.String(200))                     # 接口调用URL
    apikey = db.Column(db.String(64))                   # PDF报告文件
    used = db.Column(db.Integer)                        # 是否默认(0-否,1-是)
    create_time = db.Column(db.DateTime, index=True)    # 创建时间

    # 添加记录
    def insert(name, apikey):
        data = Llm(
            name = name,
            apikey = apikey,
            used = 0,
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(data)
        db.session.flush()
        return data.id
    
    # 更新为默认使用
    def update(id):
        db.session.query(Llm).update({"used": 0})
        data = Llm.query.get(id)
        data.used = 1
    
    # 删除记录
    def delete(id):
        data = Llm.query.get(id)
        db.session.delete(data)
    
    # 取全部记录
    def getList():
        return Llm.query.order_by(Llm.create_time.asc()).all()
    
    # 根据名称取记录
    def getByName(name):
        return Llm.query.filter(Llm.name==name).first()

    # 根据id查询
    def get(id):
        return Llm.query.get(id)
