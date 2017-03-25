#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import fnmatch

'''
遍历指定目录下的所有文件和子目录,统计文件中的行数.
可指定要统计的文件类型
'''

def listAllFiles(root, patterns='*', singleLevel=False, yieldFolders=False):
    '''
    这是一个生成器,返回指定目录下所有的文件名
    '''
    # 将文件名匹配模式从字符串(以;间隔)取出放入列表中
    patterns = patterns.split(';')

    for path, subdirs, files in os.walk(root):
        if yieldFolders:
            files.extend(subdirs)

        files.sort()
        for fileName in files:
            for pattern in patterns:
                if fnmatch.fnmatch(fileName, pattern):
                    yield os.path.join(path, fileName)
                    break

        if singleLevel:
            break

def countFileLines(filesList):
    '''
    遍历文件列表,计算文件行数
    '''
    totalCount = 0

    for fileName in filesList:
        with open(fileName, 'rU') as fd:
            for count, line in enumerate(fd, start=1):
                pass
            totalCount += count

    return totalCount

if __name__=='__main__':
    argNumber = len(sys.argv) - 1
    if argNumber < 1 or argNumber > 4:
        print '使用方法: ' + sys.argv[0] + ' 目录绝对路径' + ' [匹配模式]'
        print '\n'
        print '          目录绝对路径: 要统计的文件顶层目录绝对路径'
        print '          匹配模式: 匹配要统计的文件名后缀,使用分号间隔多个匹配模式'
        print '示例:'
        print "python " + sys.argv[0] + " \"/home/django\" \"*.py;*.c\""
        sys.exit(1)

    path = sys.argv[1]
    patterns = sys.argv[2]
    files = list(listAllFiles(path, patterns))
    print countFileLines(files)
