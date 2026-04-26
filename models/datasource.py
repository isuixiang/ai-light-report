# model datasource 数据源配置
from sqlalchemy_serializer import SerializerMixin
from models.db import db
from datetime import datetime

class DataSource(db.Model, SerializerMixin):
    __tablename__ = 'datasource'
    id = db.Column(db.Integer, primary_key=True)        # ID,主键
    name = db.Column(db.String(20))                     # 数据源名称
    db_type = db.Column(db.String(20))                  # 数据库类型
    db_host = db.Column(db.String(50))                  # 数据库主机
    db_port = db.Column(db.Integer)                     # 数据库端口
    db_name = db.Column(db.String(50))                  # 数据库名称
    db_user = db.Column(db.String(20))                  # 数据库用户
    db_password = db.Column(db.String(256))             # 数据库密码
    create_time = db.Column(db.DateTime, index=True)    # 创建时间

    # 添加记录
    def insert(name, db_type, db_host, db_port, db_name, db_user, db_password):
        data = DataSource(
            name = name,
            db_type = db_type,
            db_host = db_host,
            db_port = db_port,
            db_name = db_name,
            db_user = db_user,
            db_password = db_password,
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(data)
        db.session.flush()
        return data.id
    
    # 更新名称
    def updateName(id, name):
        data = DataSource.query.get(id)
        data.name = name
    
    # 删除记录
    def delete(id):
        data = DataSource.query.get(id)
        db.session.delete(data)
    
    # 取全部记录
    def getList():
        return DataSource.query.order_by(DataSource.create_time.asc()).all()

    # 根据id查询
    def get(id):
        return DataSource.query.get(id)
