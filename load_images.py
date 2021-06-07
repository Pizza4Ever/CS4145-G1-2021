from os import walk
import sqlite3
import computervision as cv


con = sqlite3.connect('db.db')
cur = con.cursor()

_, _, filenames = next(walk("./static"))

print(filenames)
index = 0
for name in filenames:
    description, tags = cv.get_image_description(name)


    cur.execute('''
                INSERT INTO images VALUES ('%s', %d, '%s', '%s');
                ''' % (name, index, description, tags))
    index += 1

con.commit()

con.close()
