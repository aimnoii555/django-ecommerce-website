import sqlite3
import csv

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()



with conn:
    c.execute("""SELECT * FROM myapp_orderpending WHERE user_id = 7""")
    data = c.fetchall()
    # data = c.fetchmany(5)
    # print(data)
    for d in data:
        print(d)
        print('-------------')

    #---------------Export to csv-----------------------------
    with open('allorder_user3.csv','w',newline='',encoding='utf-8') as f:
        fw = csv.writer(f) # File Writer
        fw.writerows(data)
        