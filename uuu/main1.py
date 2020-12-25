
import os
import sys
import shutil
import re
from call1 import *

path = r'D:'
operation = ''
class osError(Exception):
    pass
class exitError(Exception):
    pass
class has_exist_databases(Exception):
    pass
class not_exist_tables(Exception):
    pass
class has_exist_table(Exception):
    pass
class re_select_error(Exception):
    pass

print("welcome to my mysql")
print("语法介绍")
print("创建数据库:create database 数据库;")
print("删除数据库:drop database 数据库;")
print("显示所有数据库:show databases;")
print("切换数据库:use 数据库;")
print("创建表:create table 表(属性1，属性2);")
print("删除表:drop table 表;")
print("显示所有表:show tables;")
print("插入表:insert into 表(属性1，属性2) value(值1，值2);")
print("删除表中某项:delete from 表 where 属性1=值1;")
print("查询表:select 属性1,属性2|* from 表 where 属性=值;")
print("更改表:update table 表名 set 属性1=值 where 属性=值,必须修改对文件的读写权限，否则无法更改")
print("并集UNION:select * from 表名 union select * from 表名")
print("连接:join 表名(字段号) = 表名(字段号) 需要增加权限")
print("退出:exit")
def println(field,value):
    len_field=len(field)
    len_value=len(value)
    sum_1 = 0
    sum_2 = 0
    for i in field:
        if i =='':
            sum_1+=1
    for j in value:
        if j=='':
            sum_2+=1
    if sum_1!=len_field and sum_2!=len_value:
        print(field,value)

def run():
    Initialization()
def Initialization():
    if not os.path.exists(path):
        os.mkdir(path)
