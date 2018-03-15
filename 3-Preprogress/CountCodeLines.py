# -*- coding: utf8 -*-
import xlrd
import re
import os
#获取字符串中的特定位置的数字。如Diff: 110 lines中的110
#获取字符串中的特定位置的数字。如Diff: 110 lines中的110
#获取字符串中的特定位置的数字。如Diff: 110 lines中的110
fname = "E:\\1.xlsx"
bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
try:
    sh = bk.sheet_by_name("Sheet1")
except:
    print "no sheet in %s named Sheet1" % fname
# 获取行数
nrows = sh.nrows
# 获取列数
ncols = sh.ncols
row_list = []
#print "nrows %d, ncols %d" % (nrows, ncols)
# 获取第一行第一列数据
for i in xrange(0,nrows):
    rowValues= sh.row_values(i) #某一行数据
    for item in rowValues:
        relink1 = 'Diff: (.*) lines'
        text=re.findall(relink1, item)
        row_list.append(text)

while '' in row_list:
    row_list.remove('')

file=open('E:\\result.xls','w')
for row_list_line in row_list:
    file.write(str(row_list_line))
    file.write('\n')
file.close()