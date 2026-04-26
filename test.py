import sys
import os, base64
from utils.crypt import StringCrypto
from config import Config

# 设置解释器编码以正确输出汉字和特殊字符
sys.stdout.reconfigure(encoding='utf-8')

# 读取配置参数
config = Config.from_env()

# 生成随机SECRET_KEY
def generate_secret_key(len):
    str = os.urandom(len)
    return base64.b64encode(str)

# 字符串加密
def string_encrypt(str):
    secret_key = config.app_config.secret_key
    salt_key = config.app_config.salt_key
    crypto = StringCrypto(secret_key, salt_key)
    encrypt_str = crypto.encrypt(str)
    print(encrypt_str)

# 字符串解密
def string_decrypt(str):
    secret_key = config.app_config.secret_key
    salt_key = config.app_config.salt_key
    crypto = StringCrypto(secret_key, salt_key)
    decrypt_str = crypto.decrypt(str)
    print(decrypt_str)

# 生成SECRET_KEY
#print(generate_secret_key(32))

# 字符串加密
string_encrypt("123456")

# 字符串解密
#string_decrypt("xxx")