database = 'sql'
while operation!='exit':
    run()
    cmd = database
    print('{0}>:'.format(cmd),end='')
    operation = input().strip()
    try:
        if operation == 'exit':
            raise exitError
        if operation[-1]!=';':
            raise AssertionError("语法错误")
        else:
            operation = operation.split(';')[0]

            if operation.split(' ')[0] == 'use' :
                path = r'D:'
                exist_database = operation.split(' ')[1]
                if exist_database in os.listdir(path):
                    database = exist_database
                    print('已经成功切换数据库为{0}'.format(database))
                    path = path + '\\' + database
                    cmd = database
                else:
                    raise osError
            if path == r'D:':
                if operation == 'show databases':
                    for i in os.listdir(path):
                        print(i)
                elif operation.split(' ')[0]+' '+operation.split(' ')[1]== 'drop database':
                    if operation.split(' ')[2] in os.listdir(path):
                        shutil.rmtree(path+'\\'+operation.split(' ')[2])
                        print("删除成功")
                    else:
                        raise osError
                elif operation.split(' ')[0]+' '+operation.split(' ')[1]=='create database':
                    if operation.split(' ')[2] not in os.listdir(path):
                        os.mkdir(path+'\\'+operation.split(' ')[2])
                        print('创建成功')
                    else:
                        raise has_exist_databases
                else:
                    raise AssertionError
            if path == 'D:\\'+database and database!='':
                if operation == 'show tables':
                    print(path)
                    for i in os.listdir(path):
                        print(i.split('.')[0])
                if operation.split(' ')[0]+' '+operation.split(' ')[1] == 'create table':
                    name = operation.split(' ')[2].split('(')[0]
                    if name not in [i.split('.')[0] for i in os.listdir(path)]:
                        fields = operation.split('(')[1].split(')')[0].split(',')
                        create_wb(cmd,name,*fields)
                    else:
                        raise has_exist_table
                if operation.split(' ')[0]+' '+operation.split(' ')[1]=='drop table':
                    if operation.split(' ')[2] in [i.split('.')[0] for i in os.listdir(path)]:
                        os.remove(path+'\\'+operation.split(' ')[2]+'.xls')
                    else:
                        raise not_exist_tables
                if operation.split(' ')[0]+' '+operation.split(' ')[1]=='update table' and operation.split(' ')[3]=='set':
                    re_select=re.match(r'update table (.*) set (.*)=(.*) where (.*)=(.*)$',operation)
                    if re_select!=None:
                        if re_select.group(1) in [i.split('.')[0] for i in os.listdir(path)]:
                            name = re_select.group(1)
                            alter_wb_where(cmd,name,re_select.group(2),re_select.group(3),re_select.group(4),re_select.group(5))
                            print("更新")
                    else:
                        print('...')
                if operation.split(' ')[0]=='select':
                    re_select = re.match(r'^select (.*) from (.*)$',operation)
                    re_select_where = re.match(r'select (.*) from (.*) where (.*)=(.*)$',operation)
                    if re_select!=None and operation.find('where')==-1:
                        if re_select.group(2) in [i.split('.')[0] for i in os.listdir(path)]:
                            name = re_select.group(2)
                            select_wb(cmd, name,re_select.group(1))
                        else:
                            raise not_exist_tables
                    if re_select_where!=None:
                        if re_select_where.group(2) in [i.split('.')[0] for i in os.listdir(path)]:
                            name = re_select_where.group(2)
                            select_wb_where(cmd,name,re_select_where.group(3),re_select_where.group(4),re_select_where.group(1))
                        else:
                            raise not_exist_tables
                    if 'union' in operation.split(' '):
                        re_select = re.match(r'select (.*) from (.*) union select (.*) from (.*)', operation)
                        if re_select != 'None':
                            if re_select.group(2) in [i.split('.')[0] for i in os.listdir(path)] and re_select.group(4) in [i.split('.')[0] for i in os.listdir(path)]:
                                namea = re_select.group(2)
                                nameb = re_select.group(4)
                                union_wb(database, namea, nameb)
                            else:
                                raise not_exist_tables
                        else:
                            raise re_select_error
                if operation.split(' ')[0]+' '+operation.split(' ')[1]=='insert into':
                    re_select = re.match(r'insert into (.*)\((.*)\) value\((.*)\)', operation)
                    if re_select!='None':
                        if re_select.group(1) in [i.split('.')[0] for i in os.listdir(path)]:
                            name = re_select.group(1)
                            fields = re_select.group(2).split(',')
                            values = re_select.group(3).split(',')
                            insert_wb(database,name,fields,values)
                        else:
                            raise not_exist_tables
                if operation.split(' ')[0] + ' ' + operation.split(' ')[1] == 'delete from':
                    name = operation.split(' ')[2]
                    if operation.split(' ')[3]=='where':
                        field = operation.split(' ')[4].split('=')[0]
                        value = operation.split(' ')[4].split('=')[1]
                        delete_wb(database,name,field,value)

                    else:
                        raise AssertionError
                if operation.split(' ')[0] == 'join':
                    re_select = re.match(r'join (.*)\((.*)\) = (.*)\((.*)\)', operation)
                    if re_select != 'None':
                        if re_select.group(1) in [i.split('.')[0] for i in os.listdir(path)] and re_select.group(3) in [
                            i.split('.')[0] for i in os.listdir(path)]:
                            namea = re_select.group(1)
                            nameb = re_select.group(3)
                            numa = re_select.group(2)
                            numb = re_select.group(4)
                            lianjie_wb(database, namea, nameb, numa, numb)
                        else:
                            raise not_exist_tables
                    else:
                        raise re_select_error
    except AssertionError:
        print("语法错误")
    except exitError:
        print('成功退出',end=' ')
        sys.exit()
    except osError:
        print('该数据库不存在')
    except has_exist_databases:
        print('该数据库已存在')
    except not_exist_tables:
        print('该表不存在请重新输入')
    except has_exist_table:
        print('表已存在 请勿重复创建')
    except re_select_error:
        print('查询语句出错')
    except field_not_exist_error as e:
        print(e.args[0])