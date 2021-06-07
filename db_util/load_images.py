from os import walk
import time
import sqlite3
import computervision as cv


con = sqlite3.connect('db.db')
cur = con.cursor()

_, _, filenames = next(walk("./static"))

print(filenames)
index = 0
batch_size = 0
for name in filenames:
    print("Current file:" + name)
    batch_size +=1
    description, tags = cv.get_image_analysis(name)
    cur.execute('''
                INSERT INTO images VALUES ('%s', %d, '%s', '%s');
                ''' % (name, index, description, tags))
    index += 1


    # Currently used Azure account is a student account with a Free tier Computer Vision sevice.
    # This means that only 10 API calls can be done per minute
    if batch_size == 10:
        print("Limit reached, sleeping for 1 min")
        time.sleep(60)
        batch_size = 0


con.commit()

con.close()
