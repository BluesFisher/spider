#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
from DBUtils.PooledDB import PooledDB


class SqlObj(object):
    def __init__(self,
                 host='localhost',
                 port=3306,
                 username='root',
                 password='root',
                 database='my_python'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.db = None
        self.cursor = None

    def connect_db(self):
        # 创建连接池
        pool = PooledDB(creator=MySQLdb,
                        mincached=1,
                        maxcached=16,
                        host=self.host,
                        user=self.username,
                        passwd=self.password,
                        db=self.database,
                        port=self.port,
                        charset='utf8')
        self.db = pool.connection()
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT VERSION()")
        print "连接成功：Database version %s " % self.cursor.fetchone()

    def get_cursor(self):
        self.cursor = self.db.cursor()

    def close_db(self):
        self.cursor.close()
        self.db.close()

    def _deal_values(self, value):
        """
        self._deal_values(value) -> str or list
            处理传进来的参数
        """
        # 如果是字符串则加上''
        if isinstance(value, str):
            value = ("'{value}'".format(value=value))
        # 如果是字典则变成key=value形式
        elif isinstance(value, dict):
            result = []
            for key, value in value.items():
                value = self._deal_values(value)
                res = "{key}={value}".format(key=key, value=value)
                result.append(res)
            return result
        else:
            value = (str(value))
        return value

    def insert(self, table, insert_data, is_replace=False, need_close=True):
        '''
            insert(table, insert_data)
            添加数据到数据库
            str -> table 为字符串
            [{},{}] -> 为列表中嵌套字典类型
        '''
        self.connect_db()

        print insert_data

        try:
            for data in insert_data:
                key = ','.join(data.keys())
                values = map(self._deal_values, data.values())
                insert_data = ', '.join(values)

                action = 'insert' if not is_replace else 'replace'
                sql = (action + " into {table}({key}) values ({val})").format(
                    table=table, key=key, val=insert_data)

                print sql

                self.cursor.execute(sql)
                self.db.commit()

                print 'sql insert ok: ', sql
        except Exception as error:
            print 'sql insert err: ', error
        finally:
            if need_close:
                self.close_db()

    def delete(self, table, condition, need_close=True):
        '''
            delete(table, condition)
            删除数据库中的数据
            str -> table 字符串类型
            dict -> condition 字典类型
        '''
        self.connect_db()

        try:
            # 处理删除的条件
            condition_list = self._deal_values(condition)
            condition_data = ' and '.join(condition_list)

            # 构建sql语句
            sql = "delete from {table} where {condition}".format(
                table=table, condition=condition_data)

            self.cursor.execute(sql)
            self.db.commit()

            print 'sql delete ok: ', sql
        except Exception as error:
            print 'sql delete err: ', error
        finally:
            if need_close:
                self.close_db()

    def update(self, table, data, condition=None, need_close=True):
        """
            update(table, data, [condition])
            更新数据
            str -> table 字符串类型
            dict -> data 字典类型
            dict -> condition 字典类型
        """
        self.connect_db()

        try:
            # 处理传入的数据
            update_list = self._deal_values(data)
            update_data = ",".join(update_list)
            # 判断是否有条件
            if condition is not None:
                # 处理传入的条件
                condition_list = self._deal_values(condition)
                condition_data = ' and '.join(condition_list)
                sql = "update {table} set {values} where {condition}".format(
                    table=table, values=update_data, condition=condition_data)
            else:
                sql = "update {table} set {values}".format(table=table,
                                                           values=update_data)

            self.cursor.execute(sql)
            self.db.commit()

            print 'sql update ok: ', sql
        except Exception as error:
            print 'sql update err: ', error
        finally:
            if need_close:
                self.close_db()

    def get(self,
            table,
            show_list=['*'],
            condition=None,
            get_one=False,
            need_close=True):
        """
            get(table, show_list, [condition, get_one]) -> tupe
            获取数据 返回一个元祖
            str -> table 字符串类型
            list -> show_list 列表类型
            dict -> condition 字典类型
            boolean -> get_one 布尔类型
        """
        self.connect_db()
        result = ()
        try:
            # 处理显示的数据
            show_list = ",".join(show_list)
            sql = "select {key} from {table}".format(key=show_list,
                                                     table=table)
            # 处理传入的条件
            if condition:
                condition_list = self._deal_values(condition)
                condition_data = 'and'.join(condition_list)
                sql = "select {key} from {table} where{condition}".format(
                    key=show_list, table=table, condition=condition_data)

            self.cursor.execute(sql)

            result = self.cursor.fetchone(
            ) if get_one else self.cursor.fetchall()

            print 'sql get ok: ', sql
        except Exception as error:
            result = ()
            print 'sql get err: ', error
        finally:
            if need_close:
                self.close_db()
            return result


if __name__ == '__main__':
    sql_obj = SqlObj()
    sql_obj.insert('users', [{
        'phone': '15361420407',
        'password': '1234567',
        'name': 'zhen'
    }])
    # sql_obj.delete('users', {'phone': '13612817761'})
    # sql_obj.update('users', {'name': 'yu'}, {'phone': '13612817761'})
    # print sql_obj.get('users', ['name', 'phone'])
