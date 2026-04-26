# 生成与验证token
import jwt
import time
import string
import random

# 生成随机密钥（大小写字母+数字）
def generate_secret_key(len):
    # string.ascii_letters 大小写字母， string.digits 为数字
    characters_long = list(string.ascii_letters + string.digits)

    # 打乱字符串序列
    random.shuffle(characters_long)

    str = []

    for i in range(len):
        str.append(random.choice(characters_long))

	# 打乱字符串顺序
    random.shuffle(str)

	# 将列表转换为字符串
    return "".join(str)

# 生成token
def generate_token(payload, secret):
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token

# 验证token
def verify_token(token, secret):
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.PyJWTError:
        return None

if __name__ == '__main__':
    secret = '9xaCtVYyau/rCwMEFX3GoQjCKwUD5UXwwHdjRHxkdLM='
    payload = {
        'id': 'AILightReport',
        #'exp': int(time.time()) + 3600 * 12,    # 12小时
    }
    token = generate_token(payload, secret)
    print(token)
    '''
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IkFJTGlnaHRSZXBvcnQifQ.LPE90pfKWTKjn-0Viid6WIeuuFwqI3O18wXQ9qEQ6RQ"
    payload = verify_token(token, secret)
    print(payload)
    exp = payload['exp']
    print(exp)
    d = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(exp))
    print(d)
    '''
