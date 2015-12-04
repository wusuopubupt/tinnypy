#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import sys
import xlrd

#打开excel
def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)

#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file= 'file.xls',colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for i in range(1,nrows):
         row = table.row_values(i)
         if row:
                 #print row[i]
             imgh_url = row[0]
             title = row[1]
             sub_title = row[2]
             sql = "INSERT INTO block_content_list(block_sign,imgh_url,title,sub_title) VALUES('xiu8_2','%s','%s','%s');" % (imgh_url,title,sub_title)
             print sql
             list.append(sql)
    return list

def main():
    reload(sys) 
    sys.setdefaultencoding('utf-8')
    tables = excel_table_byindex()
   #for row in tables:
   #    print row

if __name__=="__main__":
    main()
