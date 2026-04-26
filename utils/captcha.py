# 生成验证码
import random
from PIL import Image, ImageFont, ImageDraw

def get_random_color():
    return (random.randint(120, 200), random.randint(120, 200), random.randint(120, 200))

def generate_image(length):
    s = 'qwerQWERTYUIOtyuiopas123456dfghjklPASDFGHJKLZXCVBNMxcvbnm7890'
    # 指定图片的大小
    size = (130, 50)
    # 创建一个画布 , 需要三个参数, def new(mode, size, color=0):
    # model:使用的模式, size:图片大小, color:图片颜色
    #im = Image.new('RGB', size, color=get_random_color())
    im = Image.new('RGB', size, (210, 210, 210))
    # 创建字体
    font = ImageFont.truetype('simkai.ttf', size=35)
    # 服务器字体
    #font = ImageFont.truetype('DejaVuSans.ttf', size=35)
    # 创建ImageDraw对象
    draw = ImageDraw.Draw(im)
    # 绘制验证码
    # 接收验证码
    code = ''
    for i in range(length):
        # 从字符串s中随机取出一个字符
        c = random.choice(s)
        code += c
        # 绘制
        # draw.text((x坐标,y坐标), text=绘制什么, file=字体颜色, font=字体)
        draw.text((5 + random.randint(4, 7) + 25 * i, 1),
            text=c,
            fill=get_random_color(),
            font=font)

    # 绘制干扰线
    for i in range(6):
        x1 = random.randint(0, 130)
        y1 = random.randint(0, 50/2)

        x2 = random.randint(0, 130)
        y2 = random.randint(0, 50 / 2)
        draw.line(((x1, y1), (x2, y2)))

    # 加入干扰点
    for i in range(16):
        draw.point((random.randint(0, 130), random.randint(0, 50)), fill=get_random_color())
    
    return im, code

    #im.show()
