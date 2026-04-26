# 加解密模块
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class StringCrypto:
    def __init__(self, key: str, salt: str):
        """
        初始化加密器
        
        Args:
            key: 自定义密钥
            salt: 自定义盐值
        """
        self.key = key.encode('utf-8')
        self.salt = salt.encode('utf-8')
        
        # 使用PBKDF2从密码派生密钥
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.key))
        self.fernet = Fernet(key)
    
    def encrypt(self, text: str):
        """
        加密字符串
        
        Args:
            text: 要加密的明文
            
        Returns:
            base64编码的加密字符串
        """
        try:
            text_bytes = text.encode('utf-8')
            encrypted_bytes = self.fernet.encrypt(text_bytes)
            return True, base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
        except Exception as e:
            print(f"加密失败: {e}")
            return False, f"加密失败: {e}"
    
    def decrypt(self, encrypted_text: str):
        """
        解密字符串
        
        Args:
            encrypted_text: base64编码的加密字符串
            
        Returns:
            解密后的明文
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_text.encode('utf-8'))
            decrypted_bytes = self.fernet.decrypt(encrypted_bytes)
            return True, decrypted_bytes.decode('utf-8')
        except Exception as e:
            print(f"解密失败: {e}")
            return False, f"解密失败: {e}"
