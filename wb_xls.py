from turtle import pd

import xlwt
import xlrd
import pandas as pb
import shutil
from xlutils.copy import copy
from print_op import println
'''
获取sheet名：sheet1.name
获取总行数：sheet1.nrows
获取总列数：sheet1.ncols
'''
class field_not_exist_error(Exception):
    pass
class value_not_exist_error(Exception):
    pass
class field_not_match_value(Exception):
    pass
class has_not_field(Exception):
    pass
class has_not_value(Exception):
    pass
list_all_wb = []
def create_wb(database,name,*args):
    wb_path = 'F:\mysql'+'\\'+database+'\\'+name
    wb = xlwt.Workbook()
    sh1 = wb.add_sheet(name)
    # 第一个参数是行，第二个参数是列，第三个参数是value
    for key,i in enumerate(args):
        sh1.write(0,key,i)
    wb.save(wb_path+'.xls')
    print('{0}表创建成功'.format(name))
    list_all_wb.append(wb_path)
def alter_wb(name):
    pass
def select_wb1(database,name,limit_num1,*fields):
    wb_path = 'F:\mysql' + '\\' + database + '\\' + name
    wb = xlrd.open_workbook(wb_path+'.xls')
    limit_num1 = int(limit_num1)
    limit_num = 1
    if len(*fields)>=1:
        x = [str(i) for i in wb.sheet_by_index(0).row_values(0)]
        wb_value = wb.sheet_by_index(0)
        wb_field = []
        for i in x:
            if i[-1]=='0':
                i = i.split('.')[0]
            wb_field.append(i)
        #处理 传入字段逗号问题**************************
        for i in fields:
            field = i
        fields = str(field).split(',')
        #/*******************************************
        if field!='*':
            try:
                for field in fields:
                    if field not in wb_field:
                        raise field_not_exist_error(field)
            except field_not_exist_error:
                print('{0}字段不存在'.format(field))
        for field in fields:
            if field in wb_field:
                index = wb_field.index(field)
                println([field],wb_value.col_values(index)[1:])
        if field=='*':

            for field in wb_field:
                if limit_num <= limit_num1:
                    index = wb_field.index(field)
                    limit_num+=1
                    println([field],wb_value.col_values(index)[1:])
def select_wb(database,name,*fields):
    wb_path = 'F:\mysql' + '\\' + database + '\\' + name
    wb = xlrd.open_workbook(wb_path+'.xls')
    limit_num = 1
    if len(*fields)>=1:
        x = [str(i) for i in wb.sheet_by_index(0).row_values(0)]
        wb_value = wb.sheet_by_index(0)
        wb_field = []
        for i in x:
            if i[-1]=='0':
                i = i.split('.')[0]
            wb_field.append(i)
        #处理 传入字段逗号问题**************************
        for i in fields:
            field = i
        fields = str(field).split(',')
        #/*******************************************
        if field!='*':
            try:
                for field in fields:
                    if field not in wb_field:
                        raise field_not_exist_error(field)
            except field_not_exist_error:
                print('{0}字段不存在'.format(field))
        for field in fields:
            if field in wb_field:
                index = wb_field.index(field)
                println([field],wb_value.col_values(index)[1:])
        if field=='*':
            for field in wb_field:
                index = wb_field.index(field)
                limit_num+=1
                println([field],wb_value.col_values(index)[1:])
def select_wb_where(database,name,where_field,where_value,*fields):
    int1 = 0
    wb_path = 'F:\mysql' + '\\' + database + '\\' + name
    wb = xlrd.open_workbook(wb_path + '.xls')
    if len(*fields) >= 1:
        x = [str(i) for i in wb.sheet_by_index(0).row_values(0)]
        wb_value = wb.sheet_by_index(0)
        wb_field = []
        row_number = []
        # 处理 传入字段逗号问题**************************
        for i in fields:
            field = i
        fields = str(field).split(',')
        # /*******************************************
        for i in x:
            if i[-1] == '0':
                i = i.split('.')[0]
            wb_field.append(i)
        try:
            #待查字段在不在表中
            if field != '*':
                for field in fields:
                    if field not in wb_field:
                        str1 = '没有{0}字段'.format(field)
                        raise field_not_exist_error(str1)
            #where后字段
            if where_field not in wb_field:
                str1 = '没有{0}字段'.format(field)
                raise field_not_exist_error(str1)
            col_num = wb_field.index(where_field)
            if where_value not in [str(i) for i in wb_value.col_values(col_num)[1:]]:
                str1 = '没有{0}属性'.format(where_value)
                raise has_not_value(str1)
            else:
                for key,i in enumerate([str(i) for i in wb_value.col_values(col_num)[1:]]):
                    if i==where_value:
                        row_number.append(key+1)
            if int1<=5:
                for i in row_number:
                    if field!='*':
                        for field in fields:
                            if field in wb_field:
                                index = wb_field.index(field)
                                int1+=1
                                println([field], [wb_value.row_values(i)[index]])
                        print('---------------------------------------')
            if int1<=5:
                for i in row_number:
                    if field == '*':
                        for j in wb_field:
                            index = wb_field.index(j)
                            int1+=1
                            println([j], [wb_value.row_values(i)[index]])
                        print('--------------------------')
        except has_not_value as e:
            print(e.args[0])
        except has_not_field:
            print(has_not_field.args[0])
