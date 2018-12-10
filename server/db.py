import pymysql
from bottle import Bottle, route, request, response
import json


class Contact:

    def __init__(self, name, email, phone, company):
        self.name = name
        self.email = email
        self.phone = phone
        self.company = company


class DB(object):

    TABLE_NAME = "tb_address_book"

    conn = pymysql.connect(host='localhost',
                                user='root',
                                password='root',
                                db='contact_db',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    def createTable(self):
        # with DB.conn.cursor() as cursor:
        cursor = DB.conn.cursor()
        cursor.execute("""create table if not exists tb_address_book (
            pid int auto_increment, 
            name varchar(20) not null, 
            phone varchar(20) not null, 
            email varchar(20) not null, 
            company varchar(30), 
            primary key (pid));""")

    def query(self):
        try:
            by = request.query.by
            element = request.query.element

            print(by, element)
            cursor = DB.conn.cursor()
            if by and element:
                sql = "SELECT * FROM {} WHERE {}='{}'".format(DB.TABLE_NAME, by, element)
            else:
                sql = "SELECT * FROM {}".format(DB.TABLE_NAME)
            cursor.execute(sql)
            result = cursor.fetchall()
            print('query result: ', result)
            return str(result)
        except BaseException as e:
            DB.conn.rollback()
            print('query FAILED and rollback. ', e)
            return None

    def insert(self, contact):
        try:
            cursor = DB.conn.cursor()
            sql = "INSERT INTO {}(name, phone, email, company) VALUES('{}', '{}', '{}', '{}')".format(DB.TABLE_NAME, contact.name, contact.phone, contact.email, contact.company)
            cursor.execute(sql)
            DB.conn.commit()
            return True
        except BaseException as e:
            DB.conn.rollback()
            print(e)
            return False
    
    def delete(self, phone=None):
        if phone:
            print('phone = ', phone)
            try:
                cursor = DB.conn.cursor()
                sql = "DELETE FROM {} WHERE phone='{}'".format(DB.TABLE_NAME, phone)
                cursor.execute(sql)
                DB.conn.commit()
                response.status = 200
                return '''{
                    ret_code: 0,
                    ret_message: delete success
                }'''
            except BaseException as e:
                print(e)
                return '''{
                    ret_code: -1,
                    ret_message: delete failed, %s
                }''' % str(e)
        return True

    def update(self):
        oldPhone = request.query.oldPhone
        newPhone = request.query.newPhone
        newName = request.query.newName
        if oldPhone and newName and newPhone:
            try:
                cursor = DB.conn.cursor()
                sql = "UPDATE {} SET name='{}', phone='{}' WHERE phone='{}'".format(DB.TABLE_NAME, newName, newPhone, oldPhone)
                cursor.execute(sql)
                DB.conn.commit()
                response.status = 200
                return '''{
                    ret_code: 0,
                    ret_message: update success
                }'''
            except BaseException as e:
                print(e)
                return '''{
                    ret_code: -1,
                    ret_message: update failed, %s
                }''' % str(e)

    def mountTo(self, app):
        if app:
            app.route(path='/query', method='GET', callback=self.query)
            app.route(path='/insert', method='POST', callback=self.insert)
            app.route(path='/delete/<phone>', method='GET', callback=self.delete)
            app.route(path='/update', method='GET', callback=self.update)

