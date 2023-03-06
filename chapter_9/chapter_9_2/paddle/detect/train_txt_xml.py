# -*- coding: utf-8 -*-

##输出“”   {}
from xml.etree.ElementTree import ElementTree,Element
import xml.etree.ElementTree as ET
import cv2 
import numpy as np


def save_train_txt(file_write,label,num):
    m=0
    while m <= num:   
        if(m%10 != 0):
            tree = ET.parse('data/{0}/xml/{1}.xml'.format(str(label),str(m)))
            root = tree.getroot()
            #遍历文件所有的tag 为目标的值得标签
            for elem in root.iter('xmin'):
                a=int(elem.text)
            for elem in root.iter('ymin'):
                b=int(elem.text)
            for elem in root.iter('xmax'):
                c=int(elem.text)
            for elem in root.iter('ymax'):
                d=int(elem.text)
            for elem in root.iter('name'):
                e=str(elem.text)

            file_write.write("data/{1}/jpg/{0}.jpg\t{{\"value\":\"{1}\",\"coordinate\":[[{2},{3}],[{4},{5}]]}}\n".format(str(m),e,str(a),str(b),str(c),str(d)))
            print("data/{1}/jpg/{0}.jpg\t{{\"value\":\"{1}\",\"coordinate\":[[{2},{3}],[{4},{5}]]}}\n".format(str(m),e,str(a),str(b),str(c),str(d)))
            file_write.flush()
            print(m)
        m +=1
def save_eval_txt(file_write,label,num):
    m=0
    while m < num:   
        if(m%10 == 0):
            tree = ET.parse('data/{0}/xml/{1}.xml'.format(str(label),str(m)))
            root = tree.getroot()
            #遍历文件所有的tag 为目标的值打标签
            for elem in root.iter('xmin'):
                a=int(elem.text)
            for elem in root.iter('ymin'):
                b=int(elem.text)
            for elem in root.iter('xmax'):
                c=int(elem.text)
            for elem in root.iter('ymax'):
                d=int(elem.text)
            for elem in root.iter('name'):
                e=str(elem.text)

            file_write.write("data/{1}/jpg/{0}.jpg\t{{\"value\":\"{1}\",\"coordinate\":[[{2},{3}],[{4},{5}]]}}\n".format(str(m),e,str(a),str(b),str(c),str(d)))
            print("data/{1}/jpg/{0}.jpg\t{{\"value\":\"{1}\",\"coordinate\":[[{2},{3}],[{4},{5}]]}}\n".format(str(m),e,str(a),str(b),str(c),str(d)))
            file_write.flush()
            print(m)
        m +=1

if __name__ == "__main__":
    file_write = open("./train.txt","a")
    
    save_train_txt(file_write,"no_entry",37)

    
    file_write = open("./eval.txt","a")
    save_eval_txt(file_write,"no_entry",37)

