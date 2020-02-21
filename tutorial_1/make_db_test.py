import sqlite3

conn = sqlite3.connect('db/company.db')
print(conn)

curs = conn.cursor()
print(curs)

# print(sqlite3.sqlite_version_info)
# print(curs.execute('SELECT sqlite_version()').fetchall())

# 데이터 베이스에 table 생성
curs.execute('drop table if exists employee')
curs.execute('create table employee(id, first name, last name, age)')

# table에 명시적으로 하나의 레코드 넣기
curs.execute("insert into employee values(1, 'jangwon', 'lee', 29)")

# placeholder를 이용하여 다수의 레코드 넣기
sql = 'insert into employee values (?, ?, ?, ?)'
records = [(2, 'sunhwa', 'lee', 30),
           (3, 'jongmin', 'kim', 29),
           (4, 'jaehak', 'kim', 28),
           (5, 'sungju', 'han', 26),
           (6, 'junghwan', 'kim', 26)]

for r in records:
    curs.execute(sql, r)

conn.commit()

rows = curs.execute('select id, age from employee')
for row in rows:
    print(row)

rows = curs.execute('select last name, first name from employee')
for row in rows:
    print(row)

rows = curs.execute('select * from employee')
for row in rows:
    print(row)

conn.close()
