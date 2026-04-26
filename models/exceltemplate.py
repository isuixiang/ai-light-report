# model exceltemplate Excel模板文件
from sqlalchemy_serializer import SerializerMixin
from models.db import db
from datetime import datetime

class ExcelTemplate(db.Model, SerializerMixin):
    __tablename__ = 'exceltemplate'
    id = db.Column(db.Integer, primary_key=True)        # ID,主键
    ds_id = db.Column(db.Integer)                       # 数据源ID
    title = db.Column(db.String(50))                    # 标题
    desc = db.Column(db.String(100))                    # 描述
    filename = db.Column(db.String(255))                # excel模板文件
    pattern = db.Column(db.Text)                        # 模板内容
    content = db.Column(db.Text)                        # 报表定义(JSON格式，包括row,col,type,value四个键值)
    create_time = db.Column(db.DateTime, index=True)    # 创建时间

    # 添加记录
    def insert(ds_id, title, desc, filename, pattern):
        data = ExcelTemplate(
            ds_id = ds_id,
            title = title,
            desc = desc,
            filename = filename,
            pattern = pattern,
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(data)
        db.session.flush()
        return data.id

    # 删除记录
    def delete(id):
        data = ExcelTemplate.query.get(id)
        db.session.delete(data)
    
    # 删除数据源关联的全部记录
    def deleteByDsId(ds_id):
        db.session.query(ExcelTemplate).filter(ExcelTemplate.ds_id==ds_id).delete()
    
    # 更新标题和描述
    def updateInfo(id, title, desc):
        data = ExcelTemplate.query.get(id)
        data.title = title
        data.desc = desc
    
    # 更新模板文件
    def updateFile(id, filename, pattern):
        data = ExcelTemplate.query.get(id)
        data.filename = filename
        data.pattern = pattern
    
    # 更新模板定义
    def updateContent(id, content):
        data = ExcelTemplate.query.get(id)
        data.content = content
    
    # 取全部记录
    def getList():
        return ExcelTemplate.query.order_by(ExcelTemplate.create_time.desc()).all()

    # 根据id查询
    def get(id):
        return ExcelTemplate.query.get(id)
    
    # 根据数据源ID查询
    def getListByDsId(ds_id):
        return ExcelTemplate.query.filter(ExcelTemplate.ds_id==ds_id).all()
        
    # 分页查询
    def getPage(page, ds_id):
        query = db.session.query(ExcelTemplate).filter(ExcelTemplate.ds_id==ds_id).order_by(ExcelTemplate.create_time.desc())
        pagination =  query.paginate(page=page, per_page=12, error_out=False)

        # 计算页码范围（最多显示5个页码）
        '''
        total_pages = pagination.pages
        current_page = pagination.page
        
        # 确定显示的页码范围
        if total_pages <= 5:
            start_page = 1
            end_page = total_pages
        else:
            if current_page <= 3:
                start_page = 1
                end_page = 5
            elif current_page >= total_pages - 2:
                start_page = total_pages - 4
                end_page = total_pages
            else:
                start_page = current_page - 2
                end_page = current_page + 2
        
        page_range = range(start_page, end_page + 1)
        '''
        return pagination
