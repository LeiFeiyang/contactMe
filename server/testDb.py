from db import DB, Contact

myDb = DB()
myDb.createTable()
one = Contact(name='xiaoming2', email='xiaoming@gmail.com', phone = '15002222222', company='huawei')
ret = myDb.insert(one)
print('insert result: ', ret)
ret = myDb.query()