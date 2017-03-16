#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
提取出PDF文档中的文本和JPEG格式图片
'''

import sys
import os
from binascii import b2a_hex
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator

def withPDF(pdfDoc, pdfPwd, fn, *args):
    '''
    装饰器完成一系列的初始化动作
    fn: 高阶函数(higher-order function)实现PDF文件信息的提取
    '''
    result = None
    try:
        # 打开PDF文件
        fp = open(pdfDoc, 'rb')
        # 创建PDF文件解析器对象
        parser = PDFParser(fp)
        # 创建PDF文档对象，用来存放解析出的文档结构
        doc = PDFDocument(parser, pdfPwd)

        if doc.is_extractable:
            result = fn(doc, *args)

        # 关闭PDF文档
        fp.close()
    except IOError:
        # 文件不存在或类似异常
        pass

    return result

def toByteString(s, enc='utf-8'):
    '''
    Convert the given unicode string to bytestring,
    using the standard encoding, unless it's already
    a bytestring
    '''
    if s:
        if isinstance(s, str):
            return s
        else:
            return s.encode(enc)

def updatePageTextHash(h, layoutObj, pct=0.2):
    '''
    PDF文档如果是页面中有多栏,例如论文常使用这种排版方式,可能
    导致文本段落之间乱序.
    每个layoutObj对象都有bbox(bounding box)属性,使用一个4元组
    (x0,y0,x1,y1)表示该对象在页面中的位置.使用x0,x1来定位每一
    栏文本的位置,组成hash字典,位置定位保持上下20%的误差.
    '''
    # x0表示文本的左偏移量
    x0 = layoutObj.bbox[0]
    # x1表示文本的宽度
    x1 = layoutObj.bbox[2]
    keyFound = False

    for k, v in h.items():
        # 同一栏的文本对象组成字典中的一对key-value
        hash_x0 = k[0]
        if x0 >= (hash_x0 * (1.0 - pct)) and (hash_x0 * (1.0 + pct)) >= x0:
            hash_x1 = k[1]
            if x1 >= (hash_x1 * (1.0 - pct)) and (hash_x1 * (1.0 + pct)) >= x1:
                keyFound = True
                v.append(toByteString(layoutObj.get_text()))
                h[k] = v

    if not keyFound:
        # 建立文本字典,字典的key是元组(x0,x1),value是文本
        h[(x0,x1)] = [toByteString(layoutObj.get_text())]

    return h

def determineImageType(streamFirst4Bytes):
    '''
    基于头4个字节找出图片文件类型
    '''
    fileType = None
    bytesAsHex = b2a_hex(streamFirst4Bytes)
    if bytesAsHex.startswith('ffd8'):
        fileType = '.jpeg'
    elif bytesAsHex == '89504e47':
        fileType = '.png'
    elif bytesAsHex == '47494638':
        fileType = '.gif'
    elif bytesAsHex.startswith('424d'):
        fileType = '.bmp'

    return fileType
    
def writeFile(folder, fileName, fileData, flags='w'):
    '''
    写数据到文件
    flags: 'w' 写, 'wb' 写二进制文件, 'a' 追加写
    '''
    result = False

    if os.path.isdir(folder):
        try:
            fileObj = open(os.path.join(folder, fileName), flags)
            fileObj.write(fileData)
            fileObj.close
            result = True
        except IOError:
            pass

    return result


def saveImage(layoutImage, pageNumber, imagesFolder):
    '''
    保存PDF文档中的(JPEG)图片,返回图片文件名
    '''
    result = None
    if layoutImage.stream:
        fileStream = layoutImage.stream.get_rawdata()
        fileExt = determineImageType(fileStream[0:4])
        if fileExt:
            fileName = ''.join([str(pageNumber), '_', layoutImage.name, fileExt])
            if writeFile(imagesFolder, fileName, layoutImage.stream.get_rawdata(), flags='wb'):
                result = fileName

    return result

def parseLayoutObjs(layoutObjs, pageNumber, imagesFolder, text=[]):
    '''
    遍历layoutObjs对象,抓取文本和图片
    '''
    textContent = []

    pageText = {}
    for layoutObj in layoutObjs:
        if isinstance(layoutObj, LTTextBox) or isinstance(layoutObj, LTTextLine):
            # 文本
            textContent.append(toByteString(layoutObj.get_text()))
            #pageText = updatePageTextHash(pageText, layoutObj)
        elif isinstance(layoutObj, LTImage):
            # 图片,保存到指定目录,标注它在文本中的位置
            '''
            saveFile = saveImage(layoutObj, pageNumber, imagesFolder)
            if saveFile:
                # 用HTML的<img />在文本中标签记录图片位置
                textContent.append('<img src="'+os.path.join(imagesFolder, saveFile)+'" />')
            else:
                print >> sys.stderr, "Error saving image on page", pageNumber, layoutObj.__repr__
            '''
        elif isinstance(layoutObj, LTFigure):
            # LTFigure对象包含了其它LT*对象
            textContent.append(parseLayoutObjs(layoutObj._objs, pageNumber, imagesFolder, textContent))

    #for k, v in sorted([(key,value) for (key,value) in pageText.items()]):
        # 按照每一栏的x0,x1位置排序,按照从上到下,从左到右的顺序输出文本
        #textContent.append('\n'.join(v))

    return '\n'.join(textContent)

def _parsePages(doc, imagesFolder):
    '''
    解析所有PDF页面,传递给withPDF()
    每个页面对应一个layout对象,称为LTPage对象,它包含几种子对象,
    例如,文本框(LTTextBox),图片(LTImage)等
    '''
    # 创建PDF资源管理对象
    rsrcmgr = PDFResourceManager()
    # 设置分析参数
    laparams = LAParams()
    # 创建PDF页面聚合对象
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建PDF解释器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # 字符串列表,列表元素代表每一页的文本
    textContent = []

    for i, page in enumerate(PDFPage.create_pages(doc)):
        interpreter.process_page(page)
        # 接收页面的LTPage对象
        layout = device.get_result()
        textContent.append(parseLayoutObjs(layout._objs, (i+1), imagesFolder))

    return textContent

def getPages(pdfDoc, pdfPwd='', imagesFolder='/temp'):
    '''
    处理PDF文档中的每个页面
    '''
    return '\n\n'.join(withPDF(pdfDoc, pdfPwd, _parsePages, *tuple([imagesFolder])))

if __name__=="__main__":
    getPages('./pdf/print.pdf')
    print 'Scratch pdf file end'
