from PIL import Image,ImageFilter
import os
import os.path
import xml.dom.minidom
import copy
import numpy as np
import random

def change_type(x):
    #将xml数据读取为整型
    t = ''
    for i in range(len(x)):
        t = t + x[i].firstChild.data
    t = int(t)
    return t

def change_xml(before, after):
    #改写xml
    after = str(after)
    for i in range(len(before)):
        before[i].firstChild.data = after


def change_angle(image, x1, y1, x2, y2):
    # 旋转四个随机角度
    cols = image.size[0]
    rows = image.size[1]
    x1c = change_type(x1)
    y1c = change_type(y1)
    x2c = change_type(x2)
    y2c = change_type(y2)
    angle = np.random.choice([90, 180, 270], 1)[0]
    if angle == 270:
        image = image.transpose(Image.ROTATE_270)
    elif angle == 180:
        image = image.transpose(Image.ROTATE_180)
    elif angle == 90:
        image = image.transpose(Image.ROTATE_90)

    if angle == 270:
        change_xml(x1, y1c)
        change_xml(x2, y2c)
        change_xml(y1, cols - x2c)
        change_xml(y2, cols - x1c)
    elif angle == 180:
        change_xml(x2, cols - x1c)
        change_xml(x1, cols - x2c)
        change_xml(y2, rows - y1c)
        change_xml(y1, rows - y2c)
    elif angle == 90:
        change_xml(x1, rows - y2c)
        change_xml(x2, rows - y1c)
        change_xml(y1, x1c)
        change_xml(y2, x2c)
    return image


def change_region(image, x1, y1, x2, y2):
    # 随机移动目标位置
    cols = image.size[0]
    rows = image.size[1]
    x1c = change_type(x1)
    y1c = change_type(y1)
    x2c = change_type(x2)
    y2c = change_type(y2)
    box = (x1c, y1c, x2c, y2c)
    region = image.crop(box)
    #原先位置加高斯模糊
    img_blur = region.filter(ImageFilter.GaussianBlur(radius=10))
    image.paste(img_blur, box)
    # #原先位置用绿色代替(效果较差)
    # for i in range(x1c,x2c):
    #     for j in range(y1c,y2c):
    #         r, g, b = image.getpixel((i, j))
    #         r = 132
    #         g = 147
    #         b = 42
    #         image.putpixel((i, j), (r, g, b))
    x1r = random.randint(0, cols - x2c + x1c)
    y1r = random.randint(0, rows - y2c + y1c)
    x2r = x1r + x2c - x1c
    y2r = y1r + y2c - y1c
    change_xml(x1, x1r)
    change_xml(x2, x2r)
    change_xml(y1, y1r)
    change_xml(y2, y2r)
    box = (x1r, y1r, x2r, y2r)
    isrotate = random.randint(0, 1)
    # 随机添加上下翻转
    if (isrotate == 1):
        region = region.transpose(Image.ROTATE_180)
    image.paste(region, box)
    return image


# def roll(image, delta):
#     #旋转任意角度，未完成
#     "Roll an image sideways"
#
#     xsize, ysize = image.size
#
#     delta = delta % xsize
#     if delta == 0: return image
#
#     part1 = image.crop((0, 0, delta, ysize))
#     part2 = image.crop((delta, 0, xsize, ysize))
#     image.paste(part2, (0, 0, xsize-delta, ysize))
#     image.paste(part1, (xsize-delta, 0, xsize, ysize))
#
#     return image


if __name__ == '__main__':
    for n in range(1, 1500):
        try:            
            # n = 1
            # s = n.zfill(6)
            # 生成图像和xml的路径
            s = "%06d" % n
            c = '_'
            image_path = 'JPEGImages/IMG_' + s + '.jpg'
            xml_path = 'Annotations/IMG_' + s + '.xml'
            # 判断路径文件是否存在
            if (os.path.exists(image_path) and os.path.exists(image_path)):
                image = Image.open(image_path)
                # xml = copy.deepcopy(xml_path)
                dom = xml.dom.minidom.parse(xml_path)
                root = dom.documentElement
                x1 = root.getElementsByTagName('xmin')
                y1 = root.getElementsByTagName('ymin')
                x2 = root.getElementsByTagName('xmax')
                y2 = root.getElementsByTagName('ymax')

                # 获取指定像素RGB值
                # x1c = change_type(x1)
                # y1c = change_type(y1)
                # x2c = change_type(x2)
                # y2c = change_type(y2)
                # r, g, b = image.getpixel((x1c+1, y2c+1))
                # print(r,g,b)

                # 暂时只支持单一功能，若样本数量仍不够，考虑组合两功能
                # image = change_angle(image, x1, y1, x2, y2)
                # c = c + 'a'
                image = change_region(image, x1, y1, x2, y2)
                c = c + 'r'
                #
                # 生成图片和XML文件
                # Image.fromarray(image.astype(np.uint8)).save(path + s + c + '.jpg')
                image.save('JPEGImages/IMG_' + s + c + '.jpg', 'jpeg')
                with open('Annotations/IMG_' + s + c + '.xml', 'w') as fh:
                    dom.writexml(fh)
        except:
            print(s)
