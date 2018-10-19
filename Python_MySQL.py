#__author__ = 'Eric'
#-*- coding: utf-8 -*-
# @Time    : 2018/8/20 11:55
# @FileName: MySQL.py

#在数据库中创建一个数据表
# CREATE TABLE account(
# 	number INT NOT NULL AUTO_INCREment PRIMARY KEY,
# 	acctid INT(11) DEFAULT NULL COMMENT "账户id" ,
# 	money INT(11) DEFAULT NULL COMMENT "余额"
# ) DEFAULT CHARSET 'UTF8';
#
#插入一些基本信息
# INSERT INTO account (acctid,money) VALUES
# 		( 1 , 110),
# 		( 2 , 10)
# ;

import MySQLdb
import sys

class TransferMoney(object):
    def __init__(self,conn):
        self.conn = conn

    def transfer(self,source_acctid,target_acctid,money):
        try:
            #检查两个账户能否使用
            self.check_acct_available(source_acctid)
            self.check_acct_available(target_acctid)
			
            #检查账户A是否有足够的100元
            self.check_acct_enoughmoney(source_acctid,money)
			
            #将付款人账户减去金额
            self.reduce_acct(source_acctid,money)
			
            #在收款人账户上增加金额
            self.add_acct(target_acctid,money)
			
            self.conn.commit()              #对执行的事务进行提交
        except Exception as e:
            self.conn.rollback()
            raise e

    def check_acct_available(self,acctid):
        cursor = self.conn.cursor()
        try:
            sql = 'SELECT * FROM account WHERE acctid=%s' % acctid
            cursor.execute(sql)
            print('check_acct_available:'+sql)
            rs = cursor.fetchall()
            if len(rs)!=1:          #使用SELECT语句检测是否执行一般用cursor.fetchall()
                raise Exception('账号%s不存在'%acctid)
        finally:
            cursor.close()

    def check_acct_enoughmoney(self,acctid,money):
        cursor = self.conn.cursor()
        try:
            sql = 'SELECT * FROM account WHERE acctid=%s and money>%s'%(acctid,money)
            cursor.execute(sql)
            rs = cursor.fetchall()
            if len(rs)!=1:
                raise Exception('账户%s没有足够的钱'%acctid)
        finally:
            cursor.close()

    def reduce_acct(self,acctid,money):
        cursor = self.conn.cursor()
        try:
            sql = 'UPDATE account set money=money-%s WHERE acctid=%s'%(money,acctid)
            cursor.execute(sql)
            if cursor.rowcount !=1:             #使用UPDATE语句检测是否执行一般用cursor.rowcount()
                raise Exception('账户%s减款失败'%acctid)
        finally:
            cursor.close()

    def add_acct(self,acctid,money):
        cursor = self.conn.cursor()
        try:
            sql = 'UPDATE account set money=money+%s WHERE acctid=%s' % (money, acctid)
            cursor.execute(sql)
            if cursor.rowcount != 1:  # 使用UPDATE语句检测是否执行一般用cursor.rowcount()
                raise Exception('账户%s加款失败' % acctid)
        finally:
            cursor.close()

def main():
    #命令行参数在pycharm中在Run选项下的Edit Configurations中设置，设置后再运行脚本
     source_acctid = sys.argv[1]    #1
     target_acctid = sys.argv[2]    #2
     money = sys.argv[3]        #100

     conn = MySQLdb.Connect(
         host = 'localhost',
         user = 'root',
         passwd = '123456',
         port = 3306,
         db = 'school'          #数据库名称
     )
     tr_money = TransferMoney(conn)     #创建一个类的对象

     try:
         tr_money.transfer(source_acctid,target_acctid,money)
     except Exception as e:
         print('出现的问题:' + str(e))


if __name__ == '__main__':
    main()
