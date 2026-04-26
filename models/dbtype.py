# model dbtype 支持的数据库类型
from sqlalchemy_serializer import SerializerMixin
from models.db import db

class DbType(db.Model, SerializerMixin):
    __tablename__ = 'dbtype'
    id = db.Column(db.Integer, primary_key=True)        # ID,主键
    type = db.Column(db.String(20))                     # 数据库类型
    port = db.Column(db.Integer)                        # 数据库端口
  
    # 取全部记录
    def getList():
        return DbType.query.all()

    # 根据id查询
    def get(id):
        return DbType.query.get(id)
