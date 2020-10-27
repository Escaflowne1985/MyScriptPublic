#coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '图片进行裁剪的方法，标准尺寸1280 X 720' \
              '未来添加其他尺寸'
import os
import cv2
import numpy as np
from PIL import Image


# 去水印，不太好使
def CleanLogo(i,title,num):
    # 判断如果没有该数据的文件夹就创建
    dirs = 'materials/'+ title + "/clean_jpg/"
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    # 读取图片
    img = cv2.imdecode(np.fromfile('materials/'+ title + "/web_jpg/" + str(i) + ".jpg", dtype=np.uint8), cv2.IMREAD_COLOR)
    # 去除水印
    # hight, width, depth = img.shape[0:3]
    # 图片二值化处理，把[240, 240, 240]~[255, 255, 255]以外的颜色变成0
    thresh = cv2.inRange(img, np.array([num, num, num]), np.array([255, 255, 255]))
    # 创建形状和尺寸的结构元素
    kernel = np.ones((3, 3), np.uint8)
    # 扩张待修复区域
    hi_mask = cv2.dilate(thresh, kernel, iterations=1)
    specular = cv2.inpaint(img, hi_mask, 5, flags=cv2.INPAINT_TELEA)
    cv2.imencode('.jpg', specular)[1].tofile('materials/'+ title + "/clean_jpg/" + str(i) + ".jpg" )

    print("图片去水印，保存到：", 'materials/' + title + "/clean_jpg/")

# 切割图片躲开水印部分
def CutImage(i,title):
    # 打开一张图
    img = Image.open('materials/'+ title + "/web_jpg/" + str(i) + ".jpg")
    # 图片尺寸
    img_size = img.size
    h = img_size[1]  # 图片高度
    w = img_size[0]  # 图片宽度

    x = 0.05 * w
    y = 0.05 * h
    w = 0.9 * w
    h = 0.9 * h

    # 开始截取
    region = img.crop((x, y, x + w, y + h))
    # 保存图片
    region.save('materials/'+ title + "/clean_jpg/" + str(i) + ".jpg")

    print("按比例裁剪完毕，保存到：", 'materials/' + title + "/clean_jpg/")

# 改变图片尺寸 去除水印
def ChangeImage(i,title):
    # 读取图片
    img = cv2.imdecode(np.fromfile('materials/'+ title + "/clean_jpg/" + str(i) + ".jpg", dtype=np.uint8), cv2.IMREAD_COLOR)

    # 获取图片像素大小
    h , w , n = img.shape
    # 横板图片处理方式
    if w >= h :
        if w >= 1280:
            h = int((1280/w) * h)
            w = 1280
        elif w < 1280:
            h = int((1280/w) * h)
            w = 1280
        crop_size = ( w , h )
        img_new = cv2.resize(img, crop_size, interpolation = cv2.INTER_CUBIC)
        cv2.imencode('.jpg', img_new)[1].tofile('materials/'+ title + "/clean_jpg/" + str(i) + ".jpg" )
    # 竖板图片处理方式
    else:
        if h >= 720:
            w = int((720/w) * h)
            h = 720
        elif h < 720:
            w = int((720/w) * h)
            h = 720
        crop_size = ( h , w )
        img_new = cv2.resize(img, crop_size, interpolation = cv2.INTER_CUBIC)
        cv2.imencode('.jpg', img_new)[1].tofile('materials/'+ title + "/clean_jpg/" + str(i) + ".jpg" )

    print("图片按照按视频寸尺裁剪，保存到：",'materials/'+ title + "/clean_jpg/")

# 制作封面图片
def MakeCoverImage(title):
    # 加载背景图片
    base_img = Image.open('materials_base/封面.jpg')
    # 转换图片色到分别表示RGBA的值
    target = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    # 选择png图片显示的区域
    box = (390, 140, 1280, 720)
    # 加载素材图片
    region = Image.open('materials/' + title + "/clean_jpg/1.jpg")
    # 确保图片是RGBA格式，大小和box区域一样
    region = region.convert("RGBA")
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    # 将素材图片合成道底板图上
    target.paste(region, box)
    # 将背景图上假如生成号的素材地板透明背景图
    base_img.paste(target, (0, 0), target)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域，将底图显示出来。
    # base_img.show()
    base_img.save('materials/' + title + "/clean_jpg/cover.jpg")  # 保存图片
    print("封面图片制作完毕，目录：",'materials/' + title + "/clean_jpg/")