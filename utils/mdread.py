# 读取Markdown文档内容
import re
from typing import Tuple
from pathlib import Path

# 读取文本
def read_md_content(file_path):
    try:
        full_text = ""
        
        with open(file_path, 'r', encoding='utf-8') as f:
            full_text = f.read()
        
        # 压缩
        compressed = ""
        if full_text:
            compressed = compress_markdown(full_text)
        
        return compressed
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

# 压缩文本
def compress_markdown(content: str, aggressive: bool = False):
    """
    压缩Markdown以减少tokens，保持语义
    
    Args:
        content: Markdown内容
        aggressive: 是否启用更激进的压缩
    
    Returns:
        (压缩后的内容, 压缩统计信息)
    """
    original_length = len(content)
    stats = {
        'original_tokens_estimate': estimate_tokens(content),
        'reductions': {}
    }
    
    # 复制内容开始处理
    compressed = content
    
    # 1. 移除行尾空白字符（完全安全）
    compressed = '\n'.join(line.rstrip() for line in compressed.split('\n'))
    stats['reductions']['trailing_spaces'] = original_length - len(compressed)
    
    # 2. 标准化换行符（完全安全）
    compressed = re.sub(r'\r\n', '\n', compressed)  # Windows换行转Unix
    
    # 3. 压缩连续空行（保持段落结构）
    compressed = re.sub(r'\n{3,}', '\n\n', compressed)  # 最多保留2个空行
    stats['reductions']['extra_newlines'] = original_length - len(compressed)
    
    # 4. 压缩列表项之间的多余空行（语义安全）
    '''
    # 列表项之间最多1个空行
    lines = compressed.split('\n')
    cleaned_lines = []
    in_list = False
    
    for i, line in enumerate(lines):
        is_list_item = line.strip().startswith(('-', '*', '+', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.'))
        
        if is_list_item:
            in_list = True
            cleaned_lines.append(line)
        elif line.strip() == '':
            # 如果是空行
            if in_list and i < len(lines)-1:
                next_is_list = lines[i+1].strip().startswith(('-', '*', '+', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.'))
                if not next_is_list:
                    cleaned_lines.append(line)  # 保留列表结束的空行
        else:
            in_list = False
            cleaned_lines.append(line)
    
    compressed = '\n'.join(cleaned_lines)
    '''
    
    # 5. 压缩代码块内的多余空行（可选，针对长代码块）
    if aggressive:
        compressed = compress_code_blocks(compressed)
    
    # 6. 移除HTML注释（完全安全）
    compressed = re.sub(r'<!--.*?-->', '', compressed, flags=re.DOTALL)
    
    # 7. 压缩表格内的多余空格（语义安全）
    compressed = compress_table_spacing(compressed)
    
    # 8. 智能合并短行（可选）
    if aggressive:
        compressed = merge_short_lines(compressed)
    
    '''
    stats['compressed_tokens_estimate'] = estimate_tokens(compressed)
    stats['reduction_percentage'] = (
        (stats['original_tokens_estimate'] - stats['compressed_tokens_estimate']) / 
        stats['original_tokens_estimate'] * 100
    )
    stats['compression_ratio'] = (
        stats['original_tokens_estimate'] / stats['compressed_tokens_estimate']
        if stats['compressed_tokens_estimate'] > 0 else 1
    )
    '''
    
    return compressed

def estimate_tokens(text: str):
    """粗略估计token数量"""
    # 更精确的估算：英文~4字符=1token，中文~1.5字符=1token
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    other_chars = len(text) - chinese_chars
    return int(chinese_chars / 1.3 + other_chars / 3.5)  # 更新后的估算

def compress_code_blocks(content: str) -> str:
    """压缩代码块内的多余空行"""
    lines = content.split('\n')
    result = []
    in_code_block = False
    code_block_lines = []
    
    for line in lines:
        if line.strip().startswith('```'):
            if in_code_block:
                # 结束代码块，处理内容
                compressed_code = compress_code_content('\n'.join(code_block_lines))
                result.append(compressed_code)
                result.append('```')
                code_block_lines = []
                in_code_block = False
            else:
                result.append('```')
                in_code_block = True
        elif in_code_block:
            code_block_lines.append(line)
        else:
            result.append(line)
    
    return '\n'.join(result)

def compress_code_content(code: str) -> str:
    """压缩代码内容（移除尾随空格，标准化空行）"""
    # 移除每行尾随空格
    lines = [line.rstrip() for line in code.split('\n')]
    
    # 移除开头的空行
    while lines and lines[0] == '':
        lines.pop(0)
    
    # 移除结尾的空行
    while lines and lines[-1] == '':
        lines.pop(-1)
    
    return '\n'.join(lines)

def compress_table_spacing(content: str) -> str:
    """压缩表格内的多余空格"""
    lines = content.split('\n')
    result = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检查是否是表格行
        if '|' in line and not line.strip().startswith('#'):
            # 压缩表格行
            cells = line.split('|')
            # 移除单元格内的首尾空格，但保留内部空格
            compressed_cells = [cell.strip() for cell in cells]
            compressed_line = '|'.join(compressed_cells)
            result.append(compressed_line)
        else:
            result.append(line)
        i += 1
    
    return '\n'.join(result)

def merge_short_lines(content: str, max_length: int = 80) -> str:
    """合并过短的连续行"""
    lines = content.split('\n')
    merged_lines = []
    buffer = []
    
    for line in lines:
        # 不要合并以下内容：
        # 1. 标题
        # 2. 代码块标记
        # 3. 列表项
        # 4. 表格行
        # 5. 块引用
        
        is_special_line = (
            line.strip().startswith('#') or  # 标题
            line.strip().startswith('```') or  # 代码块
            line.strip().startswith(('-', '*', '+', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or  # 列表
            '|' in line or  # 表格
            line.strip().startswith('>')  # 引用
        )
        
        if is_special_line or len(line) > max_length:
            # 处理缓冲区
            if buffer:
                merged_lines.append(' '.join(buffer))
                buffer = []
            merged_lines.append(line)
        elif line.strip() == '':
            # 空行：处理缓冲区并添加空行
            if buffer:
                merged_lines.append(' '.join(buffer))
                buffer = []
            merged_lines.append('')
        else:
            # 普通行，添加到缓冲区
            buffer.append(line.strip())
    
    # 处理最后的缓冲区
    if buffer:
        merged_lines.append(' '.join(buffer))
    
    return '\n'.join(merged_lines)

# 使用示例
'''
filename = Path('upload/files/skill_sql_generation.md')
content = read_md_content(filename)
print(len(content))
if content:
    print(content)
'''
