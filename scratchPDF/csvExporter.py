#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def csvWriter(csvfile, row):
    writer = csv.writer(csvfile)
    writer.writerow(row)

if __name__=='__main__':
    pass