def insert_wb(database,name,fields,values):
    wb_path = 'F:\mysql' + '\\' + database + '\\' + name
    wb = xlrd.open_workbook(wb_path + '.xls')
    wb_value = wb.sheet_by_index(0)
    x = [str(i) for i in wb.sheet_by_index(0).row_values(0)]
    wb_field = []
    c_wb = copy(wb)
    ws=c_wb.get_sheet(0)
    for i in x:
        if i[-1] == '0':
            i = i.split('.')[0]
        wb_field.append(i)
    try:
        for field in fields:
            if field not in wb_field:
                raise field_not_exist_error(field)
        for key,field in enumerate(fields):
            #获得列数
            col_number = wb_field.index(field)
            row_number = len(wb_value.col_values(col_number))
            ws.write(row_number,col_number,values[key])
        c_wb.save(wb_path + '.xls')
        print('成功插入数据')
    except field_not_exist_error:
        print('{0}字段不存在'.format(field))
def delete_wb(database,name,field,value):
    wb_path = 'F:\mysql' + '\\' + database + '\\' + name
    wb = xlrd.open_workbook(wb_path + '.xls')
    wb_value = wb.sheet_by_index(0)
    x = [str(i) for i in wb.sheet_by_index(0).row_values(0)]
    wb_field = []
    c_wb = copy(wb)
    ws = c_wb.get_sheet(0)
    for i in x:
        if i[-1] == '0':
            i = i.split('.')[0]
        wb_field.append(i)
    counter = []
    if field in wb_field:
        col_num = wb_field.index(field)
        col_value = wb_value.col_values(col_num)[1:]
        col_allnum = len(wb_field)
        if value in col_value:
            for key,i in enumerate(col_value):
                if i==value:
                    counter.append(key+1)
            for i in counter:
                for j in range(col_allnum):
                    ws.write(i,j,'')
            print('删除成功')
            c_wb.save(wb_path + '.xls')
        else:
            raise value_not_exist_error(value)
    else:
        raise field_not_exist_error(field)
def update_wb(database,name,table1,value1,table2,value2):
    wb_table=table2
    wb_values=value2
    wb_tablea=table1
    wb_valuesa=value1
    wb_path = 'F:\mysql' + '\\' + database + '\\' + name
    wb = xlrd.open_workbook(wb_path + '.xls')
    x = [str(i) for i in wb.sheet_by_index(0).row_values(0)]
    wb_field = []
    c_wb = copy(wb)
    ws = c_wb.get_sheet(0)
    for i in x:
        if i[-1] == '0':
            i = i.split('.')[0]
        wb_field.append(i)
    try:
        for field in table1:
            if field not in wb_field:
                raise field_not_exist_error(field)
        for field in table2:
            if field not in wb_field:
                raise field_not_exist_error(field)
    except field_not_exist_error:
        pass
#########修改数据######################################
    a = wb_field.index(wb_table)
    value = wb.sheet_by_index(0).col_values(a)
    #获得指定值的行数
    y = [i for i, x in enumerate(value) if x == wb_values]
    b=wb_field.index(wb_tablea)
    try:
        for y1 in y:
            ws.write(y1,b,wb_valuesa)
        c_wb.save(wb_path + '.xls')
        print('成功修改数据')
    except:
        raise field_not_exist_error
def lianjie_wb(database,name1,name2,numa,numb):
    wb_path = 'F:\mysql' + '\\' + database + '\\' + name1
    wb_path1 = 'F:\mysql' + '\\' + database + '\\' + name2
    Count1 = int(numa) -1
    Count2 = int(numb) -1
    sheet_value = []
    wb = xlrd.open_workbook(wb_path + '.xls')
    wb_value = wb.sheet_by_index(0)
    for sh in wb.sheets():
        tmp = []
        for r in range(sh.nrows):
            tmp.append(wb_value.row_values(r))
        sheet_value=tmp
    Table1_txt=sheet_value
    print(Table1_txt)



    sheet_value1 = []
    wb1 = xlrd.open_workbook(wb_path1 + '.xls')
    wb1_value = wb1.sheet_by_index(0)
    for sh in wb1.sheets():
        tmp = []
        for r in range(sh.nrows):
            tmp.append(wb1_value.row_values(r))
        sheet_value1=tmp

    Table2_txt = sheet_value1

    total = []
    for i in range(len(Table1_txt)):
        tmp=[]
        for j in range(len(Table2_txt)):
            if str(Table1_txt[i][Count1]) == str(Table2_txt[j][Count2]):
                for x in range(len(Table1_txt[i])):
                    if x == Count1:
                        continue
                    Table2_txt[j].append(Table1_txt[i][x])
                tmp = Table2_txt[j]
                total.append(tmp)
                break
    print(total)
    c_wb = copy(wb1)
    ws = c_wb.get_sheet(0)
    for i in range(0, len(total)):
        for j in range(0, len(total[i])):
            ws.write(i, j, str(total[i][j]))
    c_wb.save(wb_path1 + '.xls')
    print("写入数据成功！")
def union_wb(database,name1,name2):
    wb_path = 'F:\mysql' + '\\' + database + '\\' + name1
    w1b = xlrd.open_workbook(wb_path + '.xls')
    wb = pb.read_excel(wb_path + '.xls')
    array1 = wb.values
    x = [str(i) for i in w1b.sheet_by_index(0).row_values(0)]
    wb_path1 = 'F:\mysql' + '\\' + database + '\\' + name2
    wb1 = pb.read_excel(wb_path1 + '.xls')
    array2 = wb1.values
    print(x)
    for x1 in array1:
        print(x1)
    for y in array2:
        print(y)