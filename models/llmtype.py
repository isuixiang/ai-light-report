# model llmtype 支持的大模型类型
from sqlalchemy_serializer import SerializerMixin
from models.db import db

class LlmType(db.Model, SerializerMixin):
    __tablename__ = 'llmtype'
    id = db.Column(db.Integer, primary_key=True)        # ID,主键
    name = db.Column(db.String(20))                     # 大模型名称
    remark = db.Column(db.String(200))                  # 备注
  
    # 取全部记录
    def getList():
        return LlmType.query.all()

    # 根据id查询
    def get(id):
        return LlmType.query.get(id)
