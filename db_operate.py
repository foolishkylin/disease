import pymysql
import time

host = '120.27.212.215'
user = 'dm1'
password = 'QGdm@666'
port = 3306
database = 'disease'

def db_connect():
    db = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()
    return db, cursor

def db_close(db, cursor):
    cursor.close()
    db.close()

def db_make(choice):
    db, cursor = db_connect()
    sql1 = "DROP TABLE IF EXISTS %s"
    sql2 = """CREATE TABLE %s"""

    if choice == 0:
        cursor.execute(sql1 % "COMMUNITY_DICT")
    # 使用预处理语句创建表
        cursor.execute(sql2 % "COMMUNITY_DICT ("
                              "USER_ID CHAR(20) NOT NULL, "
                              "COMMUNITY_ID INT)")
    elif choice == 1:
        cursor.execute(sql1 % "PAIR")
        # 使用预处理语句创建表
        cursor.execute(sql2 % "PAIR ("
                              "USER_ID CHAR(20) NOT NULL, "
                              "PAIRS VARCHAR(10000))")

    elif choice == 2:
        cursor.execute(sql1 % "MEET_TIME")
        # 使用预处理语句创建表
        cursor.execute(sql2 % "MEET_TIME ("
                              "USER_ID CHAR(20) NOT NULL, "
                              "MEET_TIME VARCHAR(10000))")

    db_close(db, cursor)

def db_insert(data, choice):
    # SQL 插入语句
    db, cursor = db_connect()
    num = len(data)
    it = 0
    if choice == 0:
        base_sql = """INSERT INTO COMMUNITY_DICT(USER_ID, COMMUNITY_ID) VALUES (%s, %d)"""
        for id in data.keys():
            sql = base_sql % (id, data[id])
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print("process: %d / %d" % (it, num))
                it += 1
            except:
                print('something wrong happended')
                # 如果发生错误则回滚
                db.rollback()
    elif choice == 1:
        base_sql = """INSERT INTO PAIR(USER_ID, PAIRS) VALUES (%s, \"%s\")"""
        for id in data.keys():
            sql = base_sql % (id, str(data[id]))
            try:
                # 执行sql语句
                db.ping(reconnect=True)
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print("process: %d / %d" % (it, num))
                it += 1
            except:
                print('something wrong happended')
                # 如果发生错误则回滚
                db.rollback()

    elif choice == 2:
        base_sql = """INSERT INTO MEET_TIME(USER_ID, MEET_TIME) VALUES (%s, "%s")"""
        for id in data.keys():
            sql = base_sql % (id, str(data[id]))
            try:
                # 执行sql语句
                db.ping(reconnect=True)
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print("process: %d / %d" % (it, num))
                it += 1
            except:
                print('something wrong happended')
                # 如果发生错误则回滚
                db.rollback()

    elif choice == 3:
        base_sql = """INSERT INTO PATIENT_LIST(USER_ID, TIME) VALUES (%s, "%s")"""
        for record in data:
            sql = base_sql % (record['user_id'], record['time'])
            try:
                # 执行sql语句
                db.ping(reconnect=True)
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print("process: %d / %d" % (it, num))
                it += 1
            except:
                print('something wrong happended')
                # 如果发生错误则回滚
                db.rollback()


    db_close(db, cursor)

def db_select():
    db, cursor = db_connect()
    pair = dict()
    meet_time = dict()
    patients = list()
    sql = "SELECT * FROM PAIR"
    cursor.execute(sql)
    data = cursor.fetchall()
    pair = dict()
    for row in data:
        pair[row[0]] = eval(row[1])

    sql = "SELECT * FROM MEET_TIME"
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        meet_time[row[0]] = eval(row[1])

    sql = "SELECT * FROM PATIENT_LIST"
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        patient = dict()
        patient['user_id'] = row[0]
        patient['time'] = row[1]
        patients.append(patient)


    db_close(db, cursor)

    return pair, meet_time, patients


if __name__ == '__main__':
    db_make()
    db_insert()