from wb_xls import *
from print_op import println
import os
import sys
import shutil
import re
#根据路径名不同 ，来创建增删 库
path = 'F:\mysql'
opration = ''
# 自定义异常类
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
#操作（顺带着库操作）。
database = 'mysql'
if not os.path.exists(path):
    os.mkdir(path)
while opration!='exit':
    cmd = database
    print('{0}>:'.format(cmd),end='')
    opration = input().strip()
    try:
        if opration == 'exit':
            raise exitError
        ## 语法处理模块
        if opration[-1]!=';':
            raise AssertionError("语法错误")
        else:
            opration = opration.split(';')[0]
            #共有操作******************************************************
            # 选择库
            if opration.split(' ')[0] == 'use' :
                path = 'F:\mysql'
                exist_database = opration.split(' ')[1]
                if exist_database in os.listdir(path):
                    database = exist_database
                    print('已经成功切换数据库为{0}'.format(database))
                    path = path + '\\' + database
                    cmd = database
                else:
                    raise osError
            #**************************************************************
            #库操作*******************************************************
            if path == 'F:\mysql':
                #查库
                if opration == 'show databases':
                    for i in os.listdir(path):
                        print(i)
                #删库
                elif opration.split(' ')[0]+' '+opration.split(' ')[1]== 'drop database':
                    if opration.split(' ')[2] in os.listdir(path):
                        shutil.rmtree(path+'\\'+opration.split(' ')[2])
                    else:
                        raise osError
                #创建库
                elif opration.split(' ')[0]+' '+opration.split(' ')[1]=='create database':
                    if opration.split(' ')[2] not in os.listdir(path):
                        os.mkdir(path+'\\'+opration.split(' ')[2])
                        print('创建成功')
                    else:
                        raise has_exist_databases
                else:
                    raise AssertionError
            # 表操作*******************************************************
            if path == 'F:\mysql\\'+database and database!='':
                # 查表
                if opration == 'show tables':
                    for i in os.listdir(path):
                        print(i.split('.')[0])
                #建表(无字段属性 可补充)

                if opration.split(' ')[0]+' '+opration.split(' ')[1] == 'create table':
                    name = opration.split(' ')[2].split('(')[0]
                    if name not in [i.split('.')[0] for i in os.listdir(path)]:
                        fields = opration.split('(')[1].split(')')[0].split(',')
                        create_wb(cmd,name,*fields)
                    else:
                        raise has_exist_table
                #删表
                if opration.split(' ')[0]+' '+opration.split(' ')[1]=='drop table':
                    if opration.split(' ')[2] in [i.split('.')[0] for i in os.listdir(path)]:
                        os.remove(path+'\\'+opration.split(' ')[2]+'.xls')
                    else:
                        raise not_exist_tables
                # 改
                if opration.split(' ')[0] == 'update':
                    re_select = re.match(r'update (.*) set (.*) = (.*) where (.*) = (.*)', opration)
                    if re_select != 'None':
                        if re_select.group(1) in [i.split('.')[0] for i in os.listdir(path)]:
                            name = re_select.group(1)
                            tablea = re_select.group(2)
                            valuea = re_select.group(3)
                            tableb = re_select.group(4)
                            valueb = re_select.group(5)
                            update_wb(database, name, tablea, valuea, tableb, valueb)
                        else:
                            raise not_exist_tables
                    else:
                        raise re_select_error
                if opration.split(' ')[0]=='select':
                    re_select = re.match(r'^select (.*) from (.*)$',opration)
                    re_select_where = re.match(r'select (.*) from (.*) where (.*)=(.*)$',opration)
                    if re_select!=None and opration.find('where')==-1 and opration.find('union')==-1 and opration.find('limit')!=-1:
                        if re_select.group(2).split(' ')[0] in [i.split('.')[0] for i in os.listdir(path)]:
                            name = re_select.group(2).split(' ')[0]
                            num = re_select.group(2).split(' ')[1].split(',')[1].split(')')[0]
                            select_wb1(cmd, name,num,re_select.group(1))
                        else:
                            raise not_exist_tables
                    if re_select!=None and opration.find('where')==-1 and opration.find('union')==-1 and opration.find('limit')==-1:
                        if re_select.group(2).split(' ')[0] in [i.split('.')[0] for i in os.listdir(path)]:
                            name = re_select.group(2).split(' ')[0]
                            select_wb(cmd, name,re_select.group(1))
                        else:
                            raise not_exist_tables
                    if re_select_where!=None:
                        if re_select_where.group(2) in [i.split('.')[0] for i in os.listdir(path)]:
                            name = re_select_where.group(2)
                            select_wb_where(cmd,name,re_select_where.group(3),re_select_where.group(4),re_select_where.group(1))
                        else:
                            raise not_exist_tables
                    if 'union' in opration.split(' '):
                        re_select = re.match(r'select (.*) from (.*) union select (.*) from (.*)', opration)
                        if re_select != 'None':
                            if re_select.group(2) in [i.split('.')[0] for i in os.listdir(path)] and re_select.group(4) in [i.split('.')[0] for i in os.listdir(path)]:
                                namea = re_select.group(2)
                                nameb = re_select.group(4)
                                union_wb(database, namea, nameb)
                            else:
                                raise not_exist_tables
                        else:
                            raise re_select_error
                #插入语句
                if opration.split(' ')[0]+' '+opration.split(' ')[1]=='insert into':
                    re_select = re.match(r'insert into (.*)\((.*)\) value\((.*)\)', opration)
                    if re_select!='None':
                        if re_select.group(1) in [i.split('.')[0] for i in os.listdir(path)]:
                            name = re_select.group(1)
                            fields = re_select.group(2).split(',')
                            values = re_select.group(3).split(',')
                            insert_wb(database,name,fields,values)
                        else:
                            raise not_exist_tables
                #删除语句
                if opration.split(' ')[0] + ' ' + opration.split(' ')[1] == 'delete from':
                    name = opration.split(' ')[2]
                    if opration.split(' ')[3]=='where':
                        field = opration.split(' ')[4].split('=')[0]
                        value = opration.split(' ')[4].split('=')[1]
                        delete_wb(database,name,field,value)
                    else:
                        raise AssertionError
                if opration.split(' ')[0] == 'join':
                    re_select = re.match(r'join (.*)\((.*)\) = (.*)\((.*)\)', opration)
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
        print('{0}字段不存在'.format(e.args[0]))
    except value_not_exist_error as e:
        print('{0}属性不存在'.format(e.args[0]))


