from os import walk
import sqlite3
con = sqlite3.connect('example.db')
cur = con.cursor()

_, _, filenames = next(walk("./static"))

print(filenames)
index = 0
for name in filenames:
    cur.execute('''
                INSERT INTO images VALUES ('%s', %d);
                ''' % (name, index))
    index += 1

con.commit()

con.close()
