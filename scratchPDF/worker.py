#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
批量爬取PDF文档中的文本
'''

import os
import re
from scratchPDF import getPages
from csvExporter import csvWriter

def extractData():
    '''
    with open('./plainText', 'r') as fd:
        #patternNumber = r'((PATTERN\s*NUMBER\s*WHOLESALE\s*PRICE\s*SUGGESTED\s*RETAIL\sPRICE\s*){4})(([A-Z,\d]\d{3,4}\s*)+(\$\d{2,}\.\d\d\s*)+)+'
        regExp = r"PATTERN\s*NUMBER(.*?)You’ll Hear Us Smile"
        matchRet = re.findall(regExp, fd.read(), re.DOTALL)
    '''

    with open('output.csv', 'wb') as csvfile:
        fieldnames = ['Company Name', 'Annual Report Year', 'Salary Reporting Entry', 'Salary Cost Value', 'Currency', 'Report Download Link']
        csvWriter(csvfile, fieldnames)
        '''
        for item in matchRet:
            patternNum = []
            regExp = r"([A-Z]*\d{4,5})\t\n\n(\$\d{2,}\.\d{2})\s\t\n\n(\$\d{2,}\.\d{2})"
            ret = re.findall(regExp, item, re.DOTALL)
            for data in ret:
                csvWriter(csvfile, list(data))
        '''


def matchData(text):
    regExpr = re.compile("PATTERN\s*NUMBER\s*([A-Z]?\d{3,}\s*)+")
    match = regExpr.findall(text)
    print '>>>>>>>>>>>match result:'
    print match

def scratchPDFiles():
    fileList = os.listdir('./pdf')
    print fileList
    for file in fileList:
        pdfText = getPages('./pdf/' + file)
        textFile = file + '.txt'
        with open("./text/"+textFile, 'w') as fd:
            fd.write(pdfText)
        #matchData(pdfText)

if __name__=="__main__":
    print 'Working....'
    scratchPDFiles()
    #extractData()
