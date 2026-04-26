# model chatmessage AI聊天消息
from sqlalchemy_serializer import SerializerMixin
from models.db import db
from datetime import datetime

class ChatMessage(db.Model, SerializerMixin):
    __tablename__ = 'chatmessage'
    id = db.Column(db.Integer, primary_key=True)        # ID,主键
    ds_id = db.Column(db.Integer, index=True)           # 数据源ID
    role = db.Column(db.String(10))                     # 角色名称(user-用户，ai-大模型)
    type = db.Column(db.String(10))                     # 数据类型(text/sql/table)
    content = db.Column(db.Text)                        # 对话内容（JSON格式，包括type和content两个键，type区分text/sql/table，content存储对话内容）
    create_time = db.Column(db.DateTime, index=True)    # 创建时间

    # 添加记录
    def insert(ds_id, role, type, content):
        data = ChatMessage(
            ds_id = ds_id,
            role = role,
            type = type,
            content = content,
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(data)
        db.session.flush()
        return data.id
    
    # 更新SQL语句
    def updateSQL(id, content):
        data = ChatMessage.query.get(id)
        data.content = content
    
    # 删除一条记录
    def delete(id):
        data = ChatMessage.query.get(id)
        db.session.delete(data)

    # 删除一组记录
    def deleteByDsID(ds_id):
        db.session.query(ChatMessage).filter(ChatMessage.ds_id==ds_id).delete()

    # 取SQL记录
    def getSQLs(ds_id):
        return ChatMessage.query.filter(ChatMessage.ds_id==ds_id, ChatMessage.type=='sql') \
            .order_by(ChatMessage.create_time.asc()).all()
    
    # 取最新一条SQL记录
    def getLastestSQL(ds_id):
        return ChatMessage.query.filter(ChatMessage.ds_id==ds_id, ChatMessage.type=='sql') \
            .order_by(ChatMessage.create_time.desc()).first()
    
    # 取全部记录
    def getList():
        return ChatMessage.query.order_by(ChatMessage.create_time.asc()).all()
    
    # 取一组记录
    def getListByDsID(ds_id):
        return ChatMessage.query.filter(ChatMessage.ds_id==ds_id).order_by(ChatMessage.create_time.asc()).all()

    # 根据id查询
    def get(id):
        return ChatMessage.query.get(id)
