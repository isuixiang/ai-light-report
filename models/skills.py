# model skills 数据源技能文档
from sqlalchemy_serializer import SerializerMixin
from models.db import db
from datetime import datetime

class Skills(db.Model, SerializerMixin):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)        # ID,主键
    ds_id = db.Column(db.Integer, index=True)           # 数据源ID
    type = db.Column(db.Integer)                        # 类型（1-主技能，2-子技能，3-通用技能）
    name = db.Column(db.String(50))                     # 名称
    desc = db.Column(db.String(50))                     # 描述
    filename = db.Column(db.String(100))                # 文件名URL
    content = db.Column(db.Text)                        # 文档内容
    create_time = db.Column(db.DateTime, index=True)    # 创建时间

    # 添加记录
    def insert(ds_id, type, name, desc, filename, content):
        data = Skills(
            ds_id = ds_id,
            type = type,
            name = name,
            desc = desc,
            filename = filename,
            content = content,
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(data)
        db.session.flush()
        return data.id
    
    # 删除一条记录
    def delete(id):
        data = Skills.query.get(id)
        db.session.delete(data)
    
    # 删除一组记录
    def deleteByDsID(ds_id):
        db.session.query(Skills).filter(Skills.ds_id==ds_id).delete()
    
    # 取数据源的全部技能
    def getListByDsId(ds_id):
        return Skills.query.filter(Skills.ds_id==ds_id).order_by(Skills.create_time.asc()).all()
    
    # 避免重复添加主技能和通用技能
    def getSkillByDsIdType(ds_id, type):
        return Skills.query.filter(Skills.ds_id==ds_id, Skills.type==type).first()
    
    # 避免重复添加同一技能名称
    def getSkillByDsIdName(ds_id, name):
        return Skills.query.filter(Skills.ds_id==ds_id, Skills.name==name).first()
    
    # 取主技能
    def getMainSkill(ds_id):
        return Skills.query.filter(Skills.ds_id==ds_id, Skills.type==1).first()
    
    # 取通用技能
    def getCommonSkills(ds_id):
        return Skills.query.filter(Skills.ds_id==ds_id, Skills.type==3).all()
    
    # 取单个子技能
    def getSubSkill(ds_id, type, name=None):
        return Skills.query.filter(Skills.ds_id==ds_id, Skills.type==type, Skills.name==name).first()

    # 根据id查询
    def get(id):
        return Skills.query.get(id)
