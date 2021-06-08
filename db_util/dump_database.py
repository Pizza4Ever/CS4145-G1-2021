"""Script for dumping data in database db.db"""
import sqlite3
con = sqlite3.connect('db.db')

cur = con.cursor()

with open('dump.sql', 'w') as f:
    for line in con.iterdump():
        f.write('%s\n' % line)
con.close()
