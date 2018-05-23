# coding=utf-8
import os
import os.path
import xml.dom.minidom

path = "./Annotations"
files = os.listdir(path)  # 得到文件夹下所有文件名称
s = []
for xmlFile in files:  # 遍历文件夹
    if not os.path.isdir(xmlFile):  # 判断是否是文件夹,不是文件夹才打开
        print(xmlFile)

    # xml文件读取操作

    # 将获取的xml文件名送入到dom解析
    dom = xml.dom.minidom.parse(os.path.join(path, xmlFile))  ###最核心的部分os.path.join(path,xmlFile),路径拼接,输入的是具体路径
    root = dom.documentElement
    # 获取标签对name/pose之间的值
    #folder = root.getElementsByTagName('folder')
    name = root.getElementsByTagName('name')
    # 重命名class name
    #for i in range(len(folder)):
        #print(folder[i].firstChild.data)
        #folder[i].firstChild.data = 'VOC2007'
        #print(folder[i].firstChild.data)
    for i in range(len(name)):
        print(name[i].firstChild.data)
        name[i].firstChild.data = 'butterfly'
        print(name[i].firstChild.data)

        # 保存修改到xml文件中
    with open(os.path.join(path, xmlFile), 'w') as fh:
        dom.writexml(fh)
        print('写入 OK!')

    #with open('dom_write.xml','w',encoding='UTF-8') as fh:
             # 4.writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
             # 第四个参数制定了换行格式，第五个#参数制定了xml内容的编码。
     #   dom.writexml(fh,indent='',addindent='\t',newl='\n',encoding='UTF-8')
      #  print('写入xml OK!')
