# model exceloutput Excel报表输出
from sqlalchemy_serializer import SerializerMixin
from models.db import db
from datetime import datetime

class ExcelOutput(db.Model, SerializerMixin):
    __tablename__ = 'exceloutput'
    id = db.Column(db.Integer, primary_key=True)        # ID,主键
    template_id = db.Column(db.Integer)                 # 模板ID
    title = db.Column(db.String(50))                     # 标题
    content = db.Column(db.Text)                        # 报表数据(JSON格式，包括row,col,value三个键值)
    filename = db.Column(db.String(255))                # excel文件
    create_time = db.Column(db.DateTime, index=True)    # 创建时间

    # 添加记录
    def insert(template_id, title, content, filename):
        data = ExcelOutput(
            template_id = template_id,
            title = title,
            content = content,
            filename = filename,
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(data)
        db.session.flush()
        return data.id

    # 删除记录
    def delete(id):
        data = ExcelOutput.query.get(id)
        db.session.delete(data)
       
    # 根据模板ID查询
    def getListByTemplateId(template_id):
        return ExcelOutput.query.filter(ExcelOutput.template_id==template_id).order_by(ExcelOutput.create_time.desc()).all()
    
    # 根据id查询
    def get(id):
        return ExcelOutput.query.get(id)
    
        