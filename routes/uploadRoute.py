# route uploads
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv
import os, random

uploadRoute = Blueprint('uploads', __name__)

# 读取配置参数
load_dotenv(override=True)

# 文件类型
#ALLOWED_FILE_EXTENSIONS = {'md', 'xlsx'}

# 判断文件类型
def allowed_file(filename, allowed_file_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_file_extensions

# 生成文件名
def generate_filename(original_filename, prefix):
    # 获取文件扩展名
    ext = original_filename.rsplit('.', 1)[1].lower()
    # 生成14位日期时间 + 4位随机数
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(1000, 9999)
    return f"{prefix}_{timestamp}_{random_num}.{ext}"

# Skill文件上传
@uploadRoute.route('/upload/skillfile', methods=['POST'])
def upload_skillfile():
    # 检查是否有文件被上传
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # 如果用户没有选择文件
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # 生成并保存文件
    if file and allowed_file(file.filename, {'md'}):
        # 生成唯一的文件名
        filename = generate_filename(file.filename, 'skill')
        # 确保文件名安全
        filename = secure_filename(filename)
        # 保存文件
        pathname = os.path.join(os.getenv('TEMP_PATH'), filename)
        fullname = os.getcwd() + pathname
        file.save(fullname)
        
        # 返回上传成功的响应，包含图片URL
        return jsonify({
            'success': True,
            'filename': filename,
            'url': pathname
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

# Excel文件上传
@uploadRoute.route('/upload/excelfile', methods=['POST'])
def upload_excelfile():
    # 检查是否有文件被上传
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # 如果用户没有选择文件
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # 生成并保存文件
    if file and allowed_file(file.filename, {'xlsx'}):
        # 生成唯一的文件名
        filename = generate_filename(file.filename, 'excel')
        # 确保文件名安全
        filename = secure_filename(filename)
        # 保存文件
        pathname = os.path.join(os.getenv('TEMP_PATH'), filename)
        fullname = os.getcwd() + pathname
        file.save(fullname)
        
        # 返回上传成功的响应，包含图片URL
        return jsonify({
            'success': True,
            'filename': filename,
            'url': pathname
        })
    
    return jsonify({'error': 'File type not allowed'}), 400
