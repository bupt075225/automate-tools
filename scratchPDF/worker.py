#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
批量爬取PDF文档中的文本
'''

import os
from scratchPDF import getPages

def scratchPDFiles():
    fileList = os.listdir('./pdf')
    print fileList
    for file in fileList:
        getPages('./pdf/' + file)

if __name__=="__main__":
    print 'Working....'
    scratchPDFiles()
