import numpy as np
from PIL import Image
import os
import xml.dom.minidom

def change_type(x):
    #将xml数据读取为整型
    t = ''
    for i in range(len(x)):
        t = t + x[i].firstChild.data
    t = int(t)
    return t

def jugde(image, x1, y1, x2, y2, s, c, a, b):
    if a <= 2 * b or b <= 2 * a:
        try:
            box = (x1, y1, x2, y2)
            region = image.crop(box)
            region.save('../backgroud_images/IMG_' + s + '_' + str(c) + '.jpg', 'jpeg')
        except:
            print(s)

if __name__ == '__main__':
    for n in range(1, 1500):
        s = "%06d" % n
        image_path = 'JPEGImages/IMG_' + s + '.jpg'
        xml_path = 'Annotations/IMG_' + s + '.xml'
        if (os.path.exists(image_path) and os.path.exists(xml_path)):
            image = Image.open(image_path)
            cols = image.size[0]  # 宽
            rows = image.size[1]  # 高
            dom = xml.dom.minidom.parse(xml_path)
            root = dom.documentElement
            x1 = change_type(root.getElementsByTagName('xmin'))
            y1 = change_type(root.getElementsByTagName('ymin'))
            x2 = change_type(root.getElementsByTagName('xmax'))
            y2 = change_type(root.getElementsByTagName('ymax'))
            jugde(image, 0, 0, x1, rows, s, 1, x1, rows)  # 1
            jugde(image, x2, 0, cols, rows, s, 2, cols - x2, rows)  # 2
            jugde(image, 0, 0, x1, y1, s, 3, x1, y1)  # 3
            jugde(image, x2, 0, cols, y1, s, 4, cols - x2, y1)  # 4
            jugde(image, 0, y2, x1, rows, s, 5, x1, rows - y2)  # 5
            jugde(image, x2, y2, cols, rows, s, 6, cols - x2, rows - y2)  # 6
