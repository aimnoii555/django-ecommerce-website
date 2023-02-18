
import sqlite3
import csv

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

#-------------------csv-----------------------
with open('firstweb/newtoken.csv',newline='',encoding='utf-8') as f:
    fr = csv.reader(f) #file reader
    print(list(fr))